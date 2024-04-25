#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2020, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
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
########################################################################################################################
from enum import Enum


class ImageFormatTypes(Enum):
    JPEG = 'JPEG'
    JPG = 'JPG'
    PNG = 'PNG'

    def __str__(self):
        return str(self.value)

    def str(self):
        return str(self.value)

    @staticmethod
    def list():
        return list([str(ImageFormatTypes.JPEG),
                     str(ImageFormatTypes.JPG),
                     str(ImageFormatTypes.PNG)])
        pass