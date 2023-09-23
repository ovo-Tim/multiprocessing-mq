import multiprocessing_mq as mq

def init_code():
    import os

    def a():
        print(os.getpid())

    def b():
        return "It's from B!"
    
    # print(locals())
    return locals()
    
my_pro = mq.Process(init=init_code)
print(my_pro.run_com("b()"))
my_pro.run_without_return("a()")