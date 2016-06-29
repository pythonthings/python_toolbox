# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `CachedType` metaclass.

See its documentation for more details.
'''

import threading
import contextlib

from python_toolbox.sleek_reffing import SleekCallArgs

from .cached_property import CachedProperty


class InConstructionMarker:
    def __init__(self):
        self.lock = threading.Lock()
        

class SelfPlaceholder:
    '''Placeholder for `self` when storing call-args.''' 


class CachedType(type):
    '''
    A metaclass for sharing instances.
        
    For example, if you have a class like this:
    
        class Grokker(object, metaclass=caching.CachedType):
            def __init__(self, a, b=2):
                self.a = a
                self.b = b
                
    Then all the following calls would result in just one instance:
    
        Grokker(1) is Grokker(1, 2) is Grokker(b=2, a=1) is Grokker(1, **{})
    
    This metaclass understands keyword arguments.
    
    All the arguments are sleekreffed to prevent memory leaks. Sleekref is a
    variation of weakref. Sleekref is when you try to weakref an object, but if
    it's non-weakreffable, like a `list` or a `dict`, you maintain a normal,
    strong reference to it. (See documentation of
    `python_toolbox.sleek_reffing` for more details.) Thanks to sleekreffing
    you can avoid memory leaks when using weakreffable arguments, but if you
    ever want to use non-weakreffable arguments you are still able to.
    (Assuming you don't mind the memory leaks.)
    '''
    
    def __new__(mcls, *args, **kwargs):
        cls = super().__new__(mcls, *args, **kwargs)
        cls.__cache = {}
        cls.__quick_lock = threading.Lock()
        cls.__construction_lock = threading.Lock()
        return cls

    
    def __call__(cls, *args, **kwargs):
        sleek_call_args = SleekCallArgs(
            cls.__cache,
            cls.__init__,
            *((SelfPlaceholder,) + args),
            **kwargs
        )
        
        while True:
            cls.__quick_lock.acquire()
            try:
                cached_value = cls.__cache[sleek_call_args]
            except KeyError:
                cls.__cache[sleek_call_args] = in_construction_marker = \
                                                         InConstructionMarker()
                cls.__quick_lock.release()
                with in_construction_marker.lock:
                    cls.__cache[sleek_call_args] = new_instance = \
                                              super().__call__(*args, **kwargs)
                    return new_instance
            else:
                if isinstance(cached_value, InConstructionMarker):
                    in_construction_marker = cached_value
                    with in_construction_marker.lock:
                        continue
                                                  
                return value



