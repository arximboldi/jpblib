# -*- coding: utf-8 -*-
#
#  File:       jpb_tree.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:50:20 jbo>
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

from jpb.tree import *

class TestAutoTree (unittest.TestCase):

    class ValueTree (AutoTree):
        def __init__ (self, default = None):
            super (TestAutoTree.ValueTree, self).__init__ ()
            self.value = default

    class CountingTree (AutoTree):
        def __init__ (self):
            super (TestAutoTree.CountingTree, self).__init__ ()
            self.childs = 0
        def _handle_tree_new_child (self, child):
            self.childs += 1
        def _handle_tree_del_child (self, child):
            self.childs -= 1

    def setUp (self):
        self._tree_1 = TestAutoTree.ValueTree ()
        self._tree_1.child ('a').value = 1
        self._tree_1.path ('a.b.c').value = 2

    def tearDown (self):
        self._tree_1 = None

    def test_paths_rename (self):
        child_1 = self._tree_1.child ('a')
        child_2 = self._tree_1.path ('a.b.c')

        self.assertEqual (child_1.value, 1)
        self.assertEqual (child_2.value, 2)
        self.assertEqual (child_2.get_path_name (), '.a.b.c')

        child_1.rename ('d')
        self.assertEqual (child_2.get_path_name (), '.d.b.c')

    def test_adopt (self):
        child = self._tree_1.path ('a.b')
        self._tree_1.child ('d').adopt (child, 'b')

        self.assertEqual (self._tree_1.path ('a.b.c').value, None)
        self.assertEqual (self._tree_1.path ('d.b.c').value, 2)

    def test_events (self):
        tree = TestAutoTree.CountingTree ();

        tree.child ('a')
        self.assertEqual (tree.childs, 1)
        tree.child ('b')
        self.assertEqual (tree.childs, 2)
        tree.child ('a')
        self.assertEqual (tree.childs, 2)
        tree.remove ('a')
        self.assertEqual (tree.childs, 1)
        tree.remove ('b')
        self.assertEqual (tree.childs, 0)

    def test_crawling (self):
        list_pre  = []
        list_post = []

        def mk_appender (list):
            def appender (x):
                return list.append (x.get_name ())
            return appender

        self._tree_1.dfs_preorder (mk_appender (list_pre))
        self._tree_1.dfs_postorder (mk_appender (list_post))

        self.assertEqual (list_pre, ["", "a", "b", "c"])
        self.assertEqual (list_post, ["c", "b", "a", ""])



