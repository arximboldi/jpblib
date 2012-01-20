# -*- coding: utf-8 -*-
#
#  File:       sender.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:18:31 jbo>
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
This module provides a way to send different messages named objects
between objects.
"""

from connection import *

class Receiver (Destiny):
    """
    A Receiver can be used to handle the messages emited by a
    sender. Whenever a message is emited from a sender to which the
    receiver is connected, the 'receive' method will be invoqued.
    """

    def receive (self, message, *args, **kws):
        """
        Method used to receive messages from a Sender. 'message' is
        the message sent by the receiver and any other parameters are
        passed afterwards. You can provide your own implementation of
        this method. The default behaviour if to invoque the method
        with name 'message' in the receiver object or throw an
        AtttributeError if there is no method with that name in this
        receiver.
        """
        if not hasattr (self, message):
            raise AttributeError ('Uncaugh message: ' + message)
        return getattr (self, message) (*args, **kws)


class AutoReceiver (Receiver):

    def receive (self, message, *args, **kws):
        if hasattr (self, message):
            return getattr (self, message) (*args, **kws)


class Sender (Container):
    """
    A Sender can be used to emit different named messages to different
    Receivers, that can connect to it.
    """

    def send (self, message, *args, **kws):
        """
        Sends the message 'message' to all the receivers that are
        connected. Any other arguments that are passed to this
        function will be sent to the receivers as well.
        """

        for f in self._destinies:
            f.receive (message, *args, **kws)


class AutoSender (Sender):
    """
    Every attribute is considered a message sender.
    """

    def __getattr__ (self, name):
        return lambda *a, **k: self.send (name, *a, **k)

