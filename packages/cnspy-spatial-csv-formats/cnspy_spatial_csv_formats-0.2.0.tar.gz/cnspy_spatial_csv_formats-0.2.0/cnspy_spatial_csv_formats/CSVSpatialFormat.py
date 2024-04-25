#!/usr/bin/env python
# Software License Agreement (GNU GPLv3  License)
#
# Copyright (c) 2022, Roland Jung (roland.jung@aau.at) , AAU, KPK, NAV
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
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType
from cnspy_spatial_csv_formats.EstimationErrorType import EstimationErrorType
from cnspy_spatial_csv_formats.ErrorRepresentationType import ErrorRepresentationType


class CSVSpatialFormat:
    type = CSVSpatialFormatType.none
    estimation_error_type = EstimationErrorType.none
    rotation_error_representation = ErrorRepresentationType.none

    def __init__(self, fmt_type=None, est_err_type=None, err_rep_type= None):
        if fmt_type is not None and isinstance(fmt_type, CSVSpatialFormatType):
            self.type = fmt_type
        if est_err_type is not None and isinstance(est_err_type, EstimationErrorType):
            self.estimation_error_type = est_err_type
        if err_rep_type is not None and isinstance(err_rep_type, ErrorRepresentationType):
            self.rotation_error_representation = err_rep_type

    def get_header(self):
        return CSVSpatialFormatType.get_header(self.type, self.estimation_error_type, self.rotation_error_representation)

    def get_format(self):
        return CSVSpatialFormatType.get_format(self.type)

    @staticmethod
    def identify_format(fn):
        fmt, est_err, err_rep_type = CSVSpatialFormatType.identify_format(fn=fn)
        return CSVSpatialFormat(fmt, est_err_type=est_err, err_rep_type=err_rep_type)