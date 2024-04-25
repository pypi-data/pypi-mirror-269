#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2020, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
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

import os
import unittest
from cnspy_rosbag2image.ROSbag2Image import *

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

class ROSbag2Image_Test(unittest.TestCase):
    def test_convert2PosOrientCov(self):
        img_prefixes = ['left', 'right']
        topic_list = ['/pose_est', '/pose_gt']

        bagfile = str(SAMPLE_DATA_DIR + '/empty.bag')
        self.assertFalse(ROSbag2Image.extract(bagfile_name=bagfile, topic_list=topic_list,
                                           img_prefixes=img_prefixes, result_dir=str(SAMPLE_DATA_DIR + '/results'),
                                           camchain_files=[],
                                           verbose=True, fmt=ImageFormatTypes('PNG')))


if __name__ == "__main__":
     unittest.main()