import multiprocessing as mp
import threading
import time
import random
from typing import Any
import psutil
from . import interactivity
import dill
from multiprocessing.queues import Queue
from multiprocessing.shared_memory import SharedMemory

try:
    waitting_list = SharedMemory(name='waitting_list', create=True, size=1)
except:
    waitting_list = SharedMemory(name='waitting_list')
memory_view = memoryview(waitting_list.buf)
memory_view[0] = 0

def create_process(send_que:mp.Queue, rec_que:mp.Queue, init, rest_time, suspend):
    global running_func, need_suspend

    from os import getpid
    import psutil
    __pid = getpid()
    __proc = psutil.Process(__pid)

    running_func = 0
    need_suspend = False
    if init is not None:
        _locals = init()
        for (i,j) in _locals.items():
            globals()[i] = j

    waitting_list = SharedMemory(name='waitting_list')

    while True:
        # print("loop")
        if not send_que.empty():
            com = send_que.get()
            waitting_list.buf[0] -= 1
            # print(waitting_list.buf[0])
            # print(com)
            if com == -1:
                exit()
            elif com[1] == 0:
                def func(): # run the function and return the result
                    global running_func
                    running_func += 1
                    # print(com[2])
                    returns = eval(com[2], globals(), com[3])
                    rec_que.put([com[0], returns])
                    running_func -= 1
                    need_suspend = True
                    # print("finish", com[2])
                    # print("send", returns)
                threading.Thread(target=func).start()
            elif com[1] == 1:
                def func(): # run the function without returning
                    global running_func
                    running_func += 1
                    exec(com[2], globals(), com[3])
                    running_func -= 1
                    need_suspend = True
                threading.Thread(target=func).start()
        else:
            time.sleep(rest_time)
            if running_func == 0 and suspend and waitting_list.buf[0]==0 and need_suspend:
                # print("Suspend")
                need_suspend = False
                __proc.suspend()
            
class queue_plus(Queue):
    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize, ctx=mp.get_context())
    def put(self, obj, block: bool = True, timeout: float | None = None) -> None:
        obj = dill.dumps(obj)
        return super().put(obj, block, timeout)
    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        return dill.loads(super().get(block, timeout))

class Process():
    '''
        Create a process.
        argments:
            init(func): init function
            process_events(func): What to do when waiting for the result
            rest_time(float): How long to sleep when waiting for the result or task.(I suggest you not to set 0, because queue needs time to transfer)
            suspend(bool): Whether to suspend when there is no task

        communicate:
            id(int): process id
            command(int): 
                0: run code
                1: run code without returning
                -1: exit
            code(str): code to run
            args(dict): 
                arguments

    '''
    def __init__(self, init = None, process_events = None, rest_time:int = 0.05, suspend = True):
        self.send_que = queue_plus(maxsize=1000)
        self.rec_que = queue_plus(maxsize=1000)

        self.process_events = process_events
        self.rest_time = rest_time
        self.suspend = suspend
        self.result = {} # result of the process {id: result}
        self.runung_id = []

        self.process = mp.Process(
                target=create_process, 
                args=(self.send_que, self.rec_que, init, rest_time, suspend))
        self.process.start()

        self.pid = self.process.pid
        self.proc_con = psutil.Process(self.pid)
        self.inter = interactivity.inter(self.run_com, self.run_without_return)

    def get_id(self):
        pro_id = random.randint(1, 1e9)
        while pro_id in self.runung_id:
            pro_id = random.randint(1, 1e9)
        self.runung_id.append(pro_id)
        return pro_id

    def send_msg(self, msg):
        self.send_que.put(msg)
        memory_view[0] += 1
        # print("send", msg)
        if self.suspend:
            self.proc_con.resume()
            self.proc_con.resume()
            self.proc_con.resume()

    def run_com(self, code:str,args:dict = {}, process_events = None):
        '''
            Run the code and return the result.
            We use `eval` to run the code, so you can't change variables in the code(You can use `run_without_return`)
            args: 
                We won't help you to put the arguments into you function, that means you have to put the arguments by yourself.
                Example:
                    if you want to run `my_func(a)`, you should use `run_com('my_func(a)', {'a': 1})`
        '''

        # print(code)

        pro_id = self.get_id()
        self.send_msg([pro_id, 0, code, args])

        while True: # wait for the result
            # print("watting")
            # self.proc_con.resume() # TODO: I'm tired, but there still a bug
            if process_events is not None:
                process_events()
            if pro_id in self.result:
                re = self.result[pro_id]
                self.result.pop(pro_id)
                self.runung_id.remove(pro_id)
                return re
            if not self.rec_que.empty():
                result = self.rec_que.get()
                # print("get", result)
                self.result[result[0]] = result[1]
            else:
                time.sleep(self.rest_time)

    def run_without_return(self, code:str, args:dict = {}):
        '''
            Run the given code without expecting a return value. (We use `exec`)
            args: 
                We won't help you to put the arguments into you function, that means you have to put the arguments by yourself.
                Example:
                    if you want to run `my_func(a)`, you should use `run_com('my_func(a)', {'a': 1})`
        '''
        # pro_id = self.get_id()
        self.send_msg([0, 1, code, args])

    def stop(self):
        waitting_list.unlink()
        self.send_msg(-1)

    def forced_stop(self):
        self.stop()
        self.proc_con.terminate()

    def create_class(self, cls, name: str):
        self.run_without_return(f"{name} = {name}()", args={name: cls}) # instantiate
        return getattr(self.inter, name)