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
import os
from enum import Enum
import cnspy_spatial_csv_formats.PoseStructs as ps
from cnspy_spatial_csv_formats.EstimationErrorType import EstimationErrorType
from cnspy_spatial_csv_formats.ErrorRepresentationType import ErrorRepresentationType

# Primary loader for CSV files via Pandas.read_csv():
#  -  '#' are comments and first line after comment defines variable names!
#  -  Thus the 'TUM' format is not compatible and needs special treatment
class CSVSpatialFormatType(Enum):
    Timestamp = 'Timestamp'
    PoseStamped = 'PoseStamped'
    TUM = 'TUM'  # TUM-Format stems from: https://vision.in.tum.de/data/datasets/rgbd-dataset/tools#evaluation
    PositionStamped = 'PositionStamped'
    PosOrientCov = 'PosOrientCov'
    PosOrientWithCov = 'PosOrientWithCov'
    PosOrientWithCovTyped = 'PosOrientWithCovTyped'
    PoseCov = 'PoseCov'
    PoseWithCov = 'PoseWithCov'
    PoseWithCovTyped = 'PoseWithCovTyped'
    PoseErrorStamped = 'PoseErrorStamped'
    PoseTypedStamped = 'PoseTypedStamped'
    none = 'none'
    # HINT: if you add an entry here, please also add it to the .list() + .has_uncertainty method!

    def __str__(self):
        return self.value

    def has_uncertainty(self):
        if self == CSVSpatialFormatType.PosOrientCov or self == CSVSpatialFormatType.PosOrientWithCov or \
           self == CSVSpatialFormatType.PoseCov or self == CSVSpatialFormatType.PoseWithCov or \
           self == CSVSpatialFormatType.PoseWithCovTyped or self == CSVSpatialFormatType.PosOrientWithCovTyped:
            return True
        return False

    @staticmethod
    def list():
        return list([str(CSVSpatialFormatType.Timestamp),
                     str(CSVSpatialFormatType.PoseStamped),
                     str(CSVSpatialFormatType.TUM),
                     str(CSVSpatialFormatType.PositionStamped),
                     str(CSVSpatialFormatType.PosOrientCov),
                     str(CSVSpatialFormatType.PosOrientWithCov),
                     str(CSVSpatialFormatType.PosOrientWithCovTyped),
                     str(CSVSpatialFormatType.PoseCov),
                     str(CSVSpatialFormatType.PoseWithCov),
                     str(CSVSpatialFormatType.PoseWithCovTyped),
                     str(CSVSpatialFormatType.PoseErrorStamped),
                     str(CSVSpatialFormatType.PoseTypedStamped),
                     str(CSVSpatialFormatType.none)])

    @staticmethod
    def get_header(fmt):
        if str(fmt) == 'TUM':
            return ['#t', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw']
        else:
            return CSVSpatialFormatType.get_format(fmt)

    @staticmethod
    def get_format(fmt):
        if str(fmt) == 'Timestamp':
            return ['t']
        elif str(fmt) == 'TUM' or str(fmt) == 'PoseStamped':
            return ['t', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw']
        elif str(fmt) == 'PositionStamped':
            return ['t', 'tx', 'ty', 'tz']
        elif str(fmt) == 'PosOrientCov':
            return ['t', 'pxx', 'pxy', 'pxz', 'pyy', 'pyz', 'pzz', 'qrr', 'qrp', 'qry', 'qpp', 'qpy', 'qyy']
        elif str(fmt) == 'PosOrientWithCov':
            return ['t', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw', 'pxx', 'pxy', 'pxz', 'pyy', 'pyz', 'pzz', 'qrr',
                    'qrp', 'qry', 'qpp', 'qpy', 'qyy']
        elif str(fmt) == 'PosOrientWithCovTyped':
            return ['t', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw', 'pxx', 'pxy', 'pxz', 'pyy', 'pyz', 'pzz', 'qrr',
                    'qrp', 'qry', 'qpp', 'qpy', 'qyy', 'est_err_type', 'err_representation']
        elif str(fmt) == 'PoseCov':
            # R = Rz(y/c)Ry(b/p)Rx(r/a)
            # a  for roll (r)
            # b  for pitch (p)
            # c  for yaw (y - is already used for y-position of the frame)
            return ['t', 'Txx', 'Txy', 'Txz', 'Txa', 'Txb', 'Txc',
                    'Tyy', 'Tyz', 'Tya', 'Tyb', 'Tyc',
                    'Tzz', 'Tza', 'Tzb', 'Tzc',
                    'Taa', 'Tab', 'Tac',
                    'Tbb', 'Tbc',
                    'Tcc']
        elif str(fmt) == 'PoseWithCov':
            # R = Rz(y/c)Ry(b/p)Rx(r/a)
            # a  for roll (r)
            # b  for pitch (p)
            # c  for yaw (y - is already used for y-position of the frame)
            return ['t', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw',
                    'Txx', 'Txy', 'Txz', 'Txa', 'Txb', 'Txc',
                    'Tyy', 'Tyz', 'Tya', 'Tyb', 'Tyc',
                    'Tzz', 'Tza', 'Tzb', 'Tzc',
                    'Taa', 'Tab', 'Tac',
                    'Tbb', 'Tbc',
                    'Tcc']
        elif str(fmt) == 'PoseWithCovTyped':
            # R = Rz(y/c)Ry(b/p)Rx(r/a)
            # a  for roll (r)
            # b  for pitch (p)
            # c  for yaw (y - is already used for y-position of the frame)
            return ['t', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw',
                    'Txx', 'Txy', 'Txz', 'Txa', 'Txb', 'Txc',
                    'Tyy', 'Tyz', 'Tya', 'Tyb', 'Tyc',
                    'Tzz', 'Tza', 'Tzb', 'Tzc',
                    'Taa', 'Tab', 'Tac',
                    'Tbb', 'Tbc',
                    'Tcc',
                    'est_err_type', 'err_representation']
        elif str(fmt) == 'PoseTypedStamped':
            return ['t', 'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw', 'scale', 'est_err_type']
        elif str(fmt) == 'PoseErrorStamped':
            return ['t', 'nu_x', 'nu_y', 'nu_z', 'theta_x', 'theta_y', 'theta_z', 'est_err_type', 'err_representation']
        else:
            return ['no format']

    @staticmethod
    def parse(line, fmt):
        elems = line.split(",")
        if str(fmt) == 'Timestamp' or len(elems) == 1:
            return ps.sTimestamp(vec=[float(x) for x in elems[0:1]])
        elif str(fmt) == 'TUM' or str(fmt) == 'PoseStamped' or len(elems) == 8:
            return ps.sTUMPoseStamped(vec=[float(x) for x in elems[0:8]])
        elif str(fmt) == 'PositionStamped' or len(elems) == 4:
            return ps.sPositionStamped(vec=[float(x) for x in elems[0:4]])
        elif str(fmt) == 'PosOrientCov' or len(elems) == 13:
            return ps.sPosOrientCovStamped(vec=[float(x) for x in elems[0:13]])
        elif str(fmt) == 'PosOrientWithCov' or len(elems) == 20:
            return ps.sTUMPosOrientWithCovStamped(vec=[float(x) for x in elems[0:20]])
        elif str(fmt) == 'PosOrientWithCovTyped' or len(elems) == 22:
            return ps.sTUMPosOrientWithCovStampedTyped(vec=[float(x) for x in elems[0:20]],
                                                       est_type=elems[20], err_repr=elems[21])
        elif str(fmt) == 'PoseCov' or len(elems) == 22:
            return ps.sPoseCovStamped(vec=[float(x) for x in elems[0:22]])
        elif str(fmt) == 'PoseWithCov' or len(elems) == 29:
            return ps.sTUMPoseWithCovStamped(vec=[float(x) for x in elems[0:29]])
        elif str(fmt) == 'PoseWithCovTyped' or len(elems) == 31:
            return ps.sTUMPoseWithCovStampedTyped(vec=[float(x) for x in elems[0:29]],
                                                  est_type=elems[29], err_repr=elems[30])
        else:
            return None

    @staticmethod
    def header_to_format_type(header):
        header.replace(" ", "")
        header_parts = header.split(',')
        for fmt in CSVSpatialFormatType.list():
            format_type = CSVSpatialFormatType(fmt)
            # h_ = ",".join(CSVSpatialFormatType.get_header(fmt))
            h_parts = CSVSpatialFormatType.get_header(fmt)

            if len(header_parts) == len(h_parts):
                common = set(header_parts) & set(h_parts)
                if len(common) == len(header_parts):
                    return format_type

        return CSVSpatialFormatType.none

    @staticmethod
    def identify_format(fn):
        if os.path.exists(fn):
            assert(isinstance(fn, str))
            with open(fn, "r") as file:
                header = str(file.readline()).rstrip("\n\r")
                fmt = CSVSpatialFormatType.header_to_format_type(header)
                if fmt == CSVSpatialFormatType.none:
                    print("CSVSpatialFormatType.identify_format(): Header unknown!\n\t[" + str(header) + "]")
                return fmt
        else:
            print("CSVSpatialFormatType.identify_format(): File not found!\n\t[" + str(fn) + "]")
        return CSVSpatialFormatType.none


