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
        force_parametric: "list[str]" = [],
    ) -> "dict[str,Union[str,Any]]":
        """Return the input parameters as a dict"""
        if isinstance(params, str):
            cur_item = ""
            inquote = 0
            new_params: list[str] = []
            for c in params:
                if c == " " and inquote == 0:
                    if cur_item != "":
                        new_params.append(cur_item)
                        cur_item = ""
                else:
                    if c == '"' and inquote == 0:
                        inquote = 2
                    elif c == '"' and inquote == 2:
                        inquote = 0
                    elif c == "'" and inquote == 0:
                        inquote = 1
                    elif c == "'" and inquote == 1:
                        inquote = 0
                    else:
                        cur_item += c
            if inquote != 0:
                ArgChecker.__err(ValueError, "Unmatched quote")
            if cur_item != "":
                new_params.append(cur_item)
            params = new_params

        cur_key = None
        force_param = False
        ret: "dict[str, Any]" = {}
        for v in params:
            if v.startswith("-") and not force_param:
                if cur_key != None:
                    ret[cur_key] = True
                cur_key = v.strip("-")
                if cur_key in force_parametric:
                    force_param = True
                else:
                    force_param = False
            elif cur_key != None:
                ret[cur_key] = ArgChecker.__cast(v)
                cur_key = None
                force_param = False
            else:
                # Argument without key
                ArgChecker.__err(ArgumentWithoutKeyError, v)
        if cur_key != None:
            ret[cur_key] = True
        return ret

    @overload
    def __init__(self, *, force_parametric: "list[str]" = []) -> None: ...

    @overload
    def __init__(self, pars: str, force_parametric: "list[str]" = []) -> None: ...

    @overload
    def __init__(
        self, pars: "dict[str, Any]", force_parametric: "list[str]" = []
    ) -> None: ...

    def __init__(
        self,
        pars: "Union[None,str,dict[str,Any]]" = None,
        force_parametric: "list[str]" = [],
    ):
        if pars is None:
            self.__args = ArgChecker.get_dict(force_parametric=force_parametric)
        elif isinstance(pars, str):
            self.__args = ArgChecker.get_dict(pars, force_parametric=force_parametric)
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
