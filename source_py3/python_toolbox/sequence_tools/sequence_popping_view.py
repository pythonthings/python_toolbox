# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import abc
import bisect
import builtins
import types
import collections
import numbers
import itertools

from python_toolbox import caching

from .misc import CuteSequence

infinity = float('inf')
infinities = (infinity, -infinity)


class SequencePoppingView(CuteSequence):
    def __init__(self, sequence, popped_indices=None):
        self.sequence = sequence
        if popped_indices is not None:
            self.popped_indices = popped_indices

    @caching.CachedProperty
    def popped_indices(self):
        from python_toolbox import nifty_collections
        return nifty_collections.OrderedSet()
    
    def _get_sequence_index(self, index):
        current_base = 0
        current_goal = index
        while current_base != current_goal:
            n_popped_items_in_range = (
                bisect.bisect(self.popped_indices, current_goal) -
                        len(bisect.bisect_left(self.popped_indices, current_base)))
            current_base, current_goal = (current_goal, current_goal +
                                                       n_popped_items_in_range)
        assert current_goal not in self.popped_indices
        return current_goal

    def __getitem__(self, index):
        return self.sequence[self._get_sequence_index(index)]

    def __iter__(self):
        for i in itertools.count():
            if i not in self.popped_indices:
                try:
                    yield self.sequence[i]
                except IndexError:
                    raise StopIteration
                
    __contains__ = lambda self: any(item == value for value in self)

    # Can't define `index` which uses the wrapped sequence's `index` because
    # `index` stops on the first occurrence, and if our first occurrence was
    # removed, we'd need to search for the next one.

    # def _nopity_nope_nope(self, item):
        # raise TypeError("Can't add stuff to a `%s`" % type(self).__name__)
    # extend = insert = append = _nopity_nope_nope
    
    clear = lambda self: self.popped_indices.__ior__(range(len(self.sequence)))
    copy = lambda self: type(self)(self.sequence,
                                   popped_indices=self.popped_indices)
    __len__ = lambda self: len(self.sequence) - len(self.popped_indices)
    
    # These are the money methods right here:
    def pop(self, i):
        sequence_index = self._get_sequence_index(i)
        self.popped_indices.add(sequence_index)
        return self.sequence[sequence_index]
    remove = lambda self, item: \
                             self.popped_indices.add(self.sequence.index(item))
    
    
    
    