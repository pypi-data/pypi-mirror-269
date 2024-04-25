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
import unittest
from cnspy_csv2dataframe.TimestampCSV2DataFrame import TimestampCSV2DataFrame

class TimestampCSV2DataFrame_Test(unittest.TestCase):
    def load_sample_data_frame(self):
        return TimestampCSV2DataFrame(fn='./sample_data/t_est.csv')

    def test_get_t_vec(self):
        dut = self.load_sample_data_frame()
        self.assertTrue(dut.data_loaded)
        t_vec = dut.get_t_vec()
        self.assertTrue(len(t_vec) > 0)

    def test_save_to_CSV(self):
        dut = self.load_sample_data_frame()
        self.assertTrue(dut.data_loaded)
        dut.save_to_CSV(fn='./sample_data/results/t_est_copy.csv')


if __name__ == "__main__":
    unittest.main()
