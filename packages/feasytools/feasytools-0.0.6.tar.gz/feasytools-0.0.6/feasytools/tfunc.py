from abc import ABCMeta, abstractmethod
from functools import reduce
from operator import add, sub, mul, truediv, floordiv
from typing import Callable, Iterable, Optional, Union
import bisect

class TimeFunc(metaclass=ABCMeta):
    '''时变函数'''
    @abstractmethod
    def __call__(self,time:int)->float: ...
    @abstractmethod
    def __str__(self)->str: ...
    def __add__(self,other:'FloatLike')->'TimeFunc':
        return calcFunc(self,other,'+')
    def __sub__(self,other:'TimeFunc')->'TimeFunc':
        return calcFunc(self,other,'-')
    def __mul__(self,other)->'TimeFunc':
        return calcFunc(self,other,'*')
    def __truediv__(self,other)->'TimeFunc':
        return calcFunc(self,other,'/')
    def __floordiv__(self,other)->'TimeFunc':
        return calcFunc(self,other,'//')

_oper_trans = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '//': floordiv
}
_Oper = Callable[[float,float],float]
FloatLike = Union[TimeFunc,float,int]

class OverrideFunc(TimeFunc):
    '''重载函数. 正常情况下返回原始时间函数的值, 当设置了重载值时返回重载值'''
    def __init__(self,default:TimeFunc,override_val:Optional[float] = None):
        self._val:TimeFunc=default
        self._override:Optional[float] = override_val
    
    def __call__(self,t:int)->float:
        if self._override is not None: return self._override
        return self._val(t)
    
    def setOverride(self,overval:float):
        '''设置重载值'''
        self._override=overval
    
    def clearOverride(self):
        '''清除重载值'''
        self._override=None
    
    def __str__(self):
        if self._override is None: return f"OverrideF<{self._val}>"
        return f"OverrideF<O={self._override}>"

    def __repr__(self): return str(self)

class PlusFunc(TimeFunc):
    '''和函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)+self._f2(_t)
    def __str__(self)->str: return f"F<{self._f1}+{self._f2}>"
    def __repr__(self)->str: return str(self)

class QuickSumFunc(TimeFunc):
    '''快速求和函数'''
    def __init__(self,funcs:'list[TimeFunc]'): self._fs=funcs
    def __call__(self,_t:int)->float: return sum(f(_t) for f in self._fs)
    def __str__(self)->str: return f"FSum<{len(self._fs)} funcs>"
    def __repr__(self)->str: return str(self)

class MinusFunc(TimeFunc):
    '''差函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)-self._f2(_t)
    def __str__(self)->str: return f"F<{self._f1}-{self._f2}>"
    def __repr__(self)->str: return str(self)

class MulFunc(TimeFunc):
    '''积函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)*self._f2(_t)
    def __str__(self)->str: return f"F<{self._f1}*{self._f2}>"
    def __repr__(self)->str: return str(self)

class QuickMulFunc(TimeFunc):
    '''快速求积函数'''
    def __init__(self,funcs:'list[TimeFunc]'): self._fs=funcs
    def __call__(self,_t:int)->float: return reduce(mul, (f(_t) for f in self._fs))
    def __str__(self)->str: return f"FMul<{len(self._fs)} funcs>"
    def __repr__(self)->str: return str(self)

class TrueDivFunc(TimeFunc):
    '''商函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)/self._f2(_t)
    def __str__(self)->str: return f"F<{self._f1}/{self._f2}>"
    def __repr__(self)->str: return str(self)

class FloorDivFunc(TimeFunc):
    '''整除函数'''
    def __init__(self,f1:TimeFunc,f2:TimeFunc): self._f1=f1; self._f2=f2
    def __call__(self,_t:int)->float: return self._f1(_t)//self._f2(_t)
    def __str__(self)->str: return f"F<{self._f1}//{self._f2}>"
    def __repr__(self)->str: return str(self)

class ConstFunc(TimeFunc):
    '''常数函数'''
    def __init__(self,const:float): self._val:float=const
    def __call__(self,time:int)->float: return self._val
    def __str__(self)->str: return f"ConstF<{self._val}>"
    def __repr__(self)->str: return str(self)

class SegFunc(TimeFunc):
    '''分段常数函数'''
    def __init__(self,time_line:'list[int]',data:'list[float]'):
        if len(time_line) != len(data): raise ValueError(f"时间线长度{len(time_line)}和数据长度{len(data)}不一致")
        for i in range(1,len(time_line)):
            if time_line[i]<=time_line[i-1]:
                raise ValueError(f"时间必须严格递增: [{i}]={time_line[i]}<=[{i-1}]={time_line[i-1]}")
        self._tl = time_line
        self._d = data   
    
    def __call__(self,time:int)->float:
        if time < self._tl[0]: raise ValueError(f"时间{time}必须在开始时间{self._tl[0]}之后")
        return self._d[bisect.bisect_right(self._tl, time) - 1]
    def __str__(self)->str: return f"SegF<{len(self._d)} segs>"
    def __repr__(self)->str: return str(self)

class TimeImplictFunc(TimeFunc):
    '''隐式时变函数, 即调用的时机决定了时间, 而无需在__call__时指定。__call__的参数time无效'''
    def __init__(self,func:'Callable[[],float]'):self._f=func
    def __call__(self,time:int)->float:return self._f()
    def __str__(self)->str:return f"TImpF<{self._f}>"
    def __repr__(self)->str: return str(self)

class ComFunc(TimeFunc):
    '''将普通Python函数包装成可运算函数'''
    def __init__(self,func:'Callable[[int],float]'):self._f=func
    def __call__(self,time:int)->float:return self._f(time)
    def __str__(self)->str:return f"TImpF<{self._f}>"
    def __repr__(self)->str: return str(self)

class ManualFunc(TimeFunc):
    '''手动指定常数函数'''
    def __init__(self,init_val:float):self._v=init_val
    def setManual(self,val:float):self._v=val
    def __call__(self,time:int)->float:return self._v
    def __str__(self)->str:return f"ManF<{self._v}>"
    def __repr__(self)->str: return str(self)

def __calc_c0(f1:Union[ConstFunc,float],f2:float,op:_Oper)->float:
    if isinstance(f1,float): return op(f1,f2)
    elif isinstance(f1,ConstFunc): return op(f1._val,f2)
    else: raise TypeError(f1)

def __calc_c1(f1:SegFunc,f2:float,op:_Oper)->SegFunc:
    return SegFunc(f1._tl,[op(d,f2) for d in f1._d])

def __calc_c2(f1:TimeImplictFunc,f2:float,op:_Oper)->TimeImplictFunc:
    return TimeImplictFunc(lambda: op(f1._f(),f2))

def quicksum(funcs:Iterable[TimeFunc])->TimeFunc:
    '''快速求和'''
    ret = list(funcs)
    if len(ret)==0: return ConstFunc(0)
    if len(ret)==1: return ret[0]
    if len(ret)==2: return PlusFunc(ret[0],ret[1])
    return QuickSumFunc(ret)

def quickmul(funcs:Iterable[TimeFunc])->TimeFunc:
    '''快速求积'''
    ret = list(funcs)
    if len(ret)==0: return ConstFunc(1)
    if len(ret)==1: return ret[0]
    if len(ret)==2: return MulFunc(ret[0],ret[1])
    return QuickMulFunc(ret)

def calcFunc(f1:FloatLike,f2:FloatLike,op:str)->TimeFunc:
    _op = _oper_trans[op]
    if isinstance(f2,ConstFunc): f2=f2._val
    if isinstance(f2,(float,int)):
        if isinstance(f1,(ConstFunc,float,int)): return ConstFunc(__calc_c0(f1,f2,_op))
        elif isinstance(f1,SegFunc): return __calc_c1(f1,f2,_op)
        elif isinstance(f1,TimeImplictFunc): return __calc_c2(f1,f2,_op)
        else: f2 = ConstFunc(f2)
    if isinstance(f1,(float,int)): f1 = ConstFunc(f1)
    if isinstance(f1,ConstFunc) and op in ['+','*']:
        if isinstance(f2,SegFunc): return __calc_c1(f2,f1._val,_op)
        elif isinstance(f2,TimeImplictFunc): return __calc_c2(f2,f1._val,_op)
    assert isinstance(f1,TimeFunc) and isinstance(f2,TimeFunc)
    if op=='+': return PlusFunc(f1,f2)
    elif op=='-': return MinusFunc(f1,f2)
    elif op=='*': return MulFunc(f1,f2)
    elif op=='/': return TrueDivFunc(f1,f2)
    elif op=='//': return FloorDivFunc(f1,f2)
    else: raise ValueError(op)

def makeFunc(time_line:'list[int]',data:list)->TimeFunc:
    '''生成分段常数函数或常数函数'''
    if len(time_line)!=len(data): raise ValueError(f"时间线长度{len(time_line)}和数据长度{len(data)}不一致")
    if len(data)==1: return ConstFunc(data[0])
    else: return SegFunc(time_line,data)
