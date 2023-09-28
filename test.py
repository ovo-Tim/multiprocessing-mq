import multiprocessing_mq as mq
import time
def init_code():
    import os, time

    def a(msg):
        print(os.getpid())
        print(f"The message is: { msg }")

    def b():
        return "It's from B!"
    
    def c():
        for i in range(10):
            print(1)
            time.sleep(0.5)
    
    def d():
        for i in range(10):
            print(2)
            time.sleep(0.5)
    
    # print(locals())
    return locals()
    
my_pro = mq.Process(init=init_code)
my_pro.run_without_return("c()")
my_pro.run_without_return("d()")
time.sleep(2)
print(my_pro.run_com("b()"))
msg = "hello world"
my_pro.run_without_return("a(msg)", args={"msg": msg})
# time.sleep(3)
# my_pro.stop()
my_pro.forced_stop()
print("finish")