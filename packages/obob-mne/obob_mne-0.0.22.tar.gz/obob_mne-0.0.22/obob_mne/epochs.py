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
import obob_mne.events
import scipy


def collapse_conditions(epochs, keep_condition):
    """Merge conditions in event_id.

    Supposed we have an event_id like this:

    ``
    event_id = ['attention:audio/stim:audio',
                'attention:visual/stim:audio',
                'attention:audio/stim:visual',
                'attention:visual/stim:visual']
    ``

    And we want to compare the two stim conditions, ignoring the attention
    factor. Then we use this function:

    .. code-block:: python

        event_id = collapse_conditions(epochs, 'stim')

    Parameters
    ----------
    epochs : :class:`mne.Epochs`
        The  :class:`mne.Epochs` to modify
    keep_condition : str
        The factor to keep

    Returns
    -------
    epochs : :class:`mne.Epochs`
        The modified instance

    """
    epochs = epochs.copy()
    all_factors = list()
    collapsed_factors = list()
    for cur_key in epochs.event_id.keys():
        all_factors += [x for x in cur_key.split('/') if keep_condition in x]
        collapsed_factors += [x for x in cur_key.split('/') if
                              keep_condition not in x]

    all_factors = set(all_factors)

    new_event_id = dict()
    for idx, cur_factor in enumerate(all_factors):
        this_id = idx
        while this_id in epochs.events[:, 2]:
            this_id += 1

        all_values = obob_mne.events.filter_event_id(epochs.event_id,
                                                     cur_factor).values()

        epochs.events = mne.merge_events(events=epochs.events,
                                         ids=all_values,
                                         new_id=this_id,
                                         replace_events=True)
        new_event_id[cur_factor] = this_id

    epochs.event_id = new_event_id
    epochs.info['collapsed_factors'] = '/'.join(set(collapsed_factors))

    return epochs


def diff_collapsed_conditions(epochs_list):
    """No idea."""
    all_collapsed_factors = [x.info['collapsed_factors'] for x in epochs_list]

    for cur_epochs in epochs_list:
        cur_collapsed = cur_epochs.info['collapsed_factors']
        cur_coll_set = set(cur_collapsed.split('/'))

        for cur_cmp_epoch, cur_original_factors in zip(epochs_list,
                                                       all_collapsed_factors):
            if not cur_epochs == cur_cmp_epoch:
                cur_cmp_set = set(cur_original_factors.split('/'))
                cur_coll_set -= cur_cmp_set

        cur_epochs.info['collapsed_factors'] = '/'.join(cur_coll_set)


def no_diff_collapsed_conditions(epochs_list):
    """No idea."""
    all_collapsed_factors = [x.info['collapsed_factors'] for x in epochs_list]
    collapsed_factors_set = [set(x.split('/')) for x in all_collapsed_factors]

    final_set = collapsed_factors_set[0]

    for cur_set in collapsed_factors_set[1:]:
        final_set -= cur_set


def zscore_epochs(epoch):
    data = epoch.get_data()
    data = data.swapaxes(0, 1)

    original_shape = data.shape

    data = data.reshape((data.shape[0], -1))
    data = scipy.stats.zscore(data, 1)

    data = data.reshape(original_shape)
    data = data.swapaxes(0, 1)

    epoch._data = data

    return epoch
