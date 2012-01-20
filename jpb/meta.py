# -*- coding: utf-8 -*-
#
#  File:       meta.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 18:53:12 jbo>
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
Metaprogramming utilities.
"""

from util import memoize, nop
from functools import wraps

class Mockup (object):

    def __getattribute__ (self, name):
        return lambda *a, **k: None


@memoize
def mixin (one, two, *args):
    class Mixin (one, two):
        def __init__ (self, *args, **kws):
            super (Mixin, self).__init__ (*args, **kws)

    if args:
        return mixin (Mixin, *args)
    return Mixin


def monkeypatch (target, name = None):
    def patcher (func):
        patchname = func.__name__ if name is None else name
        setattr (target, patchname, func)
        return func
    return patcher


def monkeypatch_extend (target, name = None):
    def patcher (func):
        newfunc = func
        patchname = func.__name__ if name is None else name
        if hasattr (target, patchname):
            oldfunc = getattr (target, patchname)
            if not callable (oldfunc):
                raise AttributeError ('Can not extend non callable attribute')
            def extended (*a, **k):
                ret = oldfunc (*a, **k)
                func (*a, **k)
                return ret
            newfunc = extended
        setattr (target, patchname, newfunc)
        return func
    return patcher


def instance_decorator (decorator):
    class Decorator (object):
        def __init__ (self, func = nop, *args, **kws):
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__
            self._func = func
            self._args = args
            self._kws = kws

        def __get__ (self, obj, cls = None):
            if obj is None:
                return None
            decorated = decorator (obj, self._func, *self._args, **self._kws)
            obj.__dict__[self.__name__] = decorated
            return decorated
    return Decorator


def extend_methods (cls, **kws):
    for name, new_method in kws.items ():
        if hasattr (cls, name):
            old_method = getattr (cls, name)
            if not callable (old_method):
                raise AttributeError ("Can not extend a non callable attribute")
            def extended (*args, **kw):
                new_method (*args, **kw)
                return old_method (*args, **kw)
            method = extended
        else:
            method = new_method
        setattr (cls, name, method)

    return cls
