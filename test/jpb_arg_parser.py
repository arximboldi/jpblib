# -*- coding: utf-8 -*-
#
#  File:       jpb_arg_parser.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 21:01:38 jbo>
#

#
#  Copyright (C) 2009, 2012 Juan Pedro Bolívar Puente
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

import unittest

from util import *
from jpb.arg_parser import *


class TestArgParser (unittest.TestCase):

    def setUp (self):
        self._op_a = OptionWith (int, -1)
        self._op_b = OptionFlag ()
        self._op_c = OptionFunc (mock_raiser)
        self._op_d = OptionWith (float, -1.0)

        self._args = ArgParser ()
        self._args.add ('a', 'alpha', self._op_a)
        self._args.add ('b', 'beta', self._op_b)
        self._args.add ('c', 'gamma', self._op_c)
        self._args.add ('d', 'delta', self._op_d)

    def tearDown (self):
        self._args = None

    def test_unkown_args (self):
        self.assertRaises (MockError, self._args.parse, ['test', '-c'])
        self.assertRaises (UnknownArgError, self._args.parse, ['test', '-x'])

    def test_int_option_and_multi_flag_argument (self):
        self._args.parse (['test', '-ab', '10'])
        self.assertEqual (self._op_a.value, 10)
        self.assertEqual (self._op_b.value, True)

    def test_corner_option (self):
        self._args.parse (['test', '--alpha'])
        self.assertEqual (self._op_a.value, -1)
        self.assertEqual (self._op_b.value, False)

    def test_float_option (self):
        self._args.parse (['test', '-ad', '2', '2.5'])
        self.assertEqual (self._op_a.value, 2)
        self.assertEqual (self._op_d.value, 2.5)
