# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines the `ContextManagerTypeType` metaclass.

See its documentation for more information.
'''
import collections


class ContextManagerTypeType(type):
    '''Metaclass for `ContextManagerType`. Shouldn't be used directly.'''
    
    def __call__(cls, *args):
        '''
        Create a new `ContextManager`.
        
        This can work in two ways, depending on which arguments are given:
        
         1. The classic `type.__call__` way. If `name, bases, namespace` are
            passed in, `type.__call__` will be used normally.
            
         2. As a decorator for a generator function. For example:
            
                @ContextManagerType
                def MyContextManager():
                    # preparation
                    try:
                        yield
                    finally:
                        pass # cleanup
                        
            What happens here is that the function (in this case
            `MyContextManager`) is passed directly into
            `ContextManagerTypeType.__call__`. So we create a new
            `ContextManager` subclass for it, and use the original generator as
            its `.manage_context` function.
                        
        '''
        if len(args) == 1:
            from .context_manager import ContextManager
            (function,) = args
            assert isinstance(function, collections.Callable)
            name = function.__name__
            bases = (ContextManager,)
            namespace_dict = {
                'manage_context': staticmethod(function),
                '__init__': ContextManager.\
                            _ContextManager__init_lone_manage_context
            }
            return super(ContextManagerTypeType, cls).__call__(
                name,
                bases,
                namespace_dict
            )
            
        else:
            return super(ContextManagerTypeType, cls).__call__(*args)
        