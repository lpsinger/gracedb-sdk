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
from .base import Mutable, Resource


VOEVENT_TYPES = {'preliminary': 'PR',
                 'retraction': 'RE',
                 'update': 'UP',
                 'initial': 'IN'}


# FIXME: events have a 'event/' resource whereas superevents have 'events/'.
# Combine BaseVOEvents, EventVOEvents, and SupereventVOEvents into a single
# VOEvents class once this inconsistency has been fixed.
class BaseVOEvents(Mutable, Resource):

    def create_or_update(self, key, *, voevent_type=None, coinc_comment=None,
                         **kwargs):
        data = {'voevent_type': VOEVENT_TYPES[voevent_type],
                # FIXME: why doesn't GraceDB have a default for this field?
                'CoincComment': coinc_comment or False,
                **kwargs}
        return super().create_or_update(key, data=data)

    def get(self, **kwargs):
        return super().get(**kwargs)['voevents']


class EventVOEvents(BaseVOEvents):

    path = 'voevent/'


class SupereventVOEvents(BaseVOEvents):

    path = 'voevents/'
