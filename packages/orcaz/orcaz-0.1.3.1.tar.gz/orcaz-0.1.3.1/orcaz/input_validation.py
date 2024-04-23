#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Project: Optimized Registration through Conditional Adversarial networks (ORCA)
# Author: Zacharias Chalampalakis | Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 3.04.2024
# Version: 0.1.0
#
# Description:
# This module performs input validation for the orca. It verifies that the inputs provided by the user are valid
# and meets the required specifications.
#
# Usage:
# The functions in this module can be imported and used in other modules to perform input validation.
#
# ----------------------------------------------------------------------------------------------------------------------

import logging
from pathlib import Path
import os

from orcaz import constants
from rich.console import Console

console = Console()
def validate_orca_compliant_files(path: list) -> bool:
    """
    Selects the files have names that are compliant with orca input files.
    :param path: The path with the present files in the subject directory.
    :return: If input is valid return PET type, else a false flag to terminate execution.
    """
    pet_type = None
    # go through each file and see if the files have the appropriate modality prefix and tracer type.
    files = [file for file in os.listdir(path) if file.endswith('.nii') or file.endswith('.nii.gz')]
    pet_prefixes_files = [file for tag in constants.FUNCTIONAL_MODALITIES_SUFFIX for file in files if tag in file]
    ct_prefixes_files = [file for tag in constants.ANATOMICAL_MODALITIES_SUFFIX for file in files if tag in file]
    if len(ct_prefixes_files) == 1 and len(pet_prefixes_files) == 1:
        console.print(f" Orca compliant PET and CT found ", style="bold magenta")
        logging.info(f" Orca compliant PET and CT found")
        if len([file for file in pet_prefixes_files for tag in constants.PET_TYPE_AC_SUFFIX if tag in file]) == 1:
            console.print(f" Orca compliant AC-PET type found ", style="bold magenta")
            logging.info(f" Orca compliant AC-PET type found")
            pet_type = constants.PET_TYPE_AC
        elif len([file for file in pet_prefixes_files for tag in constants.PET_TYPE_NAC_SUFFIX if tag in file]) == 1:
            console.print(f" Orca compliant NAC-PET type found ", style="bold magenta")
            logging.info(f" Orca compliant NAC-PET type found")        
            pet_type = constants.PET_TYPE_NAC
        else: 
            console.print(f" Orca compliant PET type not found ", style="bold magenta")
            logging.info(f" Orca compliant PET type not found")
    else:
        console.print(f" Orca compliant PET and CT not found ", style="bold magenta")
        logging.info(f" Orca compliant PET and CT not found")
    return pet_type

def validate_orca_tracer_type(path: list) -> str:
    """
    Selects the files have tracer names that are compliant with orca input tracer types.
    :param path: The path with the present files in the subject directory.
    :return: If input is avlide return the tracer ID, else an invalide flag to terminate execution.
    """
    tracer_type = None
    # go through each file and see if the files have the appropriate modality prefix and tracer type.
    files = [file for file in os.listdir(path) if file.endswith('.nii') or file.endswith('.nii.gz')]
    pet_prefixes_files = [file for tag in constants.FUNCTIONAL_MODALITIES_SUFFIX for file in files if tag in file]
    if len([file for tag in constants.TRACER_TYPES.keys() for file in pet_prefixes_files if tag in file]) == 1:
        tracer_tag = [tag for tag in constants.TRACER_TYPES.keys() if tag in pet_prefixes_files[0]][0]
        console.print(f" Orca compliant PET tracer {tracer_tag}  found ", style="bold magenta")
        logging.info(f" Orca compliant PET tracer {tracer_tag}  found ")
    else:
        console.print(f" Orca compliant PET tracer not found ", style="bold magenta")
        logging.info(f" Orca compliant PET tracer not found")
    return constants.TRACER_TYPES[tracer_tag]

def combine_pet_type_tag(pet_tag, tracer_tag):
    """
    Combines the PET type and tracer tag to form a unique identifier for the ORCA model.
    :param tag: The PET type tag
    :param tracer_tag: The tracer tag
    :return: The combined PET type and tracer tag
    """
    pet_tag = "nac_" if pet_tag == constants.PET_TYPE_NAC else "ac_" if pet_tag == constants.PET_TYPE_AC else ""
    tracer_tag = tracer_tag.lower()
    return (pet_tag + tracer_tag)