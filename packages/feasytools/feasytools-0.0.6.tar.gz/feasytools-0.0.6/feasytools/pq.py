import heapq
from collections import deque
from typing import Generic, TypeVar

QItem=TypeVar("QItem")

class Heap(Generic[QItem]):
    '''小根堆数据结构'''
    def __init__(self):
        self._q=[]
    
    def push(self,item:QItem):
        '''入堆, O(log n)'''
        heapq.heappush(self._q,item)
    
    def pop(self)->QItem:
        '''弹出堆顶元素, O(log n)'''
        return heapq.heappop(self._q)
    
    def remove(self,item)->bool:
        '''弹出item元素, O(n)'''
        try:
            idx=self._q.index(item)
        except ValueError:
            return False
        self._q.pop(idx)
        heapq.heapify(self._q)
        return True
    
    @property
    def top(self)->QItem:
        '''获取堆顶元素，但不弹出, O(1)'''
        return self._q[0]
    
    def __len__(self)->int:
        return len(self._q)
    
    def __contains__(self,obj)->bool:
        '''检查元素是否存在, O(n)'''
        return obj in self._q
    
    def empty(self)->bool:
        '''检测堆是否为空, O(1)'''
        return len(self._q)==0
    
class PQueue(Generic[QItem]):
    '''优先级队列（小根堆数据结构）'''
    def __init__(self):
        self._q:'list[tuple[int,QItem]]'=[]
    
    def push(self,pri:int,item:QItem)->None:
        '''
        入队, O(log n)
            pri: 优先级
            item: 元素
        '''
        heapq.heappush(self._q,(pri,item))
    
    def pop(self)->'tuple[int,QItem]':
        '''获取队首元素并出队, O(log n)'''
        return heapq.heappop(self._q)
    
    def remove(self,item:QItem)->bool:
        '''弹出第一个item元素, O(n), 返回是否成功'''
        idx=-1
        for i,(_,data) in enumerate(self._q):
            if data == item:
                idx = i
                break
        if idx==-1: return False
        self._q.pop(idx)
        heapq.heapify(self._q)
        return True
    
    @property
    def top(self)->'tuple[int,QItem]':
        '''获取队首元素，但不出队, O(1)'''
        return self._q[0]
    
    def __len__(self)->int:
        return len(self._q)
    
    def __contains__(self,obj)->bool:
        return obj in self._q
    
    def empty(self)->bool:
        '''检测队列是否为空, O(1)'''
        return len(self._q)==0
    
    def __str__(self)->str:
        '''转为字符串, O(nlogn)'''
        q2=self._q.copy()
        q2.sort()
        return str(q2)

class BufferedPQ(Generic[QItem]):
    '''
    含有缓冲的优先级队列。
    该数据结构分为两部分，一个普通队列(记为q)和一个优先级队列(记为p)。
    优先级队列大小恒定(设大小为n)，普通队列大小可变(设大小为m)。
    数据进入普通队列，而后进入优先级队列，最后离开本结构。
    '''
    def __init__(self,p_size:int):
        self._sz=p_size
        self._P:'PQueue[QItem]'=PQueue()
        self._Q:'deque[tuple[int,QItem]]'=deque()
        self._sP=set()
        self._sQ=set()

    def __len__(self)->int:
        return len(self._P)+len(self._Q)
    
    @property
    def p_size(self)->int:
        '''获取优先级区大小'''
        return self._sz
    
    @property
    def p_len(self)->int:
        '''检查优先级区长度, O(1)'''
        return len(self._P)
    
    @property
    def q_len(self)->int:
        '''检查缓冲区长度, O(1)'''
        return len(self._Q)
    
    def __contains__(self,obj)->bool:
        '''检查元素是否存在, O(1)'''
        return obj in self._sP or obj in self._sQ
    
    def push(self,pri:int,obj:QItem)->bool:
        '''
        入队, O(log n)
            pri: 优先级
            item: 元素
        '''
        if self.__contains__(obj): return False
        if len(self._P)<self._sz:
            self._P.push(pri,obj)
            self._sP.add(obj)
        else:
            self._Q.append((pri,obj))
            self._sQ.add(obj)
        return True
    
    def top(self)->'tuple[int,QItem]':
        '''获取队首元素，但不出队, O(1)'''
        return self._P.top
    
    def pop(self)->'tuple[int,QItem]':
        '''获取队首元素并出队, O(log n)'''
        ret=self._P.pop()
        self._sP.remove(ret[1])
        if len(self._Q)>0:
            pri,obj=self._Q.popleft()
            self._sQ.remove(obj)
            self._P.push(pri,obj)
            self._sP.add(obj)
        return ret
    
    def empty(self)->bool:
        '''检测队列是否为空, O(1)'''
        return self._P.empty()
    
    def remove(self,obj)->bool:
        '''弹出第一个obj元素, O(n+m), 返回是否成功'''
        if self._P.remove(obj): return True
        try:
            self._Q.remove(obj)
            return True
        except:
            return False
        
    def p_has(self,obj)->bool:
        '''检查元素是否存在于优先级区, O(1)'''
        return obj in self._sP
    
    def q_has(self,obj)->bool:
        '''检查元素是否存在于缓冲区, O(1)'''
        return obj in self._sQ
    
    def __str__(self)->str:
        '''转为字符串, O(nlogn+m)'''
        return f"BufferedPQ[P={self._P},Q={self._Q}]"