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

from codecs import open

import os.path
from setuptools import setup, find_packages

# find the location of this file
this_directory = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get the Module Version from the VERSION file
with open(os.path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

# define required modules
required = ['mne', 'scipy', 'numpy', 'obob_condor', 'pandas']

setup(
    name='obob_mne',
    packages=find_packages(),
    url='https://gitlab.com/obob/obob_mne',
    version=version,
    description='I am obob_mne',
    long_description=long_description,
    license='GPL3',
    author='Thomas Hartmann',
    author_email='thomas.hartmann@th-ht.de',
    install_requires=required,
    entry_points={
                'console_scripts': [
                        'import_subject_to_freesurfer=obob_mne.mri.cmd.import_subject:import_subject',
                        'make_freesurfer_bem=obob_mne.mri.cmd.make_freesurfer_bem:make_freesurfer_bem_cmd',
                        'make_freesurfer_sourcespaces=obob_mne.mri.cmd.make_source_space:make_freesurfer_sourcespaces_cmd'
                        ]
                }
)
