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
import subprocess
import obob_condor
import mne
import os
import mne.commands.mne_make_scalp_surfaces
from .utils.jobs import JobWithFreesurfer


class FreesurferBEMJob(JobWithFreesurfer):
    freesurfer_init = 'export FREESURFER_HOME=/mnt/obob/bin/freesurfer; ' \
                      'export SUBJECTS_DIR=/mnt/obob/freesurfer_subjects; ' \
                      'source $FREESURFER_HOME/SetUpFreeSurfer.sh; '

    watershed_prefloods = [25, 20, 30, 15, 35, 10, 40, 5, 45, 2, 50, 1, 55, 65,
                           70, 75, 80, 85, 90]

    extra_paths = ['/mnt/obob/bin/freesurfer/bin',
                   '/mnt/obob/bin/freesurfer/fsfast/bin',
                   '/mnt/obob/bin/freesurfer/tktools',
                   '/mnt/obob/bin/freesurfer/mni/bin']

    def run(self, subject_id):
        super(FreesurferBEMJob, self).run()
        subjects_dir = '/mnt/obob/freesurfer_subjects'

        is_running_file = os.path.join(subjects_dir, subject_id, 'scripts',
                                       'IsRunning.lh+rh')
        if os.path.exists(is_running_file):
            os.unlink(is_running_file)
        subprocess.check_call(
            [self.freesurfer_init +
             ' recon-all -make all -no-isrunning -s ' +
             subject_id], shell=True)

        final_outpath = os.path.join(subjects_dir, subject_id, 'bem')

        for cur_preflood in self.watershed_prefloods:
            mne.bem.make_watershed_bem(subject=subject_id,
                                       subjects_dir=subjects_dir, atlas='T1',
                                       overwrite=True, preflood=cur_preflood)

            with mne.utils.ArgvSetter(
                    ('-s', subject_id, '-n', '--force', '--overwrite')):
                mne.commands.mne_make_scalp_surfaces.run()

            try:
                bem = mne.make_bem_model(subject_id, subjects_dir=subjects_dir)
            except RuntimeError:
                pass
            else:
                break

        bem_fname = os.path.join(final_outpath,
                                 '%s-complete-bem.fif' % (subject_id,))
        mne.write_bem_surfaces(bem_fname, bem)

        bem_solution = mne.make_bem_solution(bem)
        bem_solution_fname = os.path.join(
            final_outpath, '%s-complete-bem-sol.fif' % (subject_id,))
        mne.write_bem_solution(bem_solution_fname, bem_solution)


def make_freesurfer_bem(subject_id):
    os.chdir('/mnt/obob/tmp')

    job_cluster = obob_condor.JobCluster(working_directory='/mnt/obob/tmp')
    job_cluster.add_job(FreesurferBEMJob, subject_id)

    job_cluster.submit()


def make_freesurfer_bem_cmd():
    subject_id = sys.argv[1]
    make_freesurfer_bem(subject_id)
