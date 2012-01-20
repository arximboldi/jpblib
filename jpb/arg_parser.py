# -*- coding: utf-8 -*-
#
#  File:       arg_parser.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 18:50:38 jbo>
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
This module provides facilities to parse the command line arguments in
a more convenient way than 'getopt'.
"""

from error import BaseError

class ArgParserError (BaseError):
    """
    Common exception base for all argument parsing errors.
    """

    def __init__(self):
        """ Constructor """
        BaseError.__init__(self, message = "Unknown argument parsing error")

class UnknownArgError (ArgParserError):
    """
    Error thrown when an unknown option is passed as an argument.
    """

    def __init__(self, arg):
        """
        Constructor.

        Parameters:
        arg -- The unknown argument string.
        """
        super (ArgParserError, self).__init__(message = "Unknown arg: " + arg)

class OptionBase (object):
    """
    Common base for all kind of options. An 'option' is a handler for
    a detected flag.
    """

    def parse_with(self, arg):
        """
        Parses the flag receiving one argument. Return False if the
        option should not receive an argument or True if it correctly
        parsed the argument.

        Parameters:
        arg -- Argument passed to the flag.
        """
        return False

    def parse_flag(self):
        """
        Parses a flag receiving no argument. Return False if the
        option should receive an argument or True if it correctly
        handled the flag.
        """
        return False

class OptionWith (OptionBase):
    """
    An option that parses the flag argument using a given function,
    storing it in the 'value' attribute.

    Attributes:

      - value: The value parsed.
    """

    def __init__(self, func, default = None):
        """
        Constructor.

        Parameters:

          - func: The function to use to parse the string.
          - default: The default value to assign to the value attribute.
        """
        super (OptionWith, self).__init__ ()
        self.value = default
        self._func = func

    def parse_with(self, arg):
        """
        Parses the option and returns True.
        """
        self.value = self._func (arg)
        return True

class OptionFlag (OptionBase):
    """
    This option parses a flag, storing a fixed result in the value
    attribute.

    Attributes:

      - value: The resulting value.
    """

    def __init__(self, default = False, flag = True):
        """
        Constructor.

        Arguments:

          - default: The initial value for the value attribute.

          - flag: The value to assing to the value attribute in
          presence of a flag.
        """
        super (OptionFlag, self).__init__ ()
        self.value = default
        self.flag = flag

    def parse_flag(self):
        """
        Parses the flag.
        """
        self.value = self.flag
        return True

class OptionFunc (OptionBase):
    """
    This option runs a given function in the presence of a flag.
    """

    def __init__(self, func):
        """
        Constructor.

        Arguments:
          - func: The function to be run.
        """
        super (OptionFunc, self).__init__ ()
        self._func = func

    def parse_flag(self):
        """
        Runs the function.
        """
        self._func ()
        return True


class ArgParser (object):
    """
    Given a set of options this class parses the command line
    arguments. Any free non flag arguments are stored in a list.

    One can register more than one option in the same flag. In
    presence of the flag, all the options will be called with no
    arguments and, if more than option takes an argument, they will
    consume the subsequent arguments one each in the order in which
    they where registered. This allows you to have flags that take
    multiple arguments.
    """

    def __init__(self, *a, **k):
        """ Constructor """
        super (ArgParser, self).__init__ (*a, **k)
        self._free_args = []
        self._long_ops = {}
        self._short_ops = {}

    @property
    def free_args (self):
        """
        Returns the list of free arguments, that should be ready
        after parsing.
        """

        return self._free_args

    def add (self, shortarg, longarg, option):
        """
        Registers a new option into the parser.

        Parameters:
          - shortarg: Once character for the short version of the
          flag. Can be None.
          - longarg: Long version of the flag. Can be None.
          - option: Option object to parse the flag.
        """
        if shortarg in self._short_ops:
            self._short_ops[shortarg].append(option)
        else:
            self._short_ops[shortarg] = [option]

        if longarg in self._long_ops:
            self._long_ops[longarg].append(option)
        else:
            self._long_ops[longarg] = [option]

        return self

    def parse (self, argv):
        """
        Parses a given list of command line arguments, invoking the
        options and filling the free_args list.

        Parameters:
          - argv: The list of command line arguments.
        """
        i = 1
        self._argc = len (argv)
        self._argv = argv

        try:
            while i < self._argc:
                if len (argv[i]) > 1 and argv[i][0] == '-':
                    if argv[i][1] == '-':
                        i = self._parse_long (i)
                    else:
                        i = self._parse_short (i)
                else:
                    self._free_args.append (arg)
        except KeyError, e:
            raise UnknownArgError (str (e))

    def _parse_long (self, i):
        arg = self._argv[i][2:]

        return reduce (self._parse_opt, self._long_ops[arg], i + 1)

    def _parse_short (self, i):
        arg = self._argv[i][1:]

        return reduce (self._parse_opt,
                       sum (map (self._short_ops.__getitem__, arg), []),
                       i + 1)

    def _parse_opt (self, i, opt):
        if i >= self._argc or not opt.parse_with (self._argv[i]):
            opt.parse_flag ()
            return i
        else:
            return i+1
