import struct, gzip
from typing import IO, BinaryIO, Generic, Optional, TextIO, Type, TypeVar, Union, Iterable, overload
import numpy as np
from abc import abstractmethod, ABCMeta

Table_DType = Type[Union[np.int32,np.float32]]
_Table_DType = TypeVar("_Table_DType",np.int32,np.float32)

def _Lchk(L):
    assert L=='i' or L=='f'

def _dtypechk(dtype):
    assert dtype==np.int32 or dtype==np.float32

def _L2dtype(L)->Type:
    return np.int32 if L=='i' else np.float32

def _dtype2L(dtype)->str:
    return 'i' if dtype==np.int32 else 'f'

class TableWriter(metaclass = ABCMeta):
    '''数据表写入器(抽象类)'''
    @abstractmethod
    def __init__(self,col_names:'list[str]',dtype:Type)->None:
        _dtypechk(dtype)
        self._col_names:'list[str]' = col_names
        self._dtype:Table_DType = dtype
    @property
    def col_num(self)->int: 
        '''数据表的列数'''
        return len(self._col_names)
    @property
    def dtype(self)->Type:
        '''数据表的数据类型'''
        return self._dtype
    @abstractmethod
    def write(self,data:list)->None: '''写入一条数据, 数据长度必须与列数相等'''
    @abstractmethod
    def write_all(self,data:np.ndarray)->None: '''写入多条数据, 数据长度(参数ndarray的列数)必须与本表的列数相等'''
    @abstractmethod
    def close(self)->None: '''关闭写入器'''

class FileTableWriter(TableWriter):
    '''文件数据表写入器(抽象类)'''
    @abstractmethod
    def __init__(self,fh:IO,col_names:'list[str]',dtype:Type)->None:
        super().__init__(col_names,dtype)
        self._fh=fh

class MemoryTableWriter(TableWriter):
    '''内存数据表写入器'''
    _data:np.ndarray
    def __init__(self,col_names:'list[str]',dtype:Type)->None:
        '''
        初始化
            col_names: 列名
            dtype: 数据类型, 可以是np.int32或np.float32
        '''
        super().__init__(col_names,dtype)
        self._data=np.zeros((0,len(col_names)),dtype=dtype)
    
    def write(self,data:list)->None:
        self._data=np.vstack([self._data,np.array(data,dtype=self._dtype)])
    
    def write_all(self,data:np.ndarray)->None:
        self._data=np.vstack([self._data,data])
    
    def close(self): pass

    @property
    def data(self)->np.ndarray: 
        '''获取写入的所有数据'''
        return self._data
        
class CsvTableWriter(FileTableWriter):
    '''CSV数据表写入器'''
    _fh: TextIO
    def __init__(self,fname:str,col_names:'list[str]',dtype:Type)->None:
        '''
        初始化
            fname: 文件名
            col_names: 列名
            dtype: 数据类型, 可以是np.int32或np.float32
        '''
        super().__init__(open(fname,"w"),col_names,dtype)
        self._fh.write(','.join(self._col_names)+"\n")

    def write(self,data:list)->None:
        self._fh.write(','.join(map(str,data))+"\n")
    
    def write_all(self, data: np.ndarray)->None:
        for ln in data: self.write(ln)
    
    def close(self): self._fh.close()

class BinTableWriter(FileTableWriter):
    '''二进制数据表写入器(抽象类)'''
    _fh: IO
    @abstractmethod
    def __init__(self,fh,col_names:'list[str]',dtype:Type,buf_sz:int=1024):
        super().__init__(fh,col_names,dtype)
        header=_dtype2L(dtype)+('|'.join(self._col_names))
        header+=" "*((4-len(header)%4)%4)
        header=header.encode()
        self._fh.write(struct.pack("<I",len(header)))
        self._fh.write(header)
        self._buf=[]
        self._buf_sz=buf_sz
        self._dcnt=0
    
    def __wbuf(self):
        self._fh.write(np.stack(self._buf,dtype=self._dtype).tobytes())
        self._buf=[]

    def write(self,data:list):
        self._buf.append(data)
        self._dcnt+=1
        if len(data)>=self._buf_sz: self.__wbuf()
    
    def write_all(self, data: np.ndarray):
        if data.dtype!=self._dtype: data.astype(self._dtype)
        self._fh.write(data.tobytes())

    def close(self):
        if len(self._buf)>0: self.__wbuf()
        self._fh.close()

class SdtTableWriter(BinTableWriter):
    '''SDT数据表写入器'''
    def __init__(self,fname:str,col_names:'list[str]',dtype:Type,buf_sz:int=1024):
        '''
        初始化
            fname: 文件名
            col_names: 列名
            dtype: 数据类型, 可以是np.int32或np.float32
            buf_sz: 缓冲区大小, 默认为1024
        '''
        super().__init__(open(fname,"wb"),col_names,dtype,buf_sz)

class SdtGzTableWriter(BinTableWriter):
    '''SDT.GZ数据表写入器'''
    def __init__(self,fname:str,col_names:'list[str]',dtype:Type,buf_sz:int=1024):
        '''
        初始化
            fname: 文件名
            col_names: 列名
            dtype: 数据类型, 可以是np.int32或np.float32
            buf_sz: 缓冲区大小, 默认为1024
        '''
        super().__init__(gzip.open(fname,"wb"),col_names,dtype,buf_sz)

class TableReader(metaclass = ABCMeta):
    '''数据表读取器(抽象类)'''
    @abstractmethod
    def __init__(self,col_names:'list[str]',dtype:Type)->None:
        _dtypechk(dtype)
        self._col_names:'list[str]'=col_names
        self._col_cnt=len(self._col_names)
        self._cmap = {cn:i for i,cn in enumerate(self._col_names)}
        self._dtype:Type=dtype
    @property
    def head(self)->'list[str]': 
        '''表头'''
        return self._col_names
    @property
    def dtype(self)->Type: 
        '''数据类型, 可以是np.int32或np.float32'''
        return self._dtype
    @abstractmethod
    def read(self,cnt:int)->np.ndarray: '''从当前位置开始, 读取1行内容'''
    @abstractmethod
    def read_all(self)->np.ndarray: '''从头开始, 读取所有内容'''
    @abstractmethod
    def close(self)->None: '''关闭TableReader'''

class FileTableReader(TableReader):
    '''文件数据表读取器(抽象类)'''
    @abstractmethod
    def __init__(self,f:IO,col_names:'list[str]',dtype:Type)->None:
        super().__init__(col_names,dtype)
        self._fh:IO=f
    def close(self)->None:
        self._fh.close()
    
class MemoryTableReader(TableReader):
    '''内存数据表读取器'''
    _data:np.ndarray
    def __init__(self,col_names:'list[str]',data:np.ndarray):
        '''
        初始化
            col_names: 列名
            data: 数据
        '''
        super().__init__(col_names,data.dtype)
        self._data=data
        self.__pos = 0

    def read(self,cnt:int)->np.ndarray:
        assert cnt > 0, "读取行数必须大于0"
        ed = cnt + self.__pos
        if ed > self._data.shape[0]: ed = self._data.shape[0]
        return self._data[self.__pos:ed]
    
    def read_all(self)->np.ndarray:
        return self._data
    
    def close(self): pass
    
class BinTableReader(FileTableReader):
    '''二进制数据表读取器(抽象类)'''
    _fh:BinaryIO
    @abstractmethod
    def __init__(self,fname:str,openFunc,allowNegativeSeek:bool=False)->None:
        self.__fn=fname
        self._openF=openFunc
        fh:BinaryIO=self._openF(self.__fn,"rb")
        hlen=struct.unpack("<I",fh.read(4))[0]
        header=fh.read(hlen).decode()
        super().__init__(fh,header[1:].strip().split('|'),_L2dtype(header[0]))
        self._dstart=hlen+4
        self._itmsz=self._col_cnt*4
        self._neg=allowNegativeSeek

    def seek(self,row:int,col:int=0)->int:
        '''定位到第row行的第col个数据, row和col均从0开始编号'''
        dst=self._dstart+self._itmsz*row+4*col
        if self._neg or self._fh.tell()<=dst:
            return self._fh.seek(dst)
        else:
            self._fh.close()
            self._fh=self._openF(self.__fn,"rb")
            return self._fh.seek(dst)

    def read(self,cnt:int)->Optional[np.ndarray]:
        data=self._fh.read(self._itmsz*cnt)
        if data==b'': return None
        return np.frombuffer(data,self._dtype).reshape(-1,self._col_cnt)
    
    def read_all(self)->np.ndarray:
        self.seek(0,0)
        return np.frombuffer(self._fh.read(),self._dtype).reshape(-1,self._col_cnt)

    def read_col(self,col_id:Union[int,str])->np.ndarray:
        '''读取col_id列. col_id可以是下标, 也可以是列名'''
        if isinstance(col_id,str): col_id=self._cmap[col_id]
        i=0; dat=[]
        while True:
            self.seek(i,col_id)
            d=self._fh.read(4)
            if d==b'': break
            dat.append(d)
            i+=1
        return np.frombuffer(b''.join(dat),dtype=self._dtype)

    def read_at(self,start:int,cnt:int)->Optional[np.ndarray]:
        '''读取range(start,start+cnt)范围的行'''
        self.seek(start)
        return self.read(cnt)

class SdtTableReader(BinTableReader):
    '''SDT表格读取器'''
    def __init__(self,fname:str):
        '''
        初始化
            fname: 文件名
        '''
        super().__init__(fname,open,True)

class SdtGzTableReader(BinTableReader):
    '''SDT.GZ表格读取器'''
    def __init__(self,fname:str):
        '''
        初始化
            fname: 文件名
        '''
        super().__init__(fname,gzip.open,False)
    
class CsvTableReader(FileTableReader):
    '''CSV表格读取器'''
    _fh:TextIO
    def __init__(self,fname:str,dtype:Type)->None:
        '''
        初始化
            fname: 文件名
            dtype: 数据类型, 可以是np.int32或np.float32
        '''
        self.__fn=fname
        fh=open(fname,"r")
        super().__init__(fh,fh.readline().strip().split(","),dtype)

    def __parseline(self,ln:str)->np.ndarray:
        strs=map(lambda x: x.strip(), ln.split(','))
        if self._dtype==np.int32:
            return np.array(list(map(int,strs)),dtype=np.int32)
        else:
            return np.array(list(map(float,strs)),dtype=np.float32)
    
    def __read1(self)->Optional[np.ndarray]:
        '''从当前位置开始, 读取1行'''
        ln = self._fh.readline().strip()
        if ln == "": return None
        return self.__parseline(ln)
    
    def read(self,cnt:int)->Optional[np.ndarray]:
        if cnt == 1: return self.__read1()
        ret = []
        for _ in range(cnt):
            dat = self.__read1()
            if dat is None: break
            ret.append(dat)
        if len(ret) == 0: return None
        return np.stack(ret)
    
    def read_all(self)->np.ndarray:
        self._fh.close()
        self._fh = open(self.__fn,"r")
        self._fh.readline()
        return np.stack([self.__parseline(x) for x in self._fh.readlines()])

def createTableReader(fname:str,dtype:Optional[Type]=None)->TableReader:
    '''从文件名创建TableReader, 对于CSV文件需要指定dtype'''
    fn=fname.lower()
    if fn.endswith(".csv"):
        assert dtype is not None
        return CsvTableReader(fname,dtype)
    elif fn.endswith(".sdt"):
        return SdtTableReader(fname)
    elif fn.endswith(".sdt.gz"):
        return SdtGzTableReader(fname)
    else:
        raise ValueError("不支持的文件类型")

def createTableWriter(fname:str,cols:'list[str]',dtype:Type)->TableWriter:
    '''从文件名创建TableWriter'''
    fn=fname.lower()
    if fn.endswith(".csv"):
        return CsvTableWriter(fname,cols,dtype)
    elif fn.endswith(".sdt"):
        return SdtTableWriter(fname,cols,dtype)
    elif fn.endswith(".sdt.gz"):
        return SdtGzTableWriter(fname,cols,dtype)
    elif fn.endswith("<mem>"):
        return MemoryTableWriter(cols,dtype)
    else:
        raise ValueError("不支持的文件类型")

def _convbinfile(r:Union[BinaryIO,gzip.GzipFile],w:Union[BinaryIO,gzip.GzipFile],bufsz:int=1024*1024*64):
    while True:
        data=r.read(bufsz)
        if data==b'': break
        w.write(data)
    r.close()
    w.close()

def convertTableFile(rfile:str,wfile:str,dtype:Optional[Type]=None,bufsz:int=1024)->None:
    '''将一种文件类型的Table转化成另一文件类型的Table, 如果输入文件为CSV文件, 还需要指定dtype'''
    if rfile.lower().endswith(".sdt.gz") and wfile.lower().endswith(".sdt"):
        _convbinfile(gzip.open(rfile,"rb"),open(wfile,"wb"))
        return
    elif rfile.lower().endswith(".gz") and wfile.lower().endswith(".sdt.gz"):
        _convbinfile(open(rfile,"rb"),gzip.open(wfile,"wb"))
        return
    r=createTableReader(rfile,dtype)
    w=createTableWriter(wfile,r.head,r.dtype)
    while True:
        data=r.read(bufsz)
        if data is None: break
        w.write_all(data)
    r.close()
    w.close()

class ReadOnlyTable(Generic[_Table_DType]): 
    '''
    **只读**数据表, 表中所有数据必须是同一类型, 必须是32位int或float格式.
    某一行的内容直接用下标获取; 某一列的内容用col方法获取.
    由于是只读列表，因此必须从文件加载. 支持的文件类型包含csv, sdt和sdt.gz.
    '''
    _d:'Optional[np.ndarray[tuple[int,int],np.dtype[_Table_DType]]]'
    _btr:TableReader

    @overload
    def __init__(self,source:MemoryTableReader):
        '''使用MemoryTableReader初始化'''
    @overload
    def __init__(self,source:MemoryTableWriter): 
        '''使用MemoryTableWriter初始化'''
    @overload
    def __init__(self,source:str,dtype:Optional[Table_DType]=None,preload:bool=False):
        '''
        初始化
            fname: 数据表文件名, 仅支持csv, sdt和sdt.gz文件.
            dtype: 表格数据类型, 只有csv文件需要提供此项.
            preload: 是否在初始化时预加载全部数据.
        
        注意: 
            预加载使得初始化速度大幅降低, 但大幅提升了运行时性能.
            csv强制开启预加载功能, sdt和sdt.gz自选(推荐sdt.gz开启, sdt关闭).
            如果数据过大导致内存不足, 请勿使用预加载功能.
        '''
    
    def __init__(self,source:Union[str,MemoryTableWriter,MemoryTableReader],dtype:Optional[Table_DType]=None,preload:bool=False):
        if isinstance(source,str):
            self._btr=createTableReader(source,dtype)
            fn=source.lower()
            if preload or fn.lower().endswith(".csv"):
                self._d=self._btr.read_all()
            else:
                self._d=None
        elif isinstance(source,MemoryTableReader):
            self._btr=source
            self._d=source._data
        elif isinstance(source,MemoryTableWriter):
            self._btr=MemoryTableReader(source._col_names,source._data)
            self._d=source._data

    @property
    def head(self)->'list[str]': 
        '''表头'''
        return self._btr._col_names

    @property
    def dtype(self)->Table_DType: 
        '''
        表中数据类型, 可取np.int32或np.float32
        '''
        return self._btr._dtype
    
    @property
    def data(self)->'np.ndarray[(int,int),np.dtype[_Table_DType]]':
        '''
        表格数据. 如果没有预加载全部数据, 则调用此项时会加载所有数据.
        '''
        if self._d is None: self._d=self._btr.read_all()
        return self._d
    
    def force_load_all(self): self._d=self._btr.read_all()
    
    @overload
    def col(self,c:str): '''获取列名为c的列'''
    @overload
    def col(self,c:int): '''获取第c列'''
    @overload
    def col(self,c:Iterable[Union[str,int]]): '''获取多列'''

    def col(self,c:Union[Iterable[Union[str,int]],str,int])->'np.ndarray[int,np.dtype[_Table_DType]]':
        if isinstance(c,int) or isinstance(c,str):
            if self._d is None:
                assert isinstance(self._btr,BinTableReader)
                return self._btr.read_col(c)
            else:
                if isinstance(c,str): c=self._btr._cmap[c]
                return self._d[:,c]
        elif isinstance(c,Iterable):
            nc:list[int]=[self._btr._cmap[x] if isinstance(x,str) else x for x in c]
            return self.data[:,nc]
        else:
            raise TypeError("不支持的索引类型")
            
    def row(self,row_id:int)->'Optional[np.ndarray[int,np.dtype[_Table_DType]]]':
        '''获取一行数据'''
        if self._d is not None: return self._d[row_id]
        assert isinstance(self._btr,BinTableReader)
        return self._btr.read_at(row_id,1)
    
    def at(self,col_name:str,row_id:int)->_Table_DType:
        '''获取列名为col_name,行为row_id的数据'''
        return self.data[self._btr._cmap[col_name],row_id]
    
    def __getitem__(self,indices)->'Union[np.ndarray[tuple[int,...],np.dtype[_Table_DType]],_Table_DType]':
        '''仅限数字下标'''
        return self.data[indices]
    
    def save(self,path:str):
        '''
        保存到.csv或.bin.gz文件
            path: 文件路径
        '''
        if self._d is None: self._d=self._btr.read_all()
        fn=path.lower()
        if fn.endswith(".csv"):
            CsvTableWriter(path,self.head,self.dtype).write_all(self._d)
        elif fn.endswith(".sdt"):
            SdtTableWriter(path,self.head,self.dtype).write_all(self._d)
        elif fn.endswith(".sdt.gz"):
            SdtGzTableWriter(path,self.head,self.dtype).write_all(self._d)
        else:
            raise ValueError("不支持的文件名")
        
    def __str__(self):
        return ','.join(self.head)+"\n"+super().__str__()