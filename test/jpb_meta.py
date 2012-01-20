# -*- coding: utf-8 -*-
#
#  File:       jpb_meta.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:57:54 jbo>
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

import unittest
from jpb.meta import *

class TestMeta (unittest.TestCase):

    class Tester_1:
        def __init__ (self):
            self.count = 0

    class Tester_2 (Tester_1):
        def method (self):
            return "ok"

    def extension (self):
        self.count += 1

    extend_methods (Tester_1, extension = extension)
    extend_methods (Tester_2, method = extension)

    def test_addition (self):
        a = TestMeta.Tester_1 ()
        a.extension ()
        self.assertEqual (a.count, 1)

    def test_replace (self):
        a = TestMeta.Tester_2 ()
        r = a.method ()
        self.assertEqual (r, "ok")
        self.assertEqual (a.count, 1)

