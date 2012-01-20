# -*- coding: utf-8 -*-
#
#  File:       jpb_signal.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:47:48 jbo>
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
from jpb.signal import *
from jpb.meta import mixin


CleverSlot = mixin (Trackable, Slot)

class TestSignalSlot (unittest.TestCase):

    class Counter (object):
        def __init__ (self, val = 0):
            super (TestSignalSlot.Counter, self).__init__ ()
            self.val = val
        def increase (self):
            self.val += 1
            return self.val
        def decrease (self):
            self.val -= 1
            return self.val

    def test_signal (self):
        sig = Signal ()
        cnt = TestSignalSlot.Counter ()

        slt_a = sig.connect (cnt.increase)
        sig += cnt.decrease
        self.assertEquals (sig.count, 2)

        sig.notify ()
        self.assertEquals (cnt.val, 0)
        self.assertEquals (sig.fold (lambda x, y: x+y), 1)
        self.assertEquals (sig.fold (lambda x, y: x+y, 1), 2)

        sig.disconnect (cnt.decrease)
        self.assertEquals (sig.count, 1)

        sig.notify ()
        self.assertEquals (cnt.val, 1)

        sig.disconnect (slt_a)
        self.assertEquals (sig.count, 0)

    def test_cleverness (self):

        sig_a = Signal ()
        sig_b = Signal ()
        cnt = TestSignalSlot.Counter ()
        slt = CleverSlot (cnt.increase)

        sig_a += slt
        sig_a += slt
        sig_b += slt
        self.assertEquals (slt.source_count, 2)

        sig_a ()
        self.assertEquals (cnt.val, 1)
        sig_b ()
        self.assertEquals (cnt.val, 2)

        slt.disconnect_sources ()
        self.assertEquals (slt.source_count, 0)
        self.assertEquals (sig_a.count, 0)
        self.assertEquals (sig_b.count, 0)

    def test_decorator (self):
        class Decorated:
            @slot
            def function (self):
                return "called"

        d = Decorated ()
        self.assertEquals (d.function (), "called")
        self.assertTrue (isinstance (d.function, Trackable))
        self.assertEquals (d.function, d.function)

    def test_decorator_slotable (self):

        class Decorated (Tracker):
            @slot
            def one (self):
                return "one"
            @slot
            def two (self):
                return "two"

        d = Decorated ()
        s = Signal ()

        s += d.one
        self.assertEqual (d._trackables, [d.one])
        self.assertEqual (s.count, 1)

        s += d.two
        self.assertEqual (d._trackables, [d.one, d.two])
        self.assertEqual (s.count, 2)

        s += d.two
        self.assertEqual (d._trackables, [d.one, d.two])
        self.assertEqual (s.count, 2)

        d.disconnect_all ()
        self.assertEqual (s.count, 0)

    def test_decorator_signal (self):

        class Decorated (object):
            def __init__ (self):
                self.value = 1
            @signal
            def after (self, param):
                self.value = self.value + param
                return self.value
            @signal_before
            def before (self, param):
                self.value = self.value - param
                return self.value

        d = Decorated ()

        d.after += lambda _: self.assertEquals (d.value, 2)
        d.before += lambda _: self.assertEquals (d.value, 2)

        res = d.after (1)
        self.assertEquals (res, 2)
        res = d.before (1)
        self.assertEquals (res, 1)

    def test_auto_signaler_set (self):
        self._test_auto_signaler (AutoSignalSender)

    def test_auto_forward_get (self):
        self._test_auto_signaler (AutoSignalSenderGet)

    def _test_auto_signaler (self, base_class):

        class Tester (Receiver, base_class):
            def __init__ (self):
                base_class.__init__ (self)
                self.value = 0
                self.signal = Signal ()
                self.signal += self.non_decorated

            @signal
            def decorated (self, param):
                self.value += param

            def non_decorated (self, param):
                self.value += -param

        source = Tester ()
        dest = Tester ()

        source.connect (dest)
        source.signal (1)
        self.assertEqual (dest.value, -1)

        source.decorated (2)
        self.assertEqual (dest.value, 1)

    def test_weak (self):
        t = [0]
        class Tester (object):
            def method (self):
                t [0] += 1
        s = Signal ()
        o = Tester ()
        s += WeakSlot (o, Tester.method)

        self.assertEqual (s.count, 1)
        self.assertEqual (t [0], 0)
        s ()
        self.assertEqual (t [0], 1)
        s ()
        self.assertEqual (t [0], 2)
        del o
        s ()
        self.assertEqual (t [0], 2)
        self.assertEqual (s.count, 0)



