# -*- coding: utf-8 -*-
#
#  File:       jpb_observer_old.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:57:32 jbo>
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
from jpb.observer_old import *

TEST_SIGNALS = ["sig_one", "sig_two", "sig_three"]

class SubjectTester: pass
class ListenerTester: pass
subject (SubjectTester, TEST_SIGNALS)
listener (ListenerTester, TEST_SIGNALS, "ok")

CleverSubjectTester, CleverListenerTester = make_clever_observer (
    TEST_SIGNALS, defret = "ok")

class LightSubjectTester: pass
class LightListenerTester: pass
light_observer (LightSubjectTester, LightListenerTester, TEST_SIGNALS)

class TestListenerOld (unittest.TestCase):

    KLASS = ListenerTester

    def setUp (self):
        self.listener = self.KLASS ()

    def tearDown (self):
        del self.listener

    def test_listener_methods (self):
        self.assertEqual (hasattr (self.listener, 'handle_sig_one'), True)
        self.assertEqual (hasattr (self.listener, 'handle_sig_two'), True)
        self.assertEqual (hasattr (self.listener, 'handle_sig_three'), True)

    def test_listener_returns (self):
        self.assertEqual (self.listener.handle_sig_one (), "ok")
        self.assertEqual (self.listener.handle_sig_two (), "ok")
        self.assertEqual (self.listener.handle_sig_three (), "ok")

class TestSubjectOld (unittest.TestCase):

    KLASS = SubjectTester

    def setUp (self):
        self.observer = self.KLASS ()

    def tearDown (self):
        del self.observer

    def test_observer_signals (self):
        self.assertEqual (hasattr (self.observer, 'on_sig_one'), True)
        self.assertEqual (hasattr (self.observer, 'on_sig_two'), True)
        self.assertEqual (hasattr (self.observer, 'on_sig_three'), True)
        self.assertEqual (hasattr (self.observer, 'add_listener'), True)
        self.assertEqual (hasattr (self.observer, 'del_listener'), True)
        self.assertEqual (hasattr (self.observer, 'clear'), True)


class TestCleverListenerOld (TestListenerOld):

    KLASS = CleverListenerTester


class TestCleverSubjectOld (TestSubjectOld):

    KLASS = CleverSubjectTester


class TestObserverOld (unittest.TestCase):

    LISTENER_KLASS = ListenerTester
    SUBJECT_KLASS = SubjectTester

    class Counter:
        def __init__ (self, val = 0):
            self.val = 0
        def increase (self):
            self.val += 1
        def decrease (self):
            self.val -= 1

    def setUp (self):
        self.lst = self.LISTENER_KLASS ()
        self.sub = self.SUBJECT_KLASS ()

    def tearDown (self):
        del self.sub
        del self.lst

    def test_add_listener (self):
        self.sub.add_listener (self.lst)
        self.assertEqual (self.sub.on_sig_one.count, 1)
        self.assertEqual (self.sub.on_sig_two.count, 1)
        self.assertEqual (self.sub.on_sig_three.count, 1)

    def test_del_listener (self):
        self.test_add_listener ()
        self.sub.del_listener (self.lst)
        self.assertEqual (self.sub.on_sig_one.count, 0)
        self.assertEqual (self.sub.on_sig_two.count, 0)
        self.assertEqual (self.sub.on_sig_three.count, 0)


class TestCleverObserverOld (TestObserverOld):

    LISTENER_KLASS = CleverListenerTester
    SUBJECT_KLASS = CleverSubjectTester

    def test_disconnect_all (self):
        self.sub.add_listener (self.lst)
        self.lst.disconnect ()
        self.assertEqual (self.sub.on_sig_one.count, 0)
        self.assertEqual (self.sub.on_sig_two.count, 0)
        self.assertEqual (self.sub.on_sig_three.count, 0)


class TestLightObserverOld (TestObserverOld):

    class Counter (LightListenerTester):
        def __init__ (self):
            self.value = 0

        def handle_sig_one (self):
            self.value += 1

        def handle_sig_two (self):
            self.value -= 1

    LISTENER_KLASS = Counter
    SUBJECT_KLASS = LightSubjectTester

    def test_add_listener (self):
        self.sub.add_listener (self.lst)
        self.assertEqual (len (self.sub._listeners), 1)

    def test_del_listener (self):
        self.test_add_listener ()
        self.sub.del_listener (self.lst)
        self.assertEqual (len (self.sub._listeners), 0)

    def test_signaling (self):
        self.test_add_listener ()
        self.sub.on_sig_one ()
        self.assertEqual (self.lst.value, 1)
        self.sub.on_sig_two ()
        self.assertEqual (self.lst.value, 0)
