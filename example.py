from typing import Any
import multiprocessing_mq as mq
import time
def init_code():
    import os, time

    v_int = 123
    v_str = "hello world"
    v_float = 1.23
    v_bool = True

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

    class my_class():
        def __init__(self):
            self.a = "from class"
        def print_func(self):
            print("function from class")
        def __call__(self, *args: Any, **kwds: Any) -> Any:
            print("Call from class")

        def __len__(self):
            return 114514

    My_class = my_class()
    
    # print(locals())
    return locals()
    
my_pro = mq.Process(init=init_code, suspend=True, rest_time=0.01)

# my_pro.run_without_return("c()")
# my_pro.run_without_return("d()")
# time.sleep(2)

# Two ways to call the function
msg = "hello world"
my_pro.inter.a(msg)
my_pro.run_without_return("a(msg)", args={"msg": msg})
print(my_pro.run_com("b()"))
print(my_pro.inter.b())


# Get some basic type variables
my_pro.inter.v_int = 5
print(my_pro.inter.v_int)
print(my_pro.inter.v_str)
print(my_pro.inter.v_float)
print(my_pro.inter.v_bool)

# Complex class
print(my_pro.inter.My_class.a)
my_pro.inter.My_class.print_func()
my_pro.inter.My_class()
print(my_pro.inter.My_class.__len__())
print(len(my_pro.inter.My_class))

my_pro.inter.new_var = "This is a new var"
print(my_pro.inter.new_var)

# time.sleep(1)
# my_pro.stop()
my_pro.forced_stop()
print("finish")