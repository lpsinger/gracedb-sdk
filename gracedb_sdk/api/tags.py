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
from .base import Deletable, Mutable, Resource


# FIXME: events have a 'tag/' resource whereas superevents have 'tags/'.
# Combine BaseTags, EventTags, and SupereventTags into a single Log class
# once this inconsistency has been fixed.
#
# FIXME: GraceDB expects different HTTP methods to write tags for events vs.
# superevents!
class BaseTags(Deletable, Mutable, Resource):

    def get(self, **kwargs):
        return super().get(**kwargs)['tags']


class EventTags(BaseTags):

    path = 'tag/'

    def create(self, tag):
        return super().create_or_update(tag)


class SupereventTags(BaseTags):

    path = 'tags/'

    def create(self, label):
        return super().create_or_update(None, data={'name': label})
