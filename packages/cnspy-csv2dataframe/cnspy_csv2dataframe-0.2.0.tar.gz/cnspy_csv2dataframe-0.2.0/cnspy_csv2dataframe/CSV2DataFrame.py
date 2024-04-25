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
# Requirements:
# sudo pip install numpy pandas
########################################################################################################################
import os
import math
import pandas as pandas
import numpy as np
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType


class CSV2DataFrame:
    format = CSVSpatialFormatType.none
    data_frame = None
    data_loaded = False
    fn = None

    def __init__(self, fn=None, fmt=None):
        # fmt allows manually overwrite expected format to be parsed into dataframe
        if fn is not None:
            self.load_from_CSV(fn=fn, fmt_type=fmt)

    def subsample(self, step=None, num_max_points=None, verbose=False):
        if self.data_loaded:
            self.data_frame = CSV2DataFrame.subsample_DataFrame(self.data_frame, step=step,
                                                                num_max_points=num_max_points,
                                                                verbose=verbose)
        else:
            print("CSV2DataFrame: data was not loaded!")

    def load_from_CSV(self, fn, fmt_type=None):
        if os.path.exists(fn):
            # if the format is still not known it cannot be loaded, if it is None than it will be identified
            self.data_frame, self.format = CSV2DataFrame.load_CSV(filename=fn, fmt=fmt_type)
            self.fn = fn
            self.data_loaded = True
            return True
        else:
            print("CSV2DataFrame.load_from_CSV(): file does not exist: {0}".format(fn))

        # default assignment
        self.data_frame = None
        self.fn = None
        self.data_loaded = False
        self.format = CSVSpatialFormatType.none
        return False

    def save_to_CSV(self, fn, fmt=None):
        if self.data_loaded:
            CSV2DataFrame.save_CSV(data_frame=self.data_frame, filename=fn, fmt=fmt)
        else:
            print("CSV2DataFrame: data was not loaded!")

    @staticmethod
    def identify_format(dataframe):
        if isinstance(dataframe, pandas.DataFrame):
            return CSVSpatialFormatType.header_to_format_type(','.join(dataframe.keys().values))
        return CSVSpatialFormatType.none

    @staticmethod
    def load_CSV(filename, fmt=None):
        if isinstance(fmt, CSVSpatialFormatType) and fmt is not CSVSpatialFormatType.none:
            data = pandas.read_csv(filename, sep='\s+|\,', comment='#', header=None,
                                   names=CSVSpatialFormatType.get_format(fmt),
                                   engine='python')
        else:
            data = pandas.read_csv(filename, sep='\s+|\,', comment='#',
                                   engine='python')
            fmt = CSV2DataFrame.identify_format(data)
        return data, fmt

    @staticmethod
    def save_CSV(data_frame, filename, fmt=None, save_index=False):
        head = os.path.dirname(os.path.abspath(filename))
        if not os.path.exists(head):
            os.makedirs(head)

        if isinstance(fmt, CSVSpatialFormatType) and fmt is not CSVSpatialFormatType.none:
            data_frame.to_csv(filename, sep=',', index=save_index,
                              header=CSVSpatialFormatType.get_header(fmt),
                              columns=CSVSpatialFormatType.get_format(fmt))
        else:
            data_frame.to_csv(filename, sep=',', index=save_index)

    @staticmethod
    def subsample_DataFrame(df, step=None, num_max_points=None, verbose=False):

        num_elems = len(df.index)

        if num_max_points:
            step = 1
            if (int(num_max_points) > 0) and (int(num_max_points) < num_elems):
                step = int(math.ceil(num_elems / float(num_max_points)))

        sparse_indices = np.arange(start=0, stop=num_elems, step=step)

        if num_max_points or step:
            if verbose:
                print("CSV2DataFrame.subsample_DataFrame():")
                print("* len: " + str(num_elems) + ", max_num_points: " + str(
                    num_max_points) + ", subsample by: " + str(step))

            return CSV2DataFrame.sample_DataFrame(df, sparse_indices)
        else:
            return df

    @staticmethod
    def sample_DataFrame(df, indices_arr):
        num_elems = len(df.index)
        assert (len(indices_arr) <= num_elems), "CSV2DataFrame.sample_DataFrame():\n\t index array must be smaller " \
                                                    "equal the dataframe."
        assert (max(indices_arr) <= num_elems), "CSV2DataFrame.sample_DataFrame():\n\t elements in the index array " \
                                                    "must be smaller equal the dataframe."
        assert (min(indices_arr) >= 0), "CSV2DataFrame.sample_DataFrame():\n\t elemts in the index array " \
                                                    "must be greater equal zero."

        df_sub = df.iloc[indices_arr]
        df_sub.reset_index(inplace=True, drop=True)
        return df_sub
