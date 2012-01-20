# -*- coding: utf-8 -*-
#
#  File:       jpb_conf.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 21:19:02 jbo>
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
from jpb.conf import *

class TestConfBackend(unittest.TestCase):

    class MockBackend (object):
        def __init__ (self):
            self.called = None
        def _do_load (self, node, overwrite):
            self.called = "_do_load"
        def _do_save (self, node):
            self.called = "_do_save"
        def _handle_conf_new_node (self, node):
            self.called = "_handle_conf_new_child"
        def _handle_conf_del_node (self, node):
            self.called = "_handle_conf_del_child"
        def _handle_conf_change (self, node):
            self.called = "_handle_conf_change"
        def _handle_conf_nudge (self, node):
            self.called = "_handle_conf_nudge"
        def _attach_on (self, node):
            self.called = "_attach_on"
        def _detach_from (self, node):
            self.called = "_detach_from"


    def test_called (self):
        c = ConfNode ()
        c.backend = TestConfBackend.MockBackend ()

        self.assertEqual (c.backend.called, "_attach_on")
        c.load ()
        self.assertEqual (c.backend.called, "_do_load")
        c.save ()
        self.assertEqual (c.backend.called, "_do_save")
        c.child ("x")
        self.assertEqual (c.backend.called, "_handle_conf_new_child")
        c.remove ("x")
        self.assertEqual (c.backend.called, "_handle_conf_del_child")
        c.value = 1
        self.assertEqual (c.backend.called, "_handle_conf_change")
        c.nudge ()
        self.assertEqual (c.backend.called, "_handle_conf_nudge")
        be = c.backend
        c.backend = None
        self.assertEqual (be.called, "_detach_from")

    def test_set_backend (self):
        c = ConfNode ()
        c.child ("a")
        c.backend = TestConfBackend.MockBackend ()
        c.child ("b")

        self.assertTrue (isinstance (c.backend,
                                     TestConfBackend.MockBackend))
        self.assertTrue (isinstance (c.child ("a").backend,
                                      TestConfBackend.MockBackend))
        self.assertTrue (isinstance (c.child ("b").backend,
                                      TestConfBackend.MockBackend))
        self.assertRaises (ConfError,
                           c.child ("a").set_backend,
                           NullBackend ())

    def test_global_conf (self):
        cfg = GlobalConf ()

        self.assertTrue (isinstance (cfg.path ("h.o.l.a"), ConfNode))
        self.assertTrue (not isinstance (cfg.path ("h.o.l.a"), GlobalConf))
