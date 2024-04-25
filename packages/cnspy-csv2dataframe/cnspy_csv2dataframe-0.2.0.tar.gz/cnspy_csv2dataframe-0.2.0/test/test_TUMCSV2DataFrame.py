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
import numpy as np
from cnspy_csv2dataframe.TUMCSV2DataFrame import TUMCSV2DataFrame
from cnspy_csv2dataframe.CSV2DataFrame import CSV2DataFrame
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

class TUMCSVdata_Test(unittest.TestCase):
    def load_sample_data_frame(self):
        return TUMCSV2DataFrame(fn=str(SAMPLE_DATA_DIR + '/ID1-pose-gt.csv'))

    def test_load_from_CSV(self):
        print('loading...')
        d = self.load_sample_data_frame()
        self.assertTrue(d.data_loaded)

        d = TUMCSV2DataFrame(fn='no file')
        self.assertFalse(d.data_loaded)

    def test_data_to_numpy_dict(self):
        d = self.load_sample_data_frame()
        np_dict = TUMCSV2DataFrame.DataFrame_to_numpy_dict(d.data_frame)

        self.assertTrue(len(np_dict['t']) > 100)

    def test_data_to_tqp(self):
        d = self.load_sample_data_frame()
        t_vec, p_vec, q_vec = TUMCSV2DataFrame.from_DataFrame(d.data_frame)

        self.assertTrue(len(t_vec) > 0)
        self.assertTrue(len(t_vec) == len(p_vec))

    def test_tpq_to_data_frame(self):
        p_vec = np.array([[21, 72, 67],
                          [23, 78, 69],
                          [32, 74, 56],
                          [52, 54, 76]])
        q_vec = np.array([[0, 0, 0, 1],
                          [0, 0, 0, 1],
                          [0, 0, 0, 1],
                          [0, 0, 0, 1]])
        t_vec = np.array([[0],
                          [1],
                          [2],
                          [3]])
        df = TUMCSV2DataFrame.to_DataFrame(t_vec, p_vec, q_vec)
        print(str(df))
        CSV2DataFrame.save_CSV(data_frame=df, filename=str(SAMPLE_DATA_DIR + '/results/any.csv'), fmt=CSVSpatialFormatType.TUM)

    def test_subsample_DataFrame(self):
        d = self.load_sample_data_frame()

        num_samples = 200
        df_sub = TUMCSV2DataFrame.subsample_DataFrame(d.data_frame, num_max_points=200, verbose=True)

        self.assertTrue(len(df_sub.index) <= num_samples)

        CSV2DataFrame.save_CSV(data_frame=df_sub, filename=str(SAMPLE_DATA_DIR + '/results/gt_sub_200.csv'),
                               fmt=CSVSpatialFormatType.TUM)


if __name__ == "__main__":
    unittest.main()
