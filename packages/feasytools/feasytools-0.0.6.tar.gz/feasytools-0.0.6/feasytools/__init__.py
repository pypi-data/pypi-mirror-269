from .tfunc import *
from .argchk import *
from .table import *
from .pq import *
from .rangelist import *

def time2str(tspan:float):
    tspan=round(tspan)
    s=tspan%60
    m=tspan//60%60
    h=tspan//3600
    return f"{h:02}:{m:02}:{s:02}"