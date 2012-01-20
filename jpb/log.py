# -*- coding: utf-8 -*-
#
#  File:       log.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 18:52:01 jbo>
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
Module providing a system for multi-backend hierachical logs.

It also defines the following log levels:
 - LOG_FATAL, LOG_ERROR, LOG_WARNING, LOG_INFO and LOG_DEBUG.
"""

from connection import Trackable
from observer import make_observer
from tree import AutoTree, AutoTreeTraits
from singleton import Singleton
import sys

LogSubject, LogListener = \
    make_observer (
    { 'on_message' :
      """
      A message has been catched in this log level. The sender log
      node, level and the message string will be passed as parameters
      in this order.
      """
    }, 'Log', __name__)

LOG_FATAL   = 10, "fatal"
LOG_ERROR   = 8,  "error"
LOG_WARNING = 6,  "warning"
LOG_INFO    = 4,  "info"
LOG_DEBUG   = 2,  "debug"

class StdLogListener (LogListener):
    """
    This is a log listener that outputs all the messages to the given
    files. It can filter the messages below a given log level.
    """

    def __init__ (self,
                  level = LOG_INFO,
                  info_out = sys.stdout,
                  error_out = sys.stderr,
                  *a, **k):
        """
        Constructor.

        Parameters:
          - level: The cut-off level. No message under this level will
            be registered. By default this is LOG_INFO.
          - info_out: File where to write messages for every message
            which is in a level below or equal LOG_INFO. By default
            this is sys.stdout.
          - error_out: File where to write the messages for all the
            received messages with a level over LOG_INFO. By default
            this is sys.stderr.
        """

        super (StdLogListener, self).__init__ (*a, **k)
        self.level = level
        self.info_output = info_out
        self.error_output = error_out

    def on_message (self, node, level, msg):
        """
        Logs the message into the files.
        """
        if level >= self.level:
            out = self.info_output if level <= LOG_INFO else self.error_output
            out.write ('[' + node.get_path_name () + '] ' +
                       level[1].upper () + ': '
                       + msg + '\n')


class LogNode (AutoTree, LogSubject):
    """
    This represents a node of a hierarchical log, and it is a log by
    itself. Note that when a message is logged in a node, it also
    logged in all the parents of that log. That way, you can
    modularize your messages. Some parts of your system will be
    interested on messages sent only by one sub-system, so they can
    register to the LogNode associated to it. Otherwise, if you want
    to listen to all messages, you can register your LogListener in the
    root LogNode of the hierarchy.
    """

    def __init__ (self, *a, **k):
        """ Constructor. """
        super (LogNode, self).__init__ (*a, **k)

    def log (self, level, msg):
        """
        This logs a message. When a message is logged, this invokes
        the 'on_message' signal on this log and all the parents of
        this log.

        Parameters:
          - level: Level of importance of this message.
          - msg: Message to be sent to be logged.
        """
        curr = self
        while curr:
            curr.on_message (self, level, msg)
            curr = curr.parent ()

    def info (self, msg):
        """ Logs a message with LOG_INFO level. """
        self.log (LOG_INFO, msg)

    def warning (self, msg):
        """ Logs a message with LOG_WARNING level. """
        self.log (LOG_WARNING, msg)

    def error (self, msg):
        """ Logs a message with LOG_ERROR level. """
        self.log (LOG_ERROR, msg)

    def fatal (self, msg):
        """ Logs a message with LOG_FATAL level. """
        self.log (LOG_FATAL, msg)

    def debug (self, msg):
        """ Logs a message with LOG_DEBUG level. """
        self.log (LOG_DEBUG, msg)


class GlobalLog (LogNode):
    """
    Global log singleton instance. Note that as this is a Singleton,
    whenever you invoke the constructor the same instance is returned.
    """

    __metaclass__ = Singleton

    class Traits (AutoTreeTraits):
        child_cls = LogNode

    def __init__ (self):
        """ Constructor. """
        super (GlobalLog, self).__init__ (auto_tree_traits = GlobalLog.Traits)


def log (path, level, msg):
    """
    Logs a message into the global logger.

    Parameters:
      - path: Node of the global log where to register the message.
      - level: Importance of the registered message.
      - msg: Message to register.
    """
    GlobalLog ().path (path).log (level, msg)


def get_log (path):
    """
    Tool function that returns a log child in the global log with the
    given 'path' name.
    """
    return GlobalLog ().path (path)

