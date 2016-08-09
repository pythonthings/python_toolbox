# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import operator
import functools
import itertools

from python_toolbox import comparison_tools

from python_toolbox.nifty_collections.abstract import (Ordered,
                                                       DefinitelyUnordered)
from .ordered_dict import OrderedDict


class _AbstractMappingDelegator(collections.abc.Mapping):
    def __init__(self, *args, **kwargs):
        self._dict = self._dict_type(*args, **kwargs)

    __getitem__ = lambda self, key: self._dict[key]
    __len__ = lambda self: len(self._dict)
    __iter__ = lambda self: iter(self._dict)
        
    def copy(self, *args, **kwargs):
        base_dict = self._dict.copy()
        base_dict.update(*args, **kwargs)
        return type(self)(base_dict)

    __repr__ = lambda self: '%s(%s)' % (type(self).__name__,
                                        repr(self._dict) if self._dict else '')
    __reduce__ = lambda self: (self.__class__ , (self._dict,))


class _AbstractMutableMappingDelegator(_AbstractMappingDelegator,
                                       collections.abc.MutableMapping):
    def __setitem__(self, key, value):
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]


class _AbstractFrozenDict(_AbstractMappingDelegator):
    _hash = None # Overridden by instance when calculating hash.
    
    def __hash__(self):
        if self._hash is None:
            self._hash = functools.reduce(
                operator.xor,
                map(
                    hash,
                    itertools.chain(
                        (h for h in self.items()),
                        (type(self), len(self))
                    )
                ),
                0
            )

        return self._hash


class _AbstractDoubleSidedDict(_AbstractMappingDelegator):
    def __init__(self, *args, **kwargs):
        if hasattr(self, '_dict'):
            assert self.inverse.inverse is self
        else:
            self._dict = self._dict_type(*args, **kwargs)
            internal_inverse = self._dict_type((value, key) for key, value
                                               in self._dict.items())
            if len(internal_inverse) <= len(self._dict):
                raise Exception("There's a repeating value given to the "
                                "double-sided dict, that is not allowed.") # blocktodo test
            assert len(internal_inverse) == len(self._dict)
            self.inverse = type(self).__new__()
            self.inverse._dict = internal_inverse
            self.inverse.inverse = self
            self.inverse.__init__()
            

class _AbstractMutableDoubleSidedDict(_AbstractDoubleSidedDict,
                                      collections.abc.MutableMapping):
    
    def _assert_valid(self):
        assert len(self._dict) == len(self.inverse._dict)
    
    def __setitem__(self, key, value):
        self._assert_valid()
        try:
            existing_key = self.inverse[value]
        except KeyError:
            pass
        else:
            raise Exception(
                "Can't add key %s with value %s because there is already a "
                "key %s with the same value." % (key, value,
                                                 self.inverse[value]) # blocktodo test
            )
        
        try:
            existing_value = self[key]
        except KeyError:
            got_existing_value = True
        else:
            got_existing_value = False
        
        self._dict[key] = value
        self.inverse._dict[value] = key
        if got_existing_value:
            del self.inverse._dict[existing_value]
        self._assert_valid()
        

    def __delitem__(self, key):
        value = self[key] # Propagating possible KeyError # blocktodo test
        self._assert_valid()
        del self._dict[key]
        del self.inverse._dict[value]
        self._assert_valid()
        

    def clear(self):
        'D.clear() -> None.  Remove all items from D.'
        self._assert_valid()
        self._dict.clear()
        self.inverse._dict.clear()
        self._assert_valid()
        

class _UnorderedDictDelegator(DefinitelyUnordered,
                              _AbstractMappingDelegator):
        
    _dict_type = dict
        
class _OrderedDictDelegator(Ordered, _AbstractMappingDelegator):
        
    _dict_type = OrderedDict
        