# -*- coding: utf-8 -*-
#
#  File:       jpb_event.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:44:14 jbo>
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
from jpb.event import *
from jpb.sender import *

class TestEventManager (unittest.TestCase):

    def test_add_del (self):
        e = EventManager ()
        x = Receiver ()
        y = Receiver ()
        e.connect (x)
        self.assertEqual (e.count, 1)
        e.connect (y)
        self.assertEqual (e.count, 2)
        e.disconnect (x)
        self.assertEqual (e.count, 1)
        e.disconnect (y)
        self.assertEqual (e.count, 0)
        self.assertRaises (ValueError, e.disconnect, x)

    def test_forward_and_quiet (self):
        class DummyForwarder (Receiver):
            def __init__ (self):
                self.last = ''
            def receive (self, name, *a, **k):
                self.last = name

        fw = DummyForwarder ()
        mgr = EventManager ()
        mgr.connect (fw)

        a = mgr.event ('a').notify ()
        self.assertEqual (fw.last, 'a')

        b = mgr.notify ('b')
        self.assertEqual (fw.last, 'b')

        mgr.quiet = True
        mgr.notify ('a')
        self.assertEqual (fw.last, 'b')

    def test_notify_and_quiet (self):
        l = []
        def accum (x):
            l.append (x)

        mgr = EventManager ()
        mgr.event ('ac').connect (accum)

        mgr.notify ('ac', 1)
        self.assertEqual (l, [1])

        mgr.event ('ac') (2)
        self.assertEqual (l, [1, 2])

        mgr.quiet = True

        mgr.notify ('ac', 3)
        self.assertEqual (l, [1, 2])

        mgr.event ('ac') (3)
        self.assertEqual (l, [1, 2, 3])
