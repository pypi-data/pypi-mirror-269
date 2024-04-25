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
import time
from cnspy_spatial_csv_formats.CSVSpatialFormatType import CSVSpatialFormatType
from cnspy_csv2dataframe.CSV2DataFrame import CSV2DataFrame
from cnspy_csv2dataframe.PoseWithCovTyped2DataFrame import PoseWithCovTyped2DataFrame


SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

class PoseWithCov2DataFrame_Test(unittest.TestCase):
    start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        print("Process time: " + str((time.time() - self.start_time)))

    def load_(self):
        print('loading...')
        fn = str(SAMPLE_DATA_DIR + '/ID1-pose-est-pose-cov.csv')
        obj = PoseWithCovTyped2DataFrame(fn=fn)
        return obj

    def test_load_trajectory_from_CSV(self):
        obj = self.load_()
        self.assertTrue(obj.data_loaded)
        self.assertTrue(obj.format == CSVSpatialFormatType.PoseWithCovTyped)

        self.start()
        t_vec, p_vec, q_vec, P_vec_T, est_err_vec, err_rep_vec = PoseWithCovTyped2DataFrame.from_DataFrame(obj.data_frame)
        self.stop()

        print('est_err: ' + str(est_err_vec[1000]))
        print('err_rep: ' + str(err_rep_vec[1000]))
        print('P: ' + str(P_vec_T[1000]))
        print('p: ' + str(p_vec[1000]))
        print('q: ' + str(q_vec[1000]))


        df = PoseWithCovTyped2DataFrame.to_DataFrame(t_vec, p_vec, q_vec, P_vec_T, est_err_vec, err_rep_vec)
        print('keys: ' + str(df.keys().values))

if __name__ == "__main__":
    unittest.main()
