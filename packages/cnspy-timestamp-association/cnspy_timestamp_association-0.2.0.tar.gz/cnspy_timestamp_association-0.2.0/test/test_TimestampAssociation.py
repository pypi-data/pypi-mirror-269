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
import csv
from cnspy_csv2dataframe.TimestampCSV2DataFrame import TimestampCSV2DataFrame
from cnspy_timestamp_association.TimestampAssociation import TimestampAssociation

SAMPLE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

class TimestampAssociation_Test(unittest.TestCase):
    start_time = None

    def tuple_list_2_csv(self, d, fn):
        with open(fn, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['idx1', 'idx2'])
            for row in d:
                writer.writerow(row)

    def load_data(self):
        df_t_est = TimestampCSV2DataFrame(
            fn=str(SAMPLE_DATA_DIR + '/t_est.csv'))
        df_t_gt = TimestampCSV2DataFrame(
            fn=str(SAMPLE_DATA_DIR + '/t_gt.csv'))

        return df_t_est, df_t_gt

    def start(self):
        self.start_time = time.time()

    def stop(self):
        print("Process time: " + str((time.time() - self.start_time)))

    def test_load_from_CSV(self):
        df_t_est, df_t_gt = self.load_data()
        self.assertTrue(len(df_t_est.get_t_vec()) > 0)
        self.assertTrue(len(df_t_gt.get_t_vec()) > 0)

    def test_associate_1(self):
        df_t_est, df_t_gt = self.load_data()

        t_est = df_t_est.get_t_vec()
        t_gt = df_t_gt.get_t_vec()

        self.start()
        idx_est, idx_gt, t_est_matched, t_gt_matched = TimestampAssociation.associate_timestamps(
            t_est,
            t_gt)

        matches2 = zip(idx_est, idx_gt)
        self.stop()
        # takes: 0.5sec
        self.tuple_list_2_csv(d=matches2, fn=str(SAMPLE_DATA_DIR + '/matches.txt'))


if __name__ == "__main__":
    unittest.main()
