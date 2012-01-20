# -*- coding: utf-8 -*-
#
#  File:       event.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 18:52:41 jbo>
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

from log import get_log
from signal import Signal, signal
from sender import Sender, Receiver

"""
This module defines the EventManager class for managing a dynamic
group of signals with forwarding capabilities.
"""

_log = get_log (__name__)

class EventManager (Sender, Receiver):

    quiet = False

    def __init__ (self):
        super (EventManager, self).__init__ ()
        self._events = {}
        self.on_any_event = Signal ()

    def notify (self, name, *args, **kw):
        if not self.quiet:
            if name in self._events:
                self._events [name].notify (*args, **kw)
            else:
                self.send (name, *args, **kw)

    receive = notify

    def send (self, name, *a, **k):
        self.on_any_event.notify (name, a, k)
        super (EventManager, self).send (name, *a, **k)

    def event (self, name):
        if name in self._events:
            return self._events [name]

        signal = Signal ()
        signal += lambda *a, **k: self.send (name, *a, **k)
        self._events [name] = signal
        return signal

    def clear_events (self, name = None):
        if name:
            del self._events [name]
        else:
            self._events.clear ()
