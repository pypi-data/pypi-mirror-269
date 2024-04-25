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

import os
import zipfile
import shutil
import subprocess
import sys
import tempfile
import glob


def import_subject():
    full_file_name = sys.argv[1]
    f_name = os.path.basename(full_file_name)
    subject_id = f_name[0:12]

    tmp_folder = tempfile.mkdtemp()
    with zipfile.ZipFile(full_file_name, 'r') as mri_zip:
        mri_zip.extractall(tmp_folder)

    first_file = glob.glob(os.path.join(tmp_folder, '*'))[0]
    subprocess.call(['source /etc/profile.d/zz_activate_freesurfer.sh; '
                     'recon-all -i ' + first_file + ' -s ' + subject_id],
                    shell=True)

    shutil.rmtree(tmp_folder)
