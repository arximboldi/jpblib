# -*- coding: utf-8 -*-
#
#  File:       jpb_collab.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       Fri Jan 20 16:12:23 2012
#  Time-stamp: <2012-01-20 17:38:21 jbo>
#

#
#  Copyright (C) 2012 Juan Pedro Bolívar Puente
#
#  This file is part of jpblib.
#
#  jpblib is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  jpblib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Tests for jpb.collab
"""

from jpb import collab
import unittest

_global_call_trace = []

def _reset_call_trace():
    global _global_call_trace
    _global_call_trace = []

def _trace_collab_call(method):
    global _global_call_trace
    _global_call_trace.append(method)


@collab.has_constructor
class _A(object):
    def __init__(self):
        _trace_collab_call(_A.__init__)

@collab.has_constructor
class _B(_A):
    def __init__(self, b_param = 'b_param'):
        self._b_param = b_param
        _trace_collab_call(_B.__init__)

@collab.has_constructor
class _C(_A):
    def __init__(self):
        _trace_collab_call(_C.__init__)

@collab.has_constructor
class _D(_B, _C):
    def __init__(self, d_param = 'd_param'):
        self._d_param = d_param
        _trace_collab_call(_D.__init__)


class TestCollab(unittest.TestCase):

    def setUp(self):
        _reset_call_trace()

    def test_constructor_parameter_passing(self):
        obj = _D()
        self.assertEqual(obj._b_param, 'b_param')
        self.assertEqual(obj._d_param, 'd_param')
        obj = _D(b_param = 'new_b_param')
        self.assertEqual(obj._b_param, 'new_b_param')
        self.assertEqual(obj._d_param, 'd_param')
        obj = _D(d_param = 'new_d_param')
        self.assertEqual(obj._b_param, 'b_param')
        self.assertEqual(obj._d_param, 'new_d_param')
        obj = _D(d_param = 'new_d_param',
                 b_param = 'new_b_param')
        self.assertEqual(obj._b_param, 'new_b_param')
        self.assertEqual(obj._d_param, 'new_d_param')

    def test_mro_call_order(self):
        for cls in (_D, _C, _B, _A):
            _reset_call_trace()
            cls()
            self._check_trace_calls_with_mro(cls.__init__)

    def _check_trace_calls_with_mro(self, method):
        global _global_call_trace
        cls  = method.__objclass__
        name = method.__name__
        mro  = cls.__mro__[:-1] # discard object
        self.assertEqual(list(mro[::-1]), [m.__objclass__ for m in _global_call_trace])
        for m in _global_call_trace:
            m.__name__ == name
