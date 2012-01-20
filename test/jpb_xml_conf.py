# -*- coding: utf-8 -*-
#
#  File:       jpb_xml_conf.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 21:23:03 jbo>
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

import unittest
from jpb.conf import *
from jpb.xml_conf import *
from jpb.util import read_file
import os
import os.path

XML_TEST_PATH = os.path.dirname (__file__)
XML_TEST_FILENAME = os.path.join (XML_TEST_PATH, 'jpb_xml_conf_test_file.xml')
XML_TEMP_FILENAME = os.path.join (XML_TEST_PATH, 'jpb_xml_conf_temp_file.xml')

class TestXmlConfWrite (unittest.TestCase):

    def test_write (self):
        conf = ConfNode (name = 'test')
        conf.path ('a').value = 1
        conf.path ('b.c').value = 2
        conf.path ('b.d').value = 3

        xml = XmlConfBackend (XML_TEMP_FILENAME)
        conf.set_backend (xml)

        conf.save ()

        self.assertEqual (read_file (XML_TEST_FILENAME),
                          read_file (XML_TEMP_FILENAME))

        os.remove (XML_TEMP_FILENAME)


class TestXmlConfRead (unittest.TestCase):

    def setUp (self):
        self.conf = ConfNode ()
        self.xml = XmlConfBackend (XML_TEST_FILENAME)
        self.conf.set_backend (self.xml)

    def test_read (self):
        self.conf.load ()

        self.assertEqual (self.conf.name, 'test')
        self.assertEqual (self.conf.path ('a').value, 1)
        self.assertEqual (self.conf.path ('b.c').value, 2)
        self.assertEqual (self.conf.path ('b.d').value, 3)

    def test_read_default (self):
        self.conf.child ('a').value = 10
        self.conf.load (False)

        self.assertEqual (self.conf.name, 'test')
        self.assertEqual (self.conf.path ('a').value, 10)
        self.assertEqual (self.conf.path ('b.c').value, 2)
        self.assertEqual (self.conf.path ('b.d').value, 3)

