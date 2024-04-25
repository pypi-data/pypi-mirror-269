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
import numpy as np


class TimestampAssociation:
    def __init__(self):
        pass

    @staticmethod
    def get_closest(array, values):
        # from: https://stackoverflow.com/a/46184652
        # by: https://stackoverflow.com/users/1536499/anthonybell
        # make sure array is a numpy array
        array = np.array(array)
        values = np.array(values)
        # get insert positions
        idxs = np.searchsorted(array, values, side="left")

        # find indexes where previous index is closer
        prev_idx_is_less = ((idxs == len(array)) | (np.fabs(values - array[np.maximum(idxs - 1, 0)]) < np.fabs(
            values - array[np.minimum(idxs, len(array) - 1)])))
        idxs[prev_idx_is_less] -= 1

        return array[idxs], idxs

    @staticmethod
    def associate_timestamps(t_est, t_gt, offset=0.0, max_difference=0.02, round_decimals=9, unique_timestamps=True):
        # returns idx_est, idx_gt, t_est_matched, t_gt_matched
        swapped = False
        if len(t_est) > len(t_gt):
            t_vec1 = t_est + offset
            t_vec2 = t_gt
            swapped = True
        else:
            t_vec1 = t_gt
            t_vec2 = t_est + offset

        # round the timestamp arrays by N-decimals
        t_vec1 = np.round(t_vec1, decimals=round_decimals)
        t_vec2 = np.round(t_vec2, decimals=round_decimals)

        closest_t_vec1, idx_1 = TimestampAssociation.get_closest(t_vec1.transpose().ravel(), t_vec2.transpose().ravel())
        idx_2 = np.arange(0, len(idx_1), dtype=np.int32)

        if max_difference > 0:
            diff = np.abs(closest_t_vec1 - np.array(t_vec2.ravel()))
            mask_greater = np.where(diff >= max_difference)[0]
            idx_1 = np.delete(idx_1, mask_greater, axis=0)
            idx_2 = np.delete(idx_2, mask_greater, axis=0)

        t_vec_1_matched = t_vec1[idx_1]
        t_vec_2_matched = t_vec2[idx_2]

        # find uniques in both matched sets of timestamps
        if unique_timestamps:
            vec_1_matched_unique, unique_idx_1 = np.unique(t_vec_1_matched, return_index=True)
            vec_2_matched_unique, unique_idx_2 = np.unique(t_vec_2_matched, return_index=True)
            common_indices = np.intersect1d(unique_idx_1, unique_idx_2)

            idx_1 = idx_1[common_indices]
            idx_2 = idx_2[common_indices]
            t_vec_1_matched = t_vec1[idx_1]
            t_vec_2_matched = t_vec2[idx_2]

        # returns idx_est, idx_gt, t_est_matched, t_gt_matched
        if swapped:
            return idx_1, idx_2, t_vec_1_matched, t_vec_2_matched
        else:
            return idx_2, idx_1, t_vec_2_matched, t_vec_1_matched


