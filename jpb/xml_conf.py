# -*- coding: utf-8 -*-
#
#  File:       xml_conf.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       Fri Jan 20 20:29:33 2009
#  Time-stamp: <2012-01-20 20:30:57 jbo>
#

#
#  Copyright (C) 2009,2012 Juan Pedro Bolívar Puente
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

import string
from conf import NullBackend, ConfNode, ConfError
import log

from xml.sax import make_parser
from xml_util import AutoContentHandler

def read_bool (msg):
    return True if msg.lower () == 'true' else False

XML_CONF_TYPES = { "int"     : int,
                   "string"  : str,
                   "unicode" : unicode,
                   "float"   : float,
                   "bool"    : read_bool,
                   "default" : str }


class XmlConfError (ConfError):
    pass


class XmlConfBackend (NullBackend):

    def __init__ (self, fname,
                  update_on_change = False,
                  update_on_nudge  = False,
                  *a, **k):
        super (XmlConfBackend, self).__init__ (*a, **k)

        self.save_on_change = update_on_change
        self.save_on_nudge  = update_on_nudge
        self.file_name = fname

    def _do_load (self, node, overwrite):
        setter = ConfNode.set_value if overwrite else ConfNode.default
        reader = XmlSaxConfParser (node, setter)

        parser = make_parser ()
        parser.setContentHandler (reader)

        try:
            fh = open (self.file_name, 'r')
        except IOError:
            raise XmlConfError (message =
                                'Could not open config file. ' +
                                'If this is the first time you ' +
                                'run the application it might be created later.',
                                level = log.LOG_WARNING)

        parser.parse (fh)
        fh.close ()

    def _do_save (self, node):
        fh = open (self.file_name, 'w')
        writer = XmlConfWriter (fh)
        writer.write (node)
        fh.close ()

    def _handle_conf_change (self, node):
        if self.save_on_change:
            self._do_save (node)

    def _handle_conf_nudge (self, node):
        if self.save_on_nudge:
            self._do_save (node)


def sanitize (s):
    return str (s).translate (string.maketrans ('', ''), '<>"')


class XmlConfWriter (object):

    def __init__ (self, fh):
        super (XmlConfWriter, self).__init__ ()

        self._fh = fh
        self._depth = 0

    def write (self, node):
        self._write_node (node, 'config')

    def _write_node (self, node, node_tag):
        indent = ' ' * self._depth * 2
        self._fh.write (indent + '<' + node_tag)

        if node.get_name ():
            self._fh.write (' name="' + sanitize (node.get_name ()) + '"')
        if not node.value is None:
            self._fh.write (' type="' + node.value.__class__.__name__ + '"')
            self._fh.write (' value="' + sanitize (node.value) + '"')

        childs = node.childs ()
        if len (childs) > 0:
            self._fh.write ('>\n')

            self._depth += 1
            for child in childs:
                self._write_node (child, 'node')
            self._depth -= 1

            self._fh.write (indent + '</' + node_tag + '>\n')
        else:
            self._fh.write ('/>\n')


class XmlSaxConfParser (AutoContentHandler):

    def __init__ (self,
                  conf_node = None,
                  setter = ConfNode.set_value,
                  *a, **k):
        super (XmlSaxConfParser, self).__init__ (*a, **k)
        self._curr_node = conf_node if conf_node else ConfNode ()
        self._curr_type = None
        self._setter = setter

    def conf_node (self):
        return self._curr_node

    def _new_config (self, attrs):
        if self._depth != 0:
            raise XmlConfError ('Unexpected \'config\' tag')
        self._curr_node.rename (attrs ['name'])
        self._fill_node (attrs)

    def _end_config (self):
        pass

    def _new_node (self, attrs):
        if self._depth < 1:
            raise XmlConfError ('Unexpected \'node\' tag')
        self._curr_node = self._curr_node.child (attrs ['name'])
        self._fill_node (attrs)

    def _end_node (self):
        self._curr_node = self._curr_node.parent ()

    def _fill_node (self, attrs):
        try:
            self._curr_type = XML_CONF_TYPES [attrs ['type']]
        except KeyError:
            self._curr_type = XML_CONF_TYPES ['default']

        try:
            self._setter (self._curr_node, self._curr_type (attrs ['value']))
        except KeyError:
            pass

