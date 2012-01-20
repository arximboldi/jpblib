# -*- coding: utf-8 -*-
#
#  File:       observer_old.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 18:56:17 jbo>
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


from signal import *
from meta import *
from connection import *


CleverSlot = mixin (Trackable, Slot)

class Naming:
    SUBJECT_CLASS_POSTFIX  = 'Subject'
    LISTENER_CLASS_POSTFIX = 'Listener'

    SIGNAL_PREFIX          = 'on_'
    SLOT_PREFIX            = '_slot_'
    HANDLER_PREFIX         = 'handle_'

    DISCONNECT_FUNCTION    = 'disconnect'
    ADD_LISTENER_FUNCTION  = 'add_listener'
    DEL_LISTENER_FUNCTION  = 'del_listener'
    CLEAR_FUNCTION         = 'clear'


def make_observer (signals, cls_lexeme = '_Some',
                   sub_doc = '', lst_doc = '',
                   forward = False,
                   defret = None, names = Naming):
    return make_observer_with (make_subject_methods,
                               make_listener_methods,
                               signals, cls_lexeme,
                               lst_doc, sub_doc, defret, names)


def make_clever_observer (signals, cls_lexeme = '_Some',
                          lst_doc = '', sub_doc = '',
                          defret = None, names = Naming):
    return make_observer_with (make_clever_subject_methods,
                               make_clever_listener_methods,
                               signals, cls_lexeme,
                               lst_doc, sub_doc, defret, names)


def make_light_observer (signals, cls_lexeme = '_Some',
                          lst_doc = '', sub_doc = '',
                          defret = None, names = Naming):
    return make_observer_with (make_light_observer_methods,
                               make_light_listener_methods,
                               signals, cls_lexeme,
                               lst_doc, sub_doc, defret, names)

def make_observer_with (sub_mthd_fn, lst_mthd_fn,
                        signals, cls_lexeme = '_Some',
                        sub_doc = '', lst_doc = '',
                        defret = None, names = Naming):
    sub_dir = sub_mthd_fn (signals, names)
    sub_dir ['__doc__'] = sub_doc
    sub_cls = type (cls_lexeme + names.SUBJECT_CLASS_POSTFIX,
                    (object,), sub_dir)

    lst_dir = lst_mthd_fn (signals, defret, names)
    lst_dir ['__doc__'] = lst_doc
    lst_cls = type (cls_lexeme + names.LISTENER_CLASS_POSTFIX,
                    (object,), lst_dir)

    return sub_cls, lst_cls


def clever_observer (subject_cls, listener_cls, signals,
                     defret = None, names = Naming):
    clever_subject (subject_cls, signals, names)
    clever_listener (listener_cls, signals, defret, names)

    return subject_cls, listener_cls


def light_observer (subject_cls, listener_cls, signals,
                    defret = None, names = Naming):
    light_subject (subject_cls, signals, names)
    light_listener (listener_cls, signals, defret, names)

    return subject_cls, listener_cls


def observer (subject_cls, listener_cls, signals,
              defret = None, names = Naming):
    subject (subject_cls, signals, names)
    listener (listener_cls, signals, defret, names)

    return subject_cls, listener_cls


def subject (cls, signals, names = Naming):
    return extend_methods (
        cls, **make_subject_methods (signals, names))


def listener (cls, signals, defret = None, names = Naming):
    return extend_methods (
        cls, **make_listener_methods (signals, defret, names))


def clever_listener (cls, signals, defret = None, names = Naming):
    return extend_methods (
        cls, **make_clever_listener_methods (signals, defret, names))


clever_subject = subject


light_listener = listener


def light_subject (cls, signals, names = Naming):
    return extend_methods (
        cls, **make_light_subject_methods (signals, names))


def make_clever_listener_methods (signals, defret = None, names = Naming):

    def init (self):
        for sig in signals:
            setattr (self, names.SLOT_PREFIX + sig, CleverSlot (
                getattr (self, names.HANDLER_PREFIX + sig)))

    def disconnect (self):
        for sig in signals:
            getattr (self, names.SLOT_PREFIX + sig).disconnect_sources ()

    methods = { '__init__' : init,
               names.DISCONNECT_FUNCTION : disconnect }

    methods.update (make_listener_methods (signals, defret, names))
    return methods


def make_clever_subject_methods (signals, names = Naming):

    def add_listener (self, listener):
        for sig in signals:
            getattr (self, names.SIGNAL_PREFIX + sig).connect (
                getattr (listener, names.SLOT_PREFIX + sig))

    methods = make_subject_methods (signals, names)
    methods [names.ADD_LISTENER_FUNCTION] = add_listener

    return methods


def make_light_subject_methods (signals, names = Naming):

    def init (self):
        self._listeners = []

    def add_listener (self, listener):
        self._listeners.append (listener)
        return listener

    def del_listener (self, listener):
        self._listeners.remove (listener)
        return listener

    def clear (self):
        del self._listeners [:]

    methods = {'__init__' : init,
               names.ADD_LISTENER_FUNCTION : add_listener,
               names.DEL_LISTENER_FUNCTION : del_listener,
               names.CLEAR_FUNCTION : clear }

    for sig in signals:
        handler = names.HANDLER_PREFIX + sig
        def signal_func (self, __handler = handler, *args, **kw):
            for listener in self._listeners:
                getattr (listener, __handler) (*args, **kw)
        methods [names.SIGNAL_PREFIX + sig] = signal_func

    return methods


def make_listener_methods (signals, defret = None, names = Naming):

    def empty_method (self, *args, **kw):
        return defret

    methods = {}
    for sig in signals:
        methods [names.HANDLER_PREFIX + sig] = empty_method

    return methods


def make_subject_methods (signals, names = Naming):

    def init (self):
        for sig in signals:
            setattr (self, names.SIGNAL_PREFIX + sig, Signal ())

    def add_listener (self, listener):
        for sig in signals:
            getattr (self, names.SIGNAL_PREFIX + sig).connect (
                getattr (listener, names.HANDLER_PREFIX + sig))

    def del_listener (self, listener):
        for sig in signals:
            getattr (self, names.SIGNAL_PREFIX + sig).disconnect (
                getattr (listener, names.HANDLER_PREFIX + sig))

    def clear (self):
        for sig in signals:
            getattr (self, names.SIGNAL_PREFIX + sig).clear ()

    methods = {'__init__' : init,
               names.ADD_LISTENER_FUNCTION : add_listener,
               names.DEL_LISTENER_FUNCTION : del_listener,
               names.CLEAR_FUNCTION : del_listener }

    return methods


make_light_listener_methods = make_listener_methods


