# -*- coding: utf-8 -*-
#
#  File:       connection.py
#  Author:     Juan Pedro Bolívar Puente <raskolnikov@es.gnu.org>
#  Date:       Nov 2009
#  Time-stamp: <2012-01-20 18:49:03 jbo>
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

"""
This module contains classes that ease the creation of one-to-many
connections between objects.
"""

from weakref import ref
from util import remove_if


class Source (object):
    """
    An instance of the Source interface represents the 'one' side of a
    one-to-many relationship. Note that a propper implementation of this
    interface should notify the Destiny instances when the connection
    between the Source and the Destiny has been stablished or finished.
    """

    def connect (self, destiny):
        """
        Connect the 'destiny' to this source.
        """
        pass

    def disconnect (self, destiny):
        """
        Disconnect the 'destiny' from this source.
        """
        pass


class Destiny (object):
    """
    An instance of the Destiny interface is one the entinies in the
    'many' side of a one-to-many relationship.
    """

    def handle_connect (self, source):
        """
        This method will be invocated by the Source 'source' when a
        successful connection has been stablished with it.
        """
        pass

    def handle_disconnect (self, source):
        """
        This method will be invocated by the Source 'source' when this
        Destiny instance is no longer connected to it.
        """
        pass


class Container (Source):
    """
    This is a Source that stores all the destinies in a
    container. This manages the proper notification of the destinies
    also, both on connection, manual disconnection, or destruction of
    this object. The instance variable '_destinies' can be considered
    protected and it is reasonable to use it from the subclasses to do
    things with the destinies.
    """

    def __init__ (self, *a, **kw):
        """
        Constructor.

        Keyword parameters:

          - container_type: A type instance of the desired container
            to be used in _destinies to store the connections. By
            default this a list, but using a WeakList can be usefull
            also.
        """
        super (Container, self).__init__ (*a, **kw)
        t = kw.get ('container_type', list)
        self._destinies = t ()
        self

    def __del__ (self):
        """
        Destructor. Notifies the destinies.
        """
        for dest in self._destinies:
            dest.handle_disconnect (self)

    def __getstate__ (self):
        """
        We should not store connections when pickling.
        """
        try:
            d = dict (super (Container, self).__getstate__ ())
        except Exception:
            d = dict (self.__dict__)
        d.update ({ '_destinies' : self._destinies.__class__ () })
        return d

    def connect (self, destiny):
        """
        Connects a destiny to this source, storying it and properly
        notifying it. The method will do nothing if the destiny has
        been connected already. Returns the destiny object.
        """
        if destiny not in self._destinies:
            self._destinies.append (destiny)
            destiny.handle_connect (self)
        return destiny

    def disconnect (self, destiny):
        """
        Disconnects a destiny from this source, properly notifying
        it. This will raise a ValueError if the destiny is not
        connected.
        """
        self._destinies.remove (destiny)
        destiny.handle_disconnect (self)

    def disconnect_if (self, predicate):
        """
        Disconnects all the sources that satisfy 'predicate', being
        'predicate' a boolean function over the destiny objects.
        """

        def pred (dest):
            if predicate (dest):
                dest.handle_disconnect (self)
                return True
            return False

        self._destinies = remove_if (pred, self._destinies)

    def clear (self):
        """
        Disconnects all the destinies from this source.
        """

        for dest in self._destinies:
            dest.handle_disconnect (self)
        del self._destinies [:]

    @property
    def count (self):
        """
        Number of destinies connected to this source.
        """
        return len (self._destinies)


class Trackable (Destiny):
    """
    This is a Destiny that keeps track of all the sources that are
    connected to it, so you can disconnect from all of them from the
    destiny once you do not know about the source endpoints anymore,
    easing the avoidance of leaking connections. This class
    disconnects on the destructor also, so it can come very handy also
    when you have weak references to the destinies in the Source
    endpoint. This class instances only store weak references to
    connected the sources, so you don't have to worry about using this
    creating a circular reference problem.

    This Destiny is actually designed to be used as a mixin that
    extends other destiny --this means, inherit at the same time from
    this and an object that is a Destiny but does not overload the
    Destiny methods in its own way. This way you can choose whether
    you want with the overhead of keeping track of the destinies in
    the leafs of your hierarchy, or even at object construction time
    using 'meta.mixin'. If the other Destiny actually overloads the
    Destiny methods this class is still designed to cooperate and will
    call those using the super(...) mechanism.
    """

    def __init__ (self, *a, **kw):
        """
        Constructor.
        """
        super (Trackable, self).__init__ (*a, **kw)
        self._sources = []

    def __del__ (self):
        self.disconnect_sources ()

    def __getstate__ (self):
        """
        We should not store connections when pickling.
        """
        return { '_sources' : [] }

    def handle_connect (self, source):
        """
        Handles the connection to the source by keeping a weak
        reference to it.
        """
        self._sources.append (ref (source))
        super (Trackable, self).handle_connect (source)

    def handle_disconnect (self, source):
        """
        Handles the disconnection from the source removing any weak
        reference from it.
        """
        self._sources = remove_if (lambda x : x () == source, self._sources)
        super (Trackable, self).handle_disconnect (source)

    def disconnect_sources (self):
        """
        Disconnects from all the sources this destiny is connected to.
        """
        while len (self._sources) > 0:
            if self._sources [0] ():
                self._sources [0] ().disconnect (self)

    @property
    def source_count (self):
        """
        Number of sources this destiny is connected to.
        """
        return len (self._sources)


class Tracker (object):
    """
    A tracker can be used to manage a group of Trackables.
    """

    def __init__ (self, *a, **k):
        super (Tracker, self).__init__ (*a, **k)
        self._trackables = []

    def __getstate__ (self):
        """
        We should not store connections when pickling.
        """
        return { '_trackables' : [] }

    def register_trackable (self, trackable):
        """
        Registers 'trackable' into this tracker.
        """
        self._trackables.append (trackable)

    def disconnect_all (self):
        """
        Disconnects all the trackables registered into this instance.
        """
        for t in self._trackables:
            t.disconnect_sources ()

    @property
    def trackable_count (self):
        """
        Number of trackables registered into this instance.
        """
        return len (self._trackables)
