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

import sys
import obob_condor
import mne
import os
import mne.commands.mne_make_scalp_surfaces
from .utils.jobs import JobWithFreesurfer


class MakeSourceSpacesJob(JobWithFreesurfer):
    def run(self, subject_id):
        super(MakeSourceSpacesJob, self).run()
        src = mne.setup_source_space(subject_id,
                                     subjects_dir=self.subjects_dir,
                                     n_jobs=1)

        final_outpath = os.path.join(self.subjects_dir, subject_id, 'bem')
        mne.write_source_spaces(
            os.path.join(final_outpath, '%s-oct6-src.fif' % (subject_id,)),
            src, overwrite=True)

        bem_fname = os.path.join(final_outpath,
                                 '%s-complete-bem.fif' % (subject_id,))

        fs_avg_mri_path = os.path.join(self.subjects_dir, 'fsaverage', 'mri',
                                       'T1.mgz')
        vol_src = mne.setup_volume_source_space(subject_id,
                                                subjects_dir=self.subjects_dir,
                                                mri=fs_avg_mri_path,
                                                bem=bem_fname)

        mne.write_source_spaces(
            os.path.join(final_outpath, '%s-5mm-vol-src.fif' % (subject_id,)),
            vol_src, overwrite=True)

        vol_src = mne.setup_volume_source_space(subject_id,
                                                subjects_dir=self.subjects_dir,
                                                mri=fs_avg_mri_path,
                                                bem=bem_fname,
                                                pos=10)

        mne.write_source_spaces(
            os.path.join(final_outpath, '%s-10mm-vol-src.fif' % (subject_id,)),
            vol_src, overwrite=True)


def make_freesurfer_sourcespaces(subject_id):
    os.chdir('/mnt/obob/tmp')

    job_cluster = obob_condor.JobCluster(working_directory='/mnt/obob/tmp')
    job_cluster.add_job(MakeSourceSpacesJob, subject_id)

    job_cluster.submit()


def make_freesurfer_sourcespaces_cmd():
    subject_id = sys.argv[1]
    make_freesurfer_sourcespaces(subject_id)
