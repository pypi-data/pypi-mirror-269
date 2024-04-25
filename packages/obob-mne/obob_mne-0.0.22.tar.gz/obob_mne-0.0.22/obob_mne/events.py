# -*- coding: UTF-8 -*-
# Copyright (c) 2018, Thomas Hartmann
#
# This file is part of the obob_mne Project, see:
# https://gitlab.com/obob/obob_mne
#
#    obob_mne is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    obob_mne is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with obob_subjectdb. If not, see <http://www.gnu.org/licenses/>.

import mne
import numpy as np


def filter_event_id(event_id, conditions):
    """Filter mne-python style event_ids.

    Parameters
    ----------
    event_id : dict
        The event_id
    conditions : str or list or tuple
        The conditions to keep

    Returns
    -------
    The filtered event_id

    """
    conditions = [conditions] if not isinstance(conditions,
                                                (list, tuple)) else conditions
    good_event_keys = mne.epochs._hid_match(event_id, conditions)

    new_event_id = {key: value for key, value in event_id.items() if
                    key in good_event_keys}
    return new_event_id


def read_events_from_analogue(raw, tolerance=1, trigger_channels=None):
    if trigger_channels is None:
        trigger_channels = ['STI001', 'STI002', 'STI003',
                            'STI004', 'STI005', 'STI006', 'STI007', 'STI008']

    trigger_data = raw[mne.pick_channels(raw.ch_names, trigger_channels)][0] / 5  # noqa

    bit_mult = 2 ** np.arange(0, trigger_data.shape[0])

    trigger_values = np.sum((trigger_data.T * bit_mult).T, axis=0).astype(int)

    trigger_idx = np.where(np.diff(trigger_values) > 0)[0] + 1
    tmp_events = np.zeros((trigger_idx.shape[0], 3))
    tmp_events[:, 0] = trigger_idx + raw.first_samp
    tmp_events[:, 2] = trigger_values[trigger_idx]

    bad_triggers_idx = np.where(np.diff(tmp_events[:, 0]) <= tolerance)[0]

    tmp_events[bad_triggers_idx + 1, 0] = tmp_events[bad_triggers_idx, 0]
    events = np.delete(tmp_events, bad_triggers_idx, axis=0)

    return events.astype(int)
