# -*- coding: utf-8 -*-
#
#  File:       xml_util.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       2009
#  Time-stamp: <2012-01-20 20:32:16 jbo>
#

#
#  Copyright (C) 2012 Juan Pedro Bolívar Puente
#
#  This file is part of 2009.
#
#  2009 is free software: you can redistribute it and/or
#  modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  2009 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from error import BaseError
from xml.sax.handler import ContentHandler
from xml.sax import SAXException

class XmlError (BaseError): pass

class AutoContentHandler (ContentHandler, object):

    START_ELEMENT_PREFIX      = '_new_'
    END_ELEMENT_PREFIX        = '_end_'
    CHARACTERS_ELEMENT_PREFIX = '_chr_'

    def __init__ (self, *a, **k):
        super (AutoContentHandler, self).__init__ (*a, **k)
        self._name_stack = []
        self._depth = 0

    def startElement (self, name, attrs):
        self._name_stack.append (name)
        self.name = name
        self.dispatch_element (False, self.START_ELEMENT_PREFIX, attrs)
        self._depth += 1

    def endElement (self, name):
        self.name = name
        self.dispatch_element (True, self.END_ELEMENT_PREFIX)
        self._depth -= 1
        self._name_stack.pop ()

    def characters (self, content):
        self.dispatch_element (True, self.CHARACTERS_ELEMENT_PREFIX, content)

    def dispatch_element (self, silent, prev, *a, **k):
        attr = prev + self._name_stack [-1]

        if hasattr (self, attr):
            getattr (self, attr) (*a, **k)
        elif not silent:
            raise SAXException ('Unknown node: ' + self._name_stack [-1])

