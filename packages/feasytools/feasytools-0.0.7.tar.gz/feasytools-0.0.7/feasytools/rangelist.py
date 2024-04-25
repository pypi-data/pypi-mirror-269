import xml.etree.ElementTree as ET
from typing import Union, overload

class RangeList:
    '''时间范围列表，用于表示一系列时间段'''
    @staticmethod
    def parse_time(s:str)->int:
        '''将时间字符串转换为秒数, 支持格式为hh:mm:ss或者一个可转化成int的字符串'''
        try:
            return int(s)
        except:
            h,m,s = s.split(":")
            return int(h)*3600+int(m)*60+int(s)
    
    @overload
    def __init__(self, data: ET.Element): '''从xml节点初始化'''
    @overload
    def __init__(self, data: 'list[tuple[int,int]]'): '''从列表初始化'''

    def __init__(self, data: 'Union[list[tuple[int,int]], ET.Element]'):
        if isinstance(data,ET.Element):
            loop_period = int(data.attrib.get("loop_period", 0))
            loop_times = int(data.attrib.get("loop_times", 1))
            assert loop_times >= 1
            data = [(self.parse_time(itm.attrib['btime']),self.parse_time(itm.attrib["etime"])) for itm in data]
            if loop_times > 1 and len(data) > 1:
                assert loop_period > data[-1][1]
                n = len(data)
                for j in range(1, loop_times):
                    for i in range(n):
                        if data[i][0]>=data[i][1]: raise ValueError(f"起始时间{data[i][0]}晚于终止时间{data[i][1]}")
                        data.append((data[i][0]+loop_period*j,data[i][1]+loop_period*j))
        self._d:'list[tuple[int,int]]' = data
    
    def __contains__(self, t:int):
        for (l,r) in self._d:
            if l<=t and t<r: return True
        return False
    
    def __len__(self)->int: return self._d.__len__()

    def __getitem__(self, indices): return self._d.__getitem__(indices)
    
    def __str__(self): return str(self._d)

    def __iter__(self): return iter(self._d)