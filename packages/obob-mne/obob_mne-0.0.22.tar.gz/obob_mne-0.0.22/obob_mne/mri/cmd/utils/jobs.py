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

import obob_condor
import os


class JobWithFreesurfer(obob_condor.Job):
    freesurfer_init = 'export FREESURFER_HOME=/mnt/obob/bin/freesurfer; ' \
                      'export SUBJECTS_DIR=/mnt/obob/freesurfer_subjects; ' \
                      'source $FREESURFER_HOME/SetUpFreeSurfer.sh; '

    extra_paths = ['/mnt/obob/bin/freesurfer/bin',
                   '/mnt/obob/bin/freesurfer/fsfast/bin',
                   '/mnt/obob/bin/freesurfer/tktools',
                   '/mnt/obob/bin/freesurfer/mni/bin']

    subjects_dir = '/mnt/obob/freesurfer_subjects'

    def run(self):
        os.environ['FREESURFER_HOME'] = '/mnt/obob/bin/freesurfer'
        os.environ['PATH'] = ':'.join([
            os.environ['PATH'],
            ':'.join(self.extra_paths)])
        os.environ['SUBJECTS_DIR'] = self.subjects_dir
