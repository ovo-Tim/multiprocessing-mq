from typing import Any
from types import FunctionType

base_type = ["<class 'int'>", "<class 'str'>", "<class 'float'>", "<class 'bool'>", "<class 'NoneType'>", "<class 'list'>", "<class 'tuple'>", "<class 'dict'>"] # The types that can just copy
# base_magic_method = ["__call__", "__len__", "__str__", "__repr__", "__bool__", "__format__", "__hash__", "__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__", "__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__", "__mod__", "__divmod__", "__pow__", "__lshift__", "__rshift__", "__and__", "__xor__", "__or__", "__radd__", "__rsub__", "__rmul__", "__rtruediv__", "__rfloordiv__", "__rmod__", "__rdivmod__", "__rpow__", "__rlshift__", "__rrshift__", "__rand__", "__rxor__", "__ror__"]

class inter():
    def __init__(self, run_code, run_code_wr, path:str = None, without_return:list = []):
        self.___run_code = run_code
        self.___run_code_wr = run_code_wr
        self.___path = path
        self.___without_return = without_return
        self.___child_class = {}

        # TODO: Create magic methods
        # funcs:list[str] = self.___run_code(f"dir({ self.___path })")
        # for i in funcs:
        #     if i in base_magic_method:
        #         func_code = compile(f"def {i}(*args, **kwargs): return self.__getattr__('{i}')(*args, **kwargs)", "<string>", "exec")
        #         func = FunctionType(func_code.co_consts[0], locals(), i)
        #         setattr(self, i, func)

        # print(self.___path)
        # print(dir(self))
                
    
    def __getattr__(self, __name: str) -> Any:
        # print(__name)
        if self.___path is not None:
            var_path = self.___path + "." + __name
        else:
            var_path = __name

        vtype = self.___run_code(f"str(type({ var_path }))")
        if vtype == "<class 'function'>" or vtype == "<class 'method'>":
            # print(var_path)
            def func(*args, **kwargs):
                my_args = {}
                args_code = ""
                for i in range(len(args)):
                    args_code += f"__arg{i}, "
                    my_args[f"__arg{i}"] = args[i]

                for i in kwargs.keys():
                    args_code += f"{i}={i}, "
                args_code = args_code[:-2]
                my_args.update(kwargs)
                if __name in self.___without_return:
                    return self.___run_code_wr(f"{var_path}({args_code})", my_args)
                else:
                    return self.___run_code(f"{var_path}({args_code})", my_args)
            return func
        elif vtype in base_type:
            return self.___run_code(f"{var_path}")
        else: # class
            if not var_path in self.___child_class:
                self.___child_class[var_path] = inter(self.___run_code, self.___run_code_wr, var_path)
            return self.___child_class[var_path]


    # Link the magic methods
    def __call__(self, *args, **kwargs):
        # pass
        return self.__getattr__("__call__")(*args, **kwargs)

    def __getitem__(self, item):
        return self.__getattr__("__getitem__")(item)

    def __setitem__(self, key, value):
        return self.__getattr__("__setitem__")(key, value)
    
    def __repr__(self):
        return self.__getattr__("__repr__")()
    
    def __len__(self):
        return self.__getattr__("__len__")()
    
    def __iter__(self):
        return iter(self.__getattr__("__iter__")())
    
    def __str__(self):
        return self.__getattr__("__str__")()
    
    def __add__(self, other):
        return self.__getattr__("__add__")(other)
    
    def __sub__(self, other):
        return self.__getattr__("__sub__")(other)
    
    def __mul__(self, other):
        return self.__getattr__("__mul__")(other)
    
    def __truediv__(self, other):
        return self.__getattr__("__truediv__")(other)
    
    def __floordiv__(self, other):
        return self.__getattr__("__floordiv__")(other)
    
    def __mod__(self, other):
        return self.__getattr__("__mod__")(other)
    
    def __pow__(self, other):
        return self.__getattr__("__pow__")(other)
    
    def __lshift__(self, other):
        return self.__getattr__("__lshift__")(other)
    
    def __rshift__(self, other):
        return self.__getattr__("__rshift__")(other)
    
    def __and__(self, other):
        return self.__getattr__("__and__")(other)
    
    def __or__(self, other):
        return self.__getattr__("__or__")(other)
    
    def __xor__(self, other):
        return self.__getattr__("__xor__")(other)
    
    def __radd__(self, other):
        return self.__getattr__("__radd__")(other)
    
    def __rsub__(self, other):
        return self.__getattr__("__rsub__")(other)
    
    def __rmul__(self, other):
        return self.__getattr__("__rmul__")(other)
    
    def __rtruediv__(self, other):
        return self.__getattr__("__rtruediv__")(other)
    
    def __rfloordiv__(self, other):
        return self.__getattr__("__rfloordiv__")(other)
    
    def __rmod__(self, other):
        return self.__getattr__("__rmod__")(other)
    
    def __rdivmod__(self, other):
        return self.__getattr__("__rdivmod__")(other)