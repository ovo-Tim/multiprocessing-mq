from typing import Any

base_type = ["<class 'int'>", "<class 'str'>", "<class 'float'>", "<class 'bool'>", "<class 'NoneType'>", "<class 'list'>", "<class 'tuple'>", "<class 'dict'>"] # The types that can just copy
# base_magic_method = ["__call__", "__len__", "__str__", "__repr__", "__bool__", "__format__", "__hash__", "__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__", "__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__", "__mod__", "__divmod__", "__pow__", "__lshift__", "__rshift__", "__and__", "__xor__", "__or__", "__radd__", "__rsub__", "__rmul__", "__rtruediv__", "__rfloordiv__", "__rmod__", "__rdivmod__", "__rpow__", "__rlshift__", "__rrshift__", "__rand__", "__rxor__", "__ror__"]

class inter():
    def __init__(self, run_code, path:str = None):
        self.___run_code = run_code
        self.___path = path
    
    def __getattr__(self, __name: str) -> Any:
        # print(__name)
        if self.___path is not None:
            var_path = self.___path + "." + __name
        else:
            var_path = __name

        vtype = self.___run_code(f"str(type({ var_path }))")
        child_class = {}
        if vtype == "<class 'function'>" or vtype == "<class 'method'>":
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

                return self.___run_code(f"{var_path}({args_code})", my_args)
            return func
        elif vtype in base_type:
            return self.___run_code(f"{var_path}")
        else: # class
            if var_path in child_class:
                return child_class[var_path]
            child_class[var_path] = inter(self.___run_code, var_path)
            return child_class[var_path]

    def __call__(self, *args, **kwargs):
        return self.__getattr__("__call__")(*args, **kwargs)