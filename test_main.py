# -*- coding: utf-8 -*-
#
#  File:       test_main.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       Fri Jan 20 16:29:21 2012
#  Time-stamp: <2012-01-23 18:45:16 jbo>
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
Unit test runner.
"""

from test.jpb_coop import *
from test.jpb_arg_parser import *
from test.jpb_changer import *
from test.jpb_conf import *
from test.jpb_connection import *
from test.jpb_event import *
from test.jpb_log import *
from test.jpb_meta import *
from test.jpb_observer import *
from test.jpb_observer_old import *
from test.jpb_sender import *
from test.jpb_signal import *
from test.jpb_singleton import *
from test.jpb_tree import *
from test.jpb_xml_conf import *

import unittest

if __name__ == '__main__':
    unittest.main ()

