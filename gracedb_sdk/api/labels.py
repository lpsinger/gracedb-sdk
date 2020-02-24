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


# FIXME: GraceDB expects different HTTP methods to write labels for events vs.
# superevents! Replace BaseLabels, EventLabels, SupereventLabels with a single
# Labels class once this is fixed.
class BaseLabels(Deletable, Mutable, Resource):

    path = 'labels/'

    def get(self, **kwargs):
        return super().get(**kwargs)['labels']


class EventLabels(BaseLabels):

    path = 'labels/'

    def create(self, label):
        return super().create_or_update(label)


class SupereventLabels(BaseLabels):

    path = 'labels/'

    def create(self, label):
        return super().create_or_update(None, data={'name': label})
