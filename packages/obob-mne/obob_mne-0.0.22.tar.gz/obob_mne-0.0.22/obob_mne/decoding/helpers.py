# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the obob_mne Project, see:
# https://gitlab.com/obob/obob_mne
#
# obob_mne is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# obob_mne is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with obob_mne. If not, see <http://www.gnu.org/licenses/>.

import numpy as np


def _get_Y_from_metadata(data, query_list):
    n_epochs = len(data)

    y = np.zeros(n_epochs)
    my_metadata = data.metadata.reset_index()

    for idx, cur_query in enumerate(query_list):
        epochs_idx = my_metadata.query(cur_query).index
        y[epochs_idx] = idx + 1

    if np.any(y == 0):
        raise RuntimeError('Not all of the epochs were selected!')

    return y
