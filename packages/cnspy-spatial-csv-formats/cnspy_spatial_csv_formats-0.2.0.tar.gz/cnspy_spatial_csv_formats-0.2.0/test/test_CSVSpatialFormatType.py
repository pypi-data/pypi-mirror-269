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
import unittest
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType
from cnspy_spatial_csv_formats.EstimationErrorType import EstimationErrorType
from cnspy_spatial_csv_formats.ErrorRepresentationType import ErrorRepresentationType

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

class CSVFormat_Test(unittest.TestCase):
    def test_header(self):
        print('TUM CSV header:')
        for type in CSVSpatialFormatType.list():
            print(str(CSVSpatialFormatType.get_header(type)))

    def test_get_format(self):
        print('TUM CSV get_format:')
        for type in CSVSpatialFormatType.list():
            print(str(CSVSpatialFormatType.get_format(type)))

    def test_identify(self):
        fmt= CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-err.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PoseStamped)

        fmt= CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-est.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PoseStamped)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PosOrientWithCovTyped)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-est-pose-cov.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PoseWithCovTyped)
        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-gt.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PoseStamped)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/example_eval.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.none)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/212341234.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.none)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/t_est.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.Timestamp)

        fmt= CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov-type1-thetaR.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PosOrientWithCovTyped)


        fmt= CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov-type1-thetaR-anyorder.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PosOrientWithCovTyped)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/ID1-pose-est-posorient-cov-type2-thetaq.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PosOrientWithCovTyped)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/test-pos2csv.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PositionStamped)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/test-pose2csv.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PoseStamped)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/test-pos_orient_withcov2csv.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PosOrientWithCov)

        fmt = CSVSpatialFormatType.identify_format(str(SAMPLE_DATA_DIR + '/test-posewithcov2csv.csv'))
        print('identify_format:' + str(fmt))
        self.assertTrue(fmt == CSVSpatialFormatType.PoseWithCov)



if __name__ == '__main__':
    unittest.main()
