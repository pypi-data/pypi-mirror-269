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


class ROSMessageTypes(Enum):
    NOT_SUPPORTED = 'NOT_SUPPORTED'
    # GEOMETRY_MSGS_POINT = 3 == VECTOR3
    SENSOR_MSGS_IMAGE='SENSOR_MSGS_IMAGE' # http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html

    def __str__(self):
        return str(self.value)

    @staticmethod
    def get_message_type(msg_):
        """

        :rtype: ROSMessageTypes
        """

        if hasattr(msg_, 'header'):  # STAMPED
            if hasattr(msg_, 'height') and hasattr(msg_, 'width') and hasattr(msg_, 'encoding') \
                    and hasattr(msg_, 'data'):
                return ROSMessageTypes.SENSOR_MSGS_IMAGE

        return ROSMessageTypes.NOT_SUPPORTED
