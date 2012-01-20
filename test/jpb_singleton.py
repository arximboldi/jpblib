# -*- coding: utf-8 -*-
#
#  File:       jpb_singleton.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:54:50 jbo>
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
from jpb.singleton import *

class TestSingleton (unittest.TestCase):

    class SingletonMock:

        __metaclass__ = Singleton

    def test_singleton (self):
        a = TestSingleton.SingletonMock ()
        b = TestSingleton.SingletonMock ()

        self.assertTrue (a is b)

