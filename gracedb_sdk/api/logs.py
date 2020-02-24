#
# Copyright (C) 2019-2020  Leo P. Singer <leo.singer@ligo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from .base import Mapping, Mutable, Resource
from .log import EventLog, SupereventLog
from .util import field_collection, str_or_collection


# FIXME: events have a 'log/' resource whereas superevents have 'logs/'.
# Combine BaseLogs, EventLogs, and SupereventLogs into a single Logs class
# once this inconsistency has been fixed.
class BaseLogs(Mapping, Mutable, Resource):

    def get(self, **kwargs):
        return super().get(**kwargs)['log']

    def create_or_update(self, key, *,
                         filename=None, filecontents=None, tags=None,
                         **kwargs):
        # FIXME: gracedb server does not support form-encoded input
        # if there is no file!
        if filename is None and filecontents is None:
            json = {'tagname': str_or_collection(tags), **kwargs}
            data = None
            files = None
        else:
            data = (*field_collection('tagname', tags), *kwargs.items())
            json = None
            files = {'upload': (filename, filecontents)}
        return super().create_or_update(key, data=data, json=json, files=files)


class EventLogs(BaseLogs):

    path = 'log/'
    mapped_class = EventLog


class SupereventLogs(BaseLogs):

    path = 'logs/'
    mapped_class = SupereventLog
