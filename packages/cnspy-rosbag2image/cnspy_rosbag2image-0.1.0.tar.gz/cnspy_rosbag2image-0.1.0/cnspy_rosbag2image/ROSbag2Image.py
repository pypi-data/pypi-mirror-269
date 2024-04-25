#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2022, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
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

import numpy as np
import rosbag
import time
import os
import argparse
import yaml
import csv
from tqdm import tqdm
import cv2
import cv_bridge

from cnspy_rosbag2image.ImageFormatTypes import ImageFormatTypes
from cnspy_rosbag2image.ROSMessageTypes import ROSMessageTypes



class ImageRectifier:
    camera_model = None

    # distortion coefficients [k1,k2,p1,p2,k3,k4,k5,k6,s1,s2,s3,s4,taux,tauy] of 4, 5, 8, 12 or 14 elements.
    distortion_coeffs = None
    distortion_model  = None
    # [f_x, f_y, c_x, c_y]
    intrinsics = None
    # A = [f_x 0 c_x; 0 f_y c_y; 0 0 1]
    camera_matrix = None
    resolution = None
    image_size = None

    def __init__(self, camchain_fn):
        # Read Calibration and generate camera matrix
        if self.load_Kalibr_CamChain(camchain_fn):
            # https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga7dfb72c9cf9780a347fbe3d1c47e5d5a
            self.map_x, self.map_y = cv2.initUndistortRectifyMap(cameraMatrix=self.camera_matrix,
                                                                 distCoeffs=self.distortion_coeffs,
                                                                 R=None,
                                                                 newCameraMatrix=None,
                                                                 size=self.image_size,
                                                                 m1type=cv2.CV_8U)
        else:
            self.map_x = None
            self.map_y = None
        pass

    def undistort(self, img_in):
        if self.map_x is not None:
            return cv2.remap(img_in, self.map_x, self.map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        else:
            return img_in

    def load_Kalibr_CamChain(self, camchain_fn):
        with open(camchain_fn, 'r') as in_file:
            camchain = yaml.safe_load(in_file)
            if camchain is not None:
                self.camera_model = camchain['cam0']["camera_model"]
                self.distortion_coeffs = np.array(camchain['cam0']["distortion_coeffs"])
                self.distortion_model = camchain['cam0']["distortion_model"]
                self.intrinsics = np.array(camchain['cam0']["intrinsics"])
                self.resolution = camchain['cam0']["resolution"]

                self.camera_matrix = np.array([self.intrinsics[0], 0, self.intrinsics[2], 0, self.intrinsics[1], self.intrinsics[3], 0, 0, 1]).reshape(
                    3, 3)
                self.image_size = (self.resolution[0], self.resolution[1])

                in_file.close()
                return True
        return False


class ROSbag2Image:
    def __init__(self):
        pass

    @staticmethod
    def extract(bagfile_name, topic_list, result_dir="", img_prefixes=[], camchain_files=[],
                timestamp_in_name=False, verbose=False, fmt=ImageFormatTypes.PNG):
        if not os.path.isfile(bagfile_name):
            print("ROSbag2CSV: could not find file: %s" % bagfile_name)
            return False

        if len(topic_list) < 1:
            print("ROSbag2CSV: no topics specified!")
            return False

        if img_prefixes:
            if len(topic_list) != len(img_prefixes):
                print("ROSbag2CSV: topic_list and fn_list must have the same length!")
                return False

        if img_prefixes:
            if len(topic_list) != len(img_prefixes):
                print("ROSbag2CSV: topic_list and fn_list must have the same length!")
                return False

        if camchain_files:
            if len(topic_list) != len(camchain_files):
                print("ROSbag2CSV: camchain_files and fn_list must have the same length!")
                return False

        if verbose:
            print("ROSbagImage:")
            print("* bagfile name: " + str(bagfile_name))
            print("* topic_list: \t " + str(topic_list))
            print("* camchain_files: \t " + str(camchain_files))
            print("* img_prefixes: " + str(img_prefixes))
            print("* Image format: \t " + str(fmt))
            print("* Timestamp in name: \t " + str(timestamp_in_name))

        ## Open BAG file:
        try:
            bag = rosbag.Bag(bagfile_name)
        except:
            if verbose:
                print("ROSbagImage: Unexpected error!")

            return False

        info_dict = yaml.load(bag._get_yaml_info(), Loader=yaml.FullLoader)

        if info_dict is None or 'messages' not in info_dict:
            if verbose:
                print("ROSbagImage: Unexpected error, bag file might be empty!")
            bag.close()
            return False

        ## create result dir:
        if result_dir == "":
            folder = str.rstrip(bagfile_name, ".bag")
        else:
            folder = result_dir

        folder = os.path.abspath(folder)
        try:  # else already exists
            os.makedirs(folder)
        except:
            pass

        if verbose:
            print("* result_dir: \t " + str(folder))

        ## create csv file according to the topic names:
        dict_file_writers = dict()
        dict_header_written = dict()
        dict_csvfile_hdls = dict()
        dict_img_rectifier = dict()
        dict_img_prefix = dict()
        idx = 0
        for topicName in topic_list:

            if topicName[0] != '/':
                print("ROSbagImage: Not a proper topic name: %s (should start with /)" % topicName)
                continue

            if not img_prefixes:
                filename = str(folder + '/timestamp_') + str.replace(topicName[1:], '/', '_') + '.csv'
                dict_img_prefix[topicName] = str.replace(topicName[1:], '/', '_')
            else:
                prefix = img_prefixes[idx]
                filename = str(folder + '/timestamp_') + prefix + '.csv'
                dict_img_prefix[topicName] = prefix

            csvfile = open(filename, 'w+')
            file_writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            dict_file_writers[topicName] = file_writer
            dict_header_written[topicName] = False
            dict_csvfile_hdls[topicName] = csvfile
            dict_img_rectifier[topicName] = None

            if camchain_files:
                camchain_fn = camchain_files[idx]
                rect = ImageRectifier(camchain_fn=camchain_fn)
                if rect.map_x is None:
                    print("ROSbag2CSV: could not load Kalibr camchain file: %s" % camchain_fn)
                    return False

                dict_img_rectifier[topicName] = rect

            if verbose:
                print("ROSbagImage: creating csv file: %s " % filename)

            idx = idx + 1

        ## check if desired topics are in the bag file:
        num_messages = info_dict['messages']
        bag_topics = info_dict['topics']
        for topicName in topic_list:
            found = False
            for topic_info in bag_topics:
                if topic_info['topic'] == topicName:
                    found = True

            if not found:
                print("# WARNING: desired topic [" + str(topicName) + "] is not in bag file!")

        if verbose:
            print("\nROSbagImage: num messages " + str(num_messages))

        # Initialize the ROS-CV bridge
        bridge = cv_bridge.CvBridge()

        ## extract the desired topics from the BAG file
        for topic, msg, t in tqdm(bag.read_messages(), total=num_messages, unit="msgs"):
            if topic in topic_list:
                message_type = ROSMessageTypes.get_message_type(msg)
                if message_type != ROSMessageTypes.NOT_SUPPORTED:
                    file_writer = dict_file_writers[topic]

                    if not dict_header_written[topic]:
                        file_writer.writerow(['t', 'seq'])
                        dict_header_written[topic] = True

                    # write timestamp into file
                    cnt = msg.header.seq
                    timestamp_str = str("{}".format(float(msg.header.stamp.secs) + float(msg.header.stamp.nsecs) * 1e-9))
                    content = [timestamp_str, str(cnt)]
                    file_writer.writerow(content)
                    cv_image = bridge.imgmsg_to_cv2(msg)

                    if dict_img_rectifier[topicName] is not None:
                        cv_image = dict_img_rectifier[topicName].undistort(cv_image)

                    if timestamp_in_name:
                        img_fn = folder + "/" + dict_img_prefix[topic] + "_" + timestamp_str + "." + fmt.str()
                    else:
                        img_fn = folder + "/" + dict_img_prefix[topic] + "_" + str(cnt) + "." + fmt.str()

                    if verbose:
                        print("\nROSbagImage: writing file: " + img_fn)

                    cv2.imwrite(img_fn, cv_image)


        ## CLEANUP:
        # close all csv files
        for topicName in topic_list:
            dict_csvfile_hdls[topicName].close()

        # check if a topic was found by checking if the topic header was written
        for topicName in topic_list:
            if not dict_header_written[topicName]:
                print("\nROSbagImage: \n\tWARNING topic [" + str(topicName) + "] was not in bag-file")
                print("\tbag file [" + str(bagfile_name) + "] contains: ")
                # print(info_dict['topics'])
                for t in info_dict['topics']:
                    print(t['topic'])
                return False

        if verbose:
            print("\nROSbagImage: extracting done! ")

        bag.close()
        return True



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='ROSbag2Image: extract and store given topics of a rosbag into a images')
    parser.add_argument('--bagfile', help='input bag file', default="not specified")
    parser.add_argument('--topics', nargs='*', help='desired topics', default=[])
    parser.add_argument('--camchain_files', nargs='*', help='Kalibr camchain file per topic to undistort image', default=[])
    parser.add_argument('--img_prefixes', nargs='*', help='prefixes added to the images in the topic', default=[])
    parser.add_argument('--result_dir', help='directory to store results [otherwise bagfile name will be a directory]',
                        default='')
    parser.add_argument('--timestamp_in_name', action='store_true', help='append the timestamp after the prefix instead of number', default=False)
    parser.add_argument('--verbose', action='store_true', default=False)
    parser.add_argument('--format', help='image format', choices=ImageFormatTypes.list(),
                        default=str(ImageFormatTypes.PNG))

    tp_start = time.time()
    args = parser.parse_args()

    if ROSbag2Image.extract(bagfile_name=args.bagfile, topic_list=args.topics,
                           img_prefixes=args.img_prefixes, result_dir=args.result_dir,
                           camchain_files=args.camchain_files,
                           verbose=args.verbose, fmt=ImageFormatTypes(args.format)):
        print(" ")
        print("finished after [%s sec]\n" % str(time.time() - tp_start))
    else:
        print("failed! after [%s sec]\n" % str(time.time() - tp_start))