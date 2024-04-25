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
from copy import deepcopy

import mne
import os
import logging
import glob
import numpy as np
import re
import obob_mne.events
import pandas as pd
import mne.io.fiff


class LoadFromSinuhe(mne.io.fiff.Raw):
    """:class:`mne.io.Raw` mixin to facilitate loading data from sinuhe.

    By including this mixin in your study specific ``Raw`` class, you can
    facilitate loading the raw data files.

    Supposed your fif files follow the usual pattern: '19800908igdb_run01.fif',
    you can define a ``Raw`` class like this one:

    .. code-block:: python

        class Raw(mne.io.fiff.Raw, LoadFromSinuhe):
            study_acronym = 'test_study'

    Loading run 2 of subject '19800908igdb' can then be done like this:

    .. code-block:: python

        raw_data = Raw(subject_id='19800908igdb', block_nr=2, preload=True)

    """

    sinuhe_root = '/mnt/sinuhe/data_raw'
    study_acronym = None
    file_glob_patterns = [
        '%s_run%02d.fif',
        '%s_block%02d.fif',
        '%s_run%d.fif',
        '%s_block%d.fif'
    ]

    excluded_subjects = None
    replace_subject_ids = dict()

    subject_id_regex = r'^[1-2][0-9]{7}[a-z]{4}$'

    def __init__(self, subject_id, block_nr=None, **kwargs):
        if not self.study_acronym:
            raise ValueError('You must set the study_acronym parameter!')

        if not os.path.isdir(
                os.path.join(self.sinuhe_root, self.study_acronym)):
            raise ValueError('Cannot find your study on sinuhe!')

        if os.path.isfile(subject_id):
            logging.info('A filename was submitted. Loading...')
            final_fname = subject_id
        else:
            final_fname = self.get_fif_filename(subject_id, block_nr)

        super(LoadFromSinuhe, self).__init__(final_fname, **kwargs)

    @classmethod
    def get_all_subjects(cls):
        """Return a list of all subjects in the study.

        Returns
        -------
        all_subjects : list
            A list of strings with all subjects codes found.
        """
        if not cls.study_acronym:
            raise ValueError('You must set the study_acronym parameter!')

        if not os.path.isdir(os.path.join(cls.sinuhe_root, cls.study_acronym)):
            raise ValueError('Cannot find your study on sinuhe!')

        study_folder = os.path.join(cls.sinuhe_root, cls.study_acronym)
        all_fif_files = glob.glob(
            os.path.join(study_folder, '*', '*', '*.fif'))
        all_fif_files = [os.path.basename(x) for x in all_fif_files]
        all_subjects = set([x[0:12] for x in all_fif_files if
                            re.match(cls.subject_id_regex, x[0:12])])

        if cls.excluded_subjects:
            all_subjects -= set(cls.excluded_subjects)

        if cls.replace_subject_ids:
            all_subjects -= set(cls.replace_subject_ids.keys())

        return all_subjects

    @classmethod
    def get_number_of_runs(cls, subject_id):
        """Return the number of runs for the given subject.

        Parameters
        ----------
        subject_id : str
            The subject id

        Returns
        -------
        n_runs : int
            The number of runs for the subject.
        """
        n_runs = 1
        while cls.get_fif_filename(subject_id, n_runs) is not None:
            n_runs += 1

        return n_runs - 1

    @classmethod
    def get_fif_filename(cls, subject_id, run_nr):
        """Find the fif file for the subject and run.

        Parameters
        ----------
        subject_id : str
            The subject id
        run_nr : int
            The run number

        Returns
        -------
        fname : str
            The filename of the respective fif file

        """
        if not cls.study_acronym:
            raise ValueError('You must set the study_acronym parameter!')

        if not os.path.isdir(os.path.join(cls.sinuhe_root, cls.study_acronym)):
            raise ValueError('Cannot find your study on sinuhe!')

        study_folder = os.path.join(cls.sinuhe_root, cls.study_acronym)

        all_subject_ids = (subject_id.lower(), subject_id.upper())

        if cls.replace_subject_ids:
            if set(all_subject_ids) & set(cls.replace_subject_ids.values()):
                tmp_all_ids = all_subject_ids
                for cur_subject_id in set(tmp_all_ids) & set(
                        cls.replace_subject_ids.values()):
                    idx = list(cls.replace_subject_ids.values()).index(
                        cur_subject_id)
                    all_subject_ids += (list(
                        cls.replace_subject_ids.keys())[idx],)

        fname = None
        for cur_subject_id in all_subject_ids:
            if cls.excluded_subjects:
                if cur_subject_id in cls.excluded_subjects:
                    raise ValueError(
                        'Subject %s is excluded!' % (cur_subject_id,))

            for cur_glob_pattern in cls.file_glob_patterns:
                tmp_result = glob.glob(
                    os.path.join(
                        study_folder, '*', '*',
                        cls.get_glob_pattern(
                            cur_glob_pattern, cur_subject_id, run_nr
                        )
                    )
                )
                if tmp_result:
                    fname = tmp_result[-1]

        return fname

    @classmethod
    def get_glob_pattern(cls, cur_glob_pattern, cur_subject_id, run_nr):
        if run_nr is not None:
            return cur_glob_pattern % (cur_subject_id, run_nr)
        else:
            return cur_glob_pattern % (cur_subject_id, )


class AdvancedEvents(mne.io.fiff.Raw):
    """Integrate event loading and handling into :class:`mne.io.Raw`.

    Including this mixin in your study specific ``Raw`` class provides event
    handling features directly in that class.

    More specifically, it provides three extra properties:

    1. events
    2. event_id
    3. evt_metadata

    Which are automatically filled and kept up-to-date. They correspond to
    the respective meaning in :class:`mne.Epochs`.

    You can also create a subclass of this class and use
    :meth:`_process_events` to process the events (fill the event_id,
    modify the event codes....)
    """

    trigger_min_duration = 9e-3

    def __init__(self, *args, **kwargs):
        self._events = None
        self._event_id = None
        self._evt_metadata = None

        super(AdvancedEvents, self).__init__(*args, **kwargs)
        self._load_events()

    def _load_events(self):
        self._event_id = dict()
        self._events = mne.find_events(self,
                                       min_duration=self.trigger_min_duration)

        self._process_events()

    def _process_events(self):
        pass

    def get_filtered_event_id(self, condition_filter):
        """Return a filtered version of the event_id field.

        Refer to :meth:`obob_mne.events.filter_event_id` for further
        details.
        """
        return obob_mne.events.filter_event_id(self.event_id, condition_filter)

    def has_filtered_events(self, condition_filter):
        """Check whether the event_ids are present.

        Parameters
        ----------
        condition_filter : str
            The event_ids to check

        Returns
        -------
        has_events : bool
            True if the filtered events are present.

        """
        try:
            self.get_filtered_event_id(condition_filter)
        except KeyError:
            return False

        return len(self.get_filtered_event_id(condition_filter)) > 0

    def resample(self, *args, **kwargs):
        """Resample the data and reloads the events.

        For the rest, refer to :meth:`mne.io.Raw.resample`.

        """
        self._events = None
        self._event_id = None
        self._evt_metadata = None

        super(AdvancedEvents, self).resample(*args, **kwargs)
        self._load_events()

    @property
    def events(self):
        """:class:`numpy.ndarray`: The event matrix."""
        if not isinstance(self._events, np.ndarray):
            self._load_events()

        return self._events

    @property
    def event_id(self):
        """dict: The event_ids"""
        if not isinstance(self._events, np.ndarray):
            self._load_events()

        return self._event_id

    @property
    def evt_metadata(self):
        """:class:`pandas.DataFrame`: The metadata"""
        if not isinstance(self._events, np.ndarray):
            self._load_events()

        return self._evt_metadata


class AutomaticBinaryEvents(AdvancedEvents):
    """Mixin for binary events.

    If your triggers code events with binary triggers, this mixin can help you
    a lot.

    Let's suppose, you have an experiment with two types of blocks.
    At the beginning of each block, the type of the block is signalled by a
    a trigger code:

    1. Attend Auditory: Trigger 1
    2. Attend Visual: Trigger 2

    Then you present either:

    1. A tone: Trigger 4
    2. An image: Trigger 8

    And sometimes, one of them is an oddball which is marked by adding 1 to
    the trigger codes.

    In this case, you can use this mixin and write something like this:

    .. code-block:: python

        class Raw(mne.io.fiff.Raw, LoadFromSinuhe, AutomaticBinaryEvents):
            study_acronym = 'test_study'

            condition_triggers = {
                'attention': {
                    'auditory': 1,
                    'visual': 2
                }
            }

            stimulus_triggers = {
                'modality': {
                    'audio': 4,
                    'visual': 8
                },
                'oddball': 1
            }

    This will automatically result in mne-python aware event_ids like:

    ``'attention:visual/modality:audio/oddball:True'``

    """

    condition_triggers = None
    stimulus_triggers = None

    def __init__(self, *args, **kwargs):

        if not isinstance(self.stimulus_triggers, dict):
            raise ValueError('Please set stimulus_triggers to a dictionary')

        super(AutomaticBinaryEvents, self).__init__(*args, **kwargs)

    def _decode_bin_trigger(self, trigger_value, trigger_dict_item):
        if isinstance(trigger_dict_item, dict):
            for key, value in trigger_dict_item.items():
                if trigger_value & value:
                    return key
        else:
            if trigger_value & trigger_dict_item:
                return 'yes'
            else:
                return 'no'

    def _process_events(self):
        super(AutomaticBinaryEvents, self)._process_events()

        conditions_string_list = list()
        conditions_metadata = {}
        all_raw_metadata = []

        if self.condition_triggers:
            condition_trigger = self._events[0, 2]
            self._events = np.delete(self._events, (0), axis=0)

            for allcond_key, allcond_value in self.condition_triggers.items():
                decoded_trigger = self._decode_bin_trigger(condition_trigger,
                                                           allcond_value)
                conditions_string_list.append(
                    '%s:%s' % (allcond_key, decoded_trigger))
                conditions_metadata[allcond_key] = decoded_trigger

        all_event_codes = np.unique(self._events[:, 2])
        original_events = self._events.copy()

        for cur_code in all_event_codes:
            cur_string_list = list(conditions_string_list)

            for stim_group_name, stim_group_choices in \
                    self.stimulus_triggers.items():
                cur_string_list.append('%s:%s' % (stim_group_name,
                                                  self._decode_bin_trigger(
                                                      cur_code,
                                                      stim_group_choices)))

            new_event_key = '/'.join(cur_string_list)
            new_event_code = np.mod(np.abs(hash(new_event_key)), 4000)
            self._event_id[new_event_key] = new_event_code
            self._events[self._events[:, 2] == cur_code, 2] = new_event_code

        for cur_evt_code in original_events[:, 2]:
            cur_metadata = deepcopy(conditions_metadata)
            for stim_group_name, stim_group_choices in \
                    self.stimulus_triggers.items():
                cur_metadata[stim_group_name] = self._decode_bin_trigger(
                    cur_evt_code, stim_group_choices
                )

            all_raw_metadata.append(cur_metadata)

        self._evt_metadata = pd.DataFrame(all_raw_metadata)


class AutomaticBinaryEventsWithMetadata(AutomaticBinaryEvents):
    """Mixin for binary events with metadata.

    """
    def _process_events(self):
        super(AutomaticBinaryEvents, self)._process_events()

        conditions_metadata = {}
        all_raw_metadata = []

        if self.condition_triggers:
            condition_trigger = self._events[0, 2]
            self._events = np.delete(self._events, (0), axis=0)

            for allcond_key, allcond_value in self.condition_triggers.items():
                conditions_metadata[allcond_key] = self._decode_bin_trigger(
                    condition_trigger,
                    allcond_value
                )

        for cur_evt_code in self._events[:, 2]:
            cur_metadata = deepcopy(conditions_metadata)
            for stim_group_name, stim_group_choices in \
                    self.stimulus_triggers.items():
                cur_metadata[stim_group_name] = self._decode_bin_trigger(
                    cur_evt_code, stim_group_choices
                )

            all_raw_metadata.append(cur_metadata)

        self._evt_metadata = pd.DataFrame(all_raw_metadata)
