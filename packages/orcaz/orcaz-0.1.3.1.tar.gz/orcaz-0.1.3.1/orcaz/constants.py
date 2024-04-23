#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# **********************************************************************************************************************
# File: constants.py
# Project: ORCA
# Created: April 11, 2023, 12:25h
# Author: Lalith Kumar Shiyam Sundar
# Email: lalith.shiyamsundar@meduniwien.ac.at
# Institute: Quantitative Imaging and Medical Physics, Medical University of Vienna
# Description: This module contains the constants for the wolfz.
# License: Apache 2.0
# **********************************************************************************************************************

# Importing required libraries

import os
from datetime import datetime
from orcaz import file_utilities

project_root = file_utilities.get_virtual_env_root()
BINARY_PATH = os.path.join(project_root, 'bin')
MODEL_PATH = os.path.join(project_root, 'models')

# Set the paths to the binaries based on the operating system
if file_utilities.get_system()[0] == 'windows':
    GREEDY_PATH = os.path.join(BINARY_PATH, f'falcon-{file_utilities.get_system()[0]}-{file_utilities.get_system()[1]}',
                               'greedy.exe')
    C3D_PATH = os.path.join(BINARY_PATH, f'falcon-{file_utilities.get_system()[0]}-{file_utilities.get_system()[1]}',
                            'c3d.exe')
    DCM2NIIX_PATH = os.path.join(BINARY_PATH,
                                 f'falcon-{file_utilities.get_system()[0]}-{file_utilities.get_system()[1]}',
                                 'dcm2niix.exe')

elif file_utilities.get_system()[0] in ['linux', 'mac']:
    GREEDY_PATH = os.path.join(BINARY_PATH, f'falcon-{file_utilities.get_system()[0]}-{file_utilities.get_system()[1]}',
                               'greedy')
    C3D_PATH = os.path.join(BINARY_PATH, f'falcon-{file_utilities.get_system()[0]}-{file_utilities.get_system()[1]}',
                            'c3d')
    DCM2NIIX_PATH = os.path.join('/home/zach/software/dcm2niix/build/bin/dcm2niix')

# COLOR CODES
ANSI_ORANGE = '\033[38;5;208m'
ANSI_GREEN = '\033[38;5;40m'
ANSI_BLUE = '\033[1;94m'
ANSI_RESET = '\033[0m'
ANSI_VIOLET = '\033[38;5;141m'

# SUPPORTED TRACERS (limited patch)
TRACER_FDG = 'FDG'

# FILE NAMES
RESAMPLED_PREFIX = 'resampled_toPET'
ALIGNED_PREFIX = 'ORCA_aligned_'

# DIRECTORY
ORCA_WORKING_FOLDER = 'ORCA-V01'+'-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
TRANSFORMS_FOLDER = 'transforms'
ALIGNED_CT_FOLDER = 'ORCA_aligned_CT'

# MOOSE PARAMETERS
MOOSE_MODEL = "clin_ct_body"
MOOSE_PREFIX = 'CT_Body_'
MOOSE_LABEL_INDEX = {
        1: "Legs",
        2: "Body",
        3: "Head",
        4: "Arms"
    }
ACCELERATOR = 'cuda'


# EXPECTED MODALITIES
MODALITIES = ['PET', 'CT']
ANATOMICAL_MODALITIES = ['CT']
ANATOMICAL_MODALITIES_SUFFIX = ['_CT']
FUNCTIONAL_MODALITIES = ['PT']
FUNCTIONAL_MODALITIES_SUFFIX = ['_PT']

# EXPECTED PET TYPES (ac, non-ac)
PET_TYPE_AC = ['AC']
PET_TYPE_AC_SUFFIX = ['_AC']
PET_TYPE_NAC = ['NAC']
PET_TYPE_NAC_SUFFIX = ['_NAC']

# TRACER TYPES
TRACER_TYPES = {'FDG':'Fluorodeoxyglucose',
                 'PSMA':'Psma',
                   'FACBC':'Fluciclovine',
                     'DOTA':'Dotatate',
                       'AGNOSTIC':'Agnostic'}
                
# HYPERPARAMETERS
MULTI_RESOLUTION_SCHEME = '100x25x10'

# MOOSE PARAMETERS
MASK_FOLDER = 'masks'