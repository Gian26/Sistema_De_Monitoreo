__author__ = 'GNC26'
from dajax.core import Dajax

def multiply(request,a,b):
    dajax = Dajax()
    result = int(a) * (b)
    dajax.assign('#result','value',str(result))
    return dajax.json()