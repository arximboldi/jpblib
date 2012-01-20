# -*- coding: utf-8 -*-
#
#  File:       util.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:29:09 jbo>
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


import functools

near0 = 0.0001

def index_if (cond, list):
    for i, x in enumerate (list):
        if cond (x):
            return i
    raise IndexError, "Element not found."

def const (val):
    return lambda: val

class Selfable (object):

    def myself (self):
        return self


def linear (minv, maxv, val):
    return minv + (maxv - minv) * val


def nop (*a, **k):
    pass

def trace (val):
    print val
    return val

def clamp (val, vmin, vmax):
    if val < vmin: return vmin
    if val > vmax: return vmax
    return val

def union (d1, d2):
    d1.update (d2)
    return d1

def selflast (func):
    return lambda *a, **k: func (* ([a[-1]] + list(a[:-1])), ** k)

def delayed (func):
    return lambda *a1, **k1: lambda *a2, **k2: \
        func (* (a1 + a2), ** union (k1, k2))

def delayed2 (func):
    return lambda *a, **k: functools.partial (func, *a, **k)


class lazyprop (object):

    def __init__ (self, func, name = None):
        self._func    = func
        self._name    = name or func.__name__

    def __get__ (self, obj, cls = None):
        if obj is None:
            return None
        result = obj.__dict__ [self._name] = self._func (obj)
        return result


class MultiMethod (object):

    def __init__ (self, name):
        self.name = name
        self.typemap = {}

    def __call__ (self, *args):
        types = tuple (arg.__class__ for arg in args)
        function = self.typemap.get (types)
        if function is None:
            raise TypeError ("no match")
        return function(*args)

    def register (self, types, function):
        if types in self.typemap:
            raise TypeError ("duplicate registration")
        self.typemap[types] = function


_multimethod_registry = {}

def multimethod (*types):
    """
    http://www.artima.com/weblogs/viewpost.jsp?thread=101605
    """

    def register (function):
        function = getattr (function, "__lastreg__", function)
        name = function.__name__
        mm = _multimethod_registry.get (name)
        if mm is None:
            mm = _multimethod_registry[name] = MultiMethod (name)
        mm.register (types, function)
        mm.__lastreg__ = function
        return mm
    return register


class memoize:
    """
    http://avinashv.net/2008/04/python-decorators-syntactic-sugar/
    """

    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            ret = self.memoized[args]
        except KeyError:
            ret = self.memoized[args] = self.function(*args)
        return ret


def printfn (message):
    print message


def remove_if (predicate, lst):
    return [elem for elem in lst if not predicate (elem)]


def flip_dict (dct):
    new_dct = {}
    for k, v in dct.items ():
        new_dct [v] = k
    return new_dct


def read_file (fname):
    fh = open (fname, 'r')
    content = fh.read ()
    fh.close ()
    return content
