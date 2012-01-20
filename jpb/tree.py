# -*- coding: utf-8 -*-
#
#  File:       tree.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:24:42 jbo>
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
This module provides a generic implementation of the Composite
pattern.
"""

class AutoTreeTraits (object):
    """
    This class encapsulates the parameters for an AutoTree
    hierachy. Inherit from it and override the required parameters to
    obtain a new object that you can pass to AutoTree's constructor.

    Class members:

      - name_type: The class to be used to build the name objects to
        label the nodes of the auto tree.

      - separator: When building the path name of a tree it will be
        formed concatenating the names of the childs in the path using
        this as separator.

      - child_cls: Class to be used when the auto_tree has to create a
        new object. If None, AutoTree will use self.__class__ as the
        class to use, which is the proper behaviour in most cases as you
        are supposed to inherit your nodes from AutoTree.
    """

    name_type = str
    separator = '.'
    child_cls = None


class AutoTree (object):
    """
    This class provides a way to create a hierarchy of objects. This
    can be considered a generic implementation of the Composite design pattern.

    Usage: A tree is not a normal tree, it is not intended to be used
    as a container. It is inteded to be used to create objects that
    contain their own childs in the hierarchy. This is a typical
    approach, for example, in Widget frameworks. This class can be
    used both as a mix-in or inheriting from it. As an invariant, a
    node can only belong to one AutoTree.
    """

    def __init__ (self,
                  name = None,
                  auto_tree_traits = AutoTreeTraits,
                  *a, **k):
        """
        Constructor.

        Keyword parameters:

          - auto_tree_traits: Object containing the behaviour parameters
            of the auto-tree. By default it is the AutoTreeTraits class.

          - name: Name to give to this node.
        """
        super (AutoTree, self).__init__ (*a, **k)

        self._traits = auto_tree_traits
        self._name = self._traits.name_type () if name is None else name
        self._parent = None
        self._childs = {}


    def child (self, name):
        """
        Return a child given its name. If it does not exist, it
        creates a new instance of self.__class__ or the class
        specified in the traits, gives it the specified name, inserts
        it into the tree, and returns it.
        """

        try:
            child = self._childs [name]
        except KeyError:
            if self._traits.child_cls:
                child = self._traits.child_cls ()
            else:
                child = self.__class__ ()
            self.adopt (child, name)

        return child

    def has_child (self, name):
        return name in self._childs

    get_child = child

    def path (self, path_name):
        """
        Returns the child that is specified in the given path.  All
        the non existing nodes along the path are created using de
        rules described in 'child'.
        """

        path = str.split (path_name, self._traits.separator)
        return reduce (AutoTree.child, path, self)

    get_path = path

    def get_name (self):
        """
        Returns the name of this node.
        """
        return self._name

    def get_path_name (self):
        """
        Returns the absolute path of this node starting from the root.
        """
        return self._traits.separator.join (self.get_path_list ())

    def get_path_list (self, base = None):
        """
        Appends the absolute path of this node starting from the root
        as a list of strings (names of the intermediate nodes) to the
        list passed in the parameter 'base'.
        """

        if base is None:
            base = []

        if self._parent:
            base = self._parent.get_path_list (base)
            base.append (self._name)
            return base
        else:
            base.append (self._name)
            return base

    def parent (self):
        """
        Returns the parent of this node.
        """
        return self._parent

    def reparent (self, parent):
        """
        Changes the parent of this node to 'parent'. Note that if the
        node had a parent already it is extracted from that tree. Be
        careful because this method does not check agains circular
        references.
        """
        return parent.adopt (self)

    def adopt (self, child, name = None):
        """
        Adopts a the node 'child' value renaming it to 'name'. Note
        that the child won't be renamed if 'name' is None. Also, if
        the child had a parent already, it is removed from that tree.
        """

        if name is None:
            name = child._name

        old_parent = child._parent
        if old_parent:
            old_parent.remove (child.get_name ())

        child._parent = self
        child._name   = name
        self._childs [name] = child
        self._handle_tree_new_child (child)

        return child

    def remove (self, name):
        """
        Removes the child named 'name' from the tree. That child is
        now a root value.
        """

        child = self._childs [name]
        self._handle_tree_del_child (child)
        del self._childs [name]
        child._parent = None
        child._name = self._traits.name_type ()

        return child

    def rename (self, name):
        """
        Changes the name of this node to 'name'
        """

        if self._parent:
            del self._parent._childs [self._name]
            self._parent._childs [name] = self
        self._name = name

    def dfs_preorder (self, func):
        """
        Crawls the tree in preorder deep-first-search calling func ()
        on every node. 'func' should therefore accept a node as a
        parameter.
        """

        func (self)
        for child in self._childs.values ():
            child.dfs_preorder (func)

    def dfs_postorder (self, func):
        """
        Same as 'dfs_preorder', but using postorder deep-first-search.
        """

        for child in self._childs.values ():
            child.dfs_postorder (func)
        func (self)

    def childs (self):
        """
        Returns a iterator over the childs of this node.
        """
        return self._childs.values ()

    def _handle_tree_new_child (self, child):
        pass

    def _handle_tree_del_child (self, child):
        pass

    name = property (get_name, rename, doc =
                     """
                     Name of the this node.
                     """)

