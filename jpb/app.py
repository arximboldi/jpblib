# -*- coding: utf-8 -*-
#
#  File:       app.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2010
#  Time-stamp: <2012-01-20 18:50:55 jbo>
#

#
#  Copyright (C) 2010, 2011 Juan Pedro Bolívar Puente
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
Python application basic framework.
"""

import sys
import os.path
import os
import traceback

from xml_conf import *
from conf import *
from log import *
from arg_parser import *

_log = get_log (__name__)

class AppSuccess (Exception):
    pass

class AppBase (object):

    GLOBAL      = True

    NAME        = os.path.basename (sys.argv[0])
    VERSION     = ''
    DESCRIPTION = ''
    AUTHOR      = ''
    COPYRIGHT   = ''

    LOG_FILE    = 'messages.log'
    CONFIG_FILE = 'config.xml'

    LICENSE     = \
"""\
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

    USAGE       = \
"""\
Usage: %(program)s [options]
"""

    OPTIONS     = \
"""\
Options:
  -h, --help       Display this information.
  -v, --version    Display program version.
  -V, --verbose    Display debugging information.
"""

    def do_prepare (self, argparser):
        pass

    def do_execute (self, args):
        pass

    def do_release (self):
        pass

    def run_and_exit (self):
        sys.exit (self.run ())

    def run (self):
        self._std_logger  = None
        self._file_logger = None
        self._log_file    = None

        if self.GLOBAL:
            self._std_logger = StdLogListener ()
            GlobalConf ().rename (self.NAME)
            GlobalLog ().rename (self.NAME)
            GlobalLog ().connect (self._std_logger)

        args = self.make_args ()
        self.do_prepare (args)

        try:
            args.parse (sys.argv)
            self.setup_folders ()
            self.setup_log ()
            self.load_config ()

            ret_val = self.do_execute (args.free_args)
            self.save_config ()
        except AppSuccess, e:
            ret_val = os.EX_OK
        except LoggableError, e:
            e.log ()
            _log.debug (traceback.format_exc ())
            ret_val = e.get_code ()
        except Exception, e:
            _log.fatal ("Unexpected error:\n" + e.message)
            _log.debug (traceback.format_exc ())
            ret_val = os.EX_SOFTWARE

        self.do_release ()
        self.close_log ()

        return ret_val

    def print_help (self):
        print self.DESCRIPTION
        print self.USAGE % { "program" : self.NAME}
        print self.OPTIONS

        raise AppSuccess ()

    def print_version (self):
        print self.NAME, self.VERSION, '\n'
        print self.COPYRIGHT
        print self.LICENSE
        print "Written by", self.AUTHOR

        raise AppSuccess ()

    def get_config_folder (self):
        return self._config_folder

    def get_data_folder (self):
        return self._data_folder

    def setup_folders (self):
        self._config_folder = os.path.join (os.environ ['HOME'], '.' + self.NAME)
        self._data_folder = os.path.join (['data'])

        if not os.path.isdir (self._config_folder):
            os.makedirs (self._config_folder)

    def load_config (self):
        if self.GLOBAL:
            try:
                GlobalConf ().set_backend (XmlConfBackend (
                    os.path.join (self.get_config_folder (), self.CONFIG_FILE)))
                GlobalConf ().load ()
            except LoggableError, e:
                e.log ()

    def save_config (self):
        if self.GLOBAL:
            try:
                GlobalConf ().save ()
            except LoggableError, e:
                e.log ()

    def setup_log (self):
        if self.GLOBAL:
            fname = os.path.join (self.get_config_folder (), self.LOG_FILE)
            try:
                self._log_file = open (fname, 'w')
                self._file_logger = StdLogListener (LOG_INFO,
                                                   self._log_file,
                                                   self._log_file)
                GlobalLog ().connect (self._file_logger)
            except Exception:
                _log.warning ("Could not open log file, " + fname)

        if self._arg_verbose.value:
            if self._std_logger:
                self._std_logger.level = LOG_DEBUG
            if self._file_logger:
                self._file_logger.level = LOG_DEBUG

    def close_log (self):
        if self.GLOBAL and self._log_file:
            self._log_file.close ()

    def make_args (self):
        self._arg_verbose = OptionFlag ()
        args = ArgParser ()
        args.add ('h', 'help', OptionFunc (self.print_help))
        args.add ('v', 'version', OptionFunc (self.print_version))
        args.add ('V', 'verbose', self._arg_verbose)
        return args
