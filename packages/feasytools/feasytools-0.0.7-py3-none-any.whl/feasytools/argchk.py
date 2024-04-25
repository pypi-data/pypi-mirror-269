# ArgChecker: A simple tool for parsing command line arguments with type checking and error handling
import sys
from typing import Any, Callable, Iterable, Optional, Union, overload


class KeyNotSpecifiedError(KeyError):
    def __init__(self, key: str):
        super().__init__(f"'{key}' must be specified.")
        self.key = key


class ArgumentWithoutKeyError(ValueError):
    def __init__(self, val: str):
        super().__init__(f"'{val}' is an argument without key.")
        self.val = val


class ArgChecker:
    ErrorHandler: "Optional[Callable[[Exception],None]]" = None

    @staticmethod
    def __err(err_type: type, data: str):
        if ArgChecker.ErrorHandler is not None:
            ArgChecker.ErrorHandler(err_type(data))
        # If the error handler is not set or does not terminate the program, raise the error directly
        raise err_type(data)

    @staticmethod
    def __cast(v: str) -> "Union[None,bool,int,float,str]":
        if v == "True":
            return True
        if v == "False":
            return False
        if v == "None":
            return None
        try:
            return int(v)
        except:
            pass
        try:
            return float(v)
        except:
            return v.strip('"')

    @staticmethod
    def get_dict(
        params: "Union[str,Iterable[str]]" = sys.argv[1:],
    ) -> "dict[str,Union[str,Any]]":
        """ Return the input parameters as a dict """
        if isinstance(params, str):
            params = params.split(sep=" ")
            new_params: "list[str]" = []
            in_quotes1 = False
            in_quotes2 = False
            current_param = ""
            for param in params:
                if param.startswith('"') and not param.endswith('"'):
                    in_quotes2 = True
                    current_param = param
                elif in_quotes2:
                    current_param += " " + param
                    if param.endswith('"'):
                        in_quotes2 = False
                        new_params.append('"' + current_param.strip('"') + '"')
                elif param.startswith("'") and not param.endswith("'"):
                    in_quotes1 = True
                    current_param = param
                elif in_quotes1:
                    current_param += " " + param
                    if param.endswith("'"):
                        in_quotes1 = False
                        new_params.append('"' + current_param.strip('"') + '"')
                else:
                    new_params.append(param)
            params = new_params

        cur_key = None
        ret: "dict[str, Any]" = {}
        for v in params:
            if v.startswith("-"):
                if cur_key != None:
                    ret[cur_key] = True
                cur_key = v.strip("-")
            elif cur_key != None:
                ret[cur_key] = ArgChecker.__cast(v)
                cur_key = None
            else:
                # Argument without key
                ArgChecker.__err(KeyError, v)
        if cur_key != None:
            ret[cur_key] = True
        return ret

    def __init__(self, pars: "Union[None,str,dict[str,Any]]" = None):
        if pars is None:
            self.__args = ArgChecker.get_dict()
        elif isinstance(pars, str):
            self.__args = ArgChecker.get_dict(pars)
        elif isinstance(pars, dict):
            self.__args = pars
        else:
            raise TypeError(type(pars))

    def pop_bool(self, key: str) -> bool:
        if self.__args.pop(key, False):
            return True
        return False

    def pop_int(self, key: str, default: "Optional[int]" = None) -> int:
        val = self.__args.pop(key, default)
        if val is None:
            ArgChecker.__err(KeyNotSpecifiedError, key)
        return int(val)

    def pop_str(self, key: str, default: "Optional[str]" = None) -> str:
        val = self.__args.pop(key, default)
        if val is None:
            ArgChecker.__err(KeyNotSpecifiedError, key)
        return str(val).strip('"')

    def pop_float(self, key: str, default: "Optional[float]" = None) -> float:
        val = self.__args.pop(key, default)
        if val is None:
            ArgChecker.__err(KeyNotSpecifiedError, key)
        return float(val)

    def empty(self) -> bool:
        return len(self.__args) == 0

    def keys(self):
        return self.__args.keys()

    def values(self):
        return self.__args.values()

    def items(self):
        return self.__args.items()

    def __len__(self) -> int:
        return len(self.__args)

    def __getitem__(self, key: str):
        return self.__args[key]

    def __repr__(self):
        return "ArgChecker<" + repr(self.__args) + ">"

    def __str__(self):
        return str(self.__args)
