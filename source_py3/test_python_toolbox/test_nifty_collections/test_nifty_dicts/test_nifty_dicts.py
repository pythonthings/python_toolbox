# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections.abc

from python_toolbox.third_party import unittest2

import nose

from python_toolbox import cute_iter_tools
from python_toolbox import cute_testing

from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import (
    DoubleDict, FrozenDict, OrderedDict,
    DoubleFrozenDict, DoubleOrderedDict,
    FrozenOrderedDict, DoubleFrozenOrderedDict
)

from .abstract_two_test_cases import * 


class DoubleDictTestCase(_AbstractDoubleNotFrozenDictTestCase,
                         _AbstractDoubleNotOrderedDictTestCase,
                         _AbstractNotFrozenNotOrderedDictTestCase):
    d_type = DoubleDict


class FrozenDictTestCase(_AbstractFrozenNotDoubleDictTestCase,
                         _AbstractFrozenNotOrderedDictTestCase,
                         _AbstractNotDoubleNotOrderedDictTestCase):
    d_type = FrozenDict

        
class OrderedDictTestCase(_AbstractOrderedNotDoubleDictTestCase,
                          _AbstractOrderedNotFrozenDictTestCase,
                          _AbstractNotDoubleNotFrozenDictTestCase):
    d_type = OrderedDict
        
        
class DoubleFrozenDictTestCase(_AbstractDoubleFrozenDictTestCase,
                               _AbstractDoubleNotOrderedDictTestCase,
                               _AbstractFrozenNotOrderedDictTestCase):
    d_type = DoubleFrozenDict
        
        
class DoubleOrderedDictTestCase(_AbstractDoubleFrozenDictTestCase,
                               _AbstractDoubleNotOrderedDictTestCase,
                               _AbstractFrozenNotOrderedDictTestCase):
    d_type = DoubleOrderedDict
        