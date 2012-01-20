# -*- coding: utf-8 -*-
#
#  File:       jpb_sender.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:57:26 jbo>
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
from jpb.sender import *

class OneReceiver (Receiver):

    def on_something (self):
        self.value = 'something'

    def on_somewhat (self, param):
        self.value = param

class TestSender (unittest.TestCase):

    def setUp (self):
        self.one = OneReceiver ()
        self.two = OneReceiver ()
        self.sender = Sender ()

    def test_add_del (self):
        self.assertEqual (self.sender.count, 0)
        self.sender.connect (self.one)
        self.assertEqual (self.sender.count, 1)
        self.sender.connect (self.two)
        self.assertEqual (self.sender.count, 2)
        self.sender.connect (self.two)
        self.assertEqual (self.sender.count, 2)

        self.sender.disconnect (self.two)
        self.assertEqual (self.sender.count, 1)
        self.assertRaises (ValueError, self.sender.disconnect, self.two)
        self.sender.disconnect (self.one)
        self.assertEqual (self.sender.count, 0)

    def test_sending (self):
        self.sender.connect (self.one)
        self.sender.connect (self.two)

        self.sender.send ('on_something')
        self.assertEqual (self.one.value, 'something')
        self.assertEqual (self.two.value, 'something')

        self.sender.send ('on_somewhat', 'what')
        self.assertEqual (self.one.value, 'what')
        self.assertEqual (self.two.value, 'what')

        self.sender.disconnect (self.one)
        self.sender.send ('on_something')
        self.assertEqual (self.one.value, 'what')
        self.assertEqual (self.two.value, 'something')



