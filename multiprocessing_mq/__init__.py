import multiprocessing as mp
import threading
import time
import random

def create_process(send_que:mp.Queue, rec_que:mp.Queue, init, rest_time):
    if init is not None:
        _locals = init()
        for (i,j) in _locals.items():
            globals()[i] = j

    while True:
        if not send_que.empty():
            com = send_que.get()
            if com[1] == 0:
                func = lambda: rec_que.put([com[0], eval(com[2])]) # run the function and return the result
                threading.Thread(target=func).start()
            elif com[1] == 1:
                threading.Thread(target=lambda: eval(com[2])).start()
        else:
            time.sleep(rest_time)

class Process():
    '''
        Create a process.

        communicate:
            id(int): process id
            command(int): 
                0: run code
                1: run code without returning
            code(str): code to run

    '''
    def __init__(self, init = None, process_events = None, rest_time:int = 0.05):
        self.send_que = mp.Queue()
        self.rec_que = mp.Queue()

        self.process_events = process_events
        self.rest_time = rest_time
        self.result = {} # result of the process {id: result}
        self.runung_id = []

        self.process = mp.Process(
                target=create_process, 
                args=(self.send_que, self.rec_que, init, rest_time))
        self.process.start()

    def get_id(self):
        pro_id = random.randint(1, 1e9)
        while pro_id in self.runung_id:
            pro_id = random.randint(1, 1e9)
        self.runung_id.append(pro_id)
        return pro_id

    def run_com(self, code:str, process_events = None):
        pro_id = self.get_id()
        self.send_que.put([pro_id, 0, code])

        while True: # wait for the result
            if process_events is not None:
                process_events()
            if not self.rec_que.empty():
                result = self.rec_que.get()
                self.result[result[0]] = result[1]

                if self.result[pro_id] is not None:
                    re = self.result[pro_id]
                    del self.result[pro_id]
                    return re
            else:
                time.sleep(self.rest_time)

    def run_without_return(self, code:str):
        pro_id = self.get_id()
        self.send_que.put([pro_id, 1, code])
