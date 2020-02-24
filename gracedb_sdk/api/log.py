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
from .base import Resource
from .tags import EventTags, SupereventTags


# FIXME: events have a 'log/' resource whereas superevents have 'logs/'.
# Combine BaseLog, EventLog, and SupereventLog into a single Log class
# once this inconsistency has been fixed.
class BaseLog(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = self.tags_class(self)


class EventLog(BaseLog):

    tags_class = EventTags


class SupereventLog(BaseLog):

    tags_class = SupereventTags
