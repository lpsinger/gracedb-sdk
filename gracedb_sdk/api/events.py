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
from os.path import join

from .base import Deletable, Mapping, Mutable, Resource
from .event import Event, Superevent
from .util import field_collection, str_or_collection


class BaseEvents(Deletable, Mapping, Mutable, Resource):

    def search(self, **kwargs):
        url = self.url
        while url:
            response = self.session.get(url, params=kwargs).json()
            url = response.get('links', {}).get('next')
            kwargs = None
            yield from response.get(self.path.strip('/'), [])


class Events(BaseEvents):

    path = 'events/'
    mapped_class = Event

    def __getitem__(self, key):
        """Make the API forgiving of mixing up events and superevents."""
        if 'S' in key:
            return self.parent.superevents[key]
        else:
            return super().__getitem__(key)

    def create_or_update(self, event_id, *,
                         filename='initial.data',
                         filecontents=None, labels=None, **kwargs):
        data = (*field_collection('labels', labels), *kwargs.items())
        files = {'eventFile': (filename, filecontents)}
        return super().create_or_update(event_id, data=data, files=files)


SUPEREVENT_CATEGORIES = {'M': 'M', 'T': 'T', 'G': 'P'}


class Superevents(BaseEvents):

    path = 'superevents/'
    mapped_class = Superevent

    def __getitem__(self, key):
        """Make the API forgiving of mixing up events and superevents."""
        if 'S' not in key:
            return self.parent.events[key]
        else:
            return super().__getitem__(key)

    def create_or_update(self, superevent_id, *,
                         events=None, labels=None, **kwargs):
        data = {key: value for key, value in kwargs.items()
                if value is not None}
        if events:
            data['events'] = str_or_collection(events)
        if labels:
            data['labels'] = str_or_collection(labels)

        # Automatically guess category based on prefix of preferred event
        preferred_event = kwargs.get('preferred_event')
        if preferred_event is not None:
            category = SUPEREVENT_CATEGORIES[preferred_event[0]]
            data['category'] = category

        # FIXME: superevent creation requests must be JSON-encoded rather than
        # form-encoded due to https://git.ligo.org/lscsoft/gracedb/issues/195
        if superevent_id is None:
            return super().create_or_update(superevent_id, json=data)
        else:
            # FIXME: GraceDB does not support 'put' here, only 'patch'!
            # This is inconsistent between events and superevents.
            url = join(self.url, superevent_id) + '/'
            return self.session.patch(url, json=data)
