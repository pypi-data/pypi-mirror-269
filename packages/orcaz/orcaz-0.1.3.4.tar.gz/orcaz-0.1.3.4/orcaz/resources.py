#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Author: Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 04.07.2023
# Version: 0.1.0
#
# Description:
# This module contains the urls and filenames of the binaries that are required for the orca.
#
# Usage:
# The variables in this module can be imported and used in other modules within the orca to download the necessary
# binaries for the orca.
#
# ----------------------------------------------------------------------------------------------------------------------
import torch
from orcaz import constants

# ORCA MODELS

ORCA_MODELS = {
    "nac_fluorodeoxyglucose": {
        "url": "https://enhance-pet.s3.eu-central-1.amazonaws.com/orca/fdg_nac_g_epoch_2000.zip",
        "filename": "fdg_nac_g_epoch_2000.zip",
        "model": "fdg_nac_g_epoch_2000.pth",
        "directory": "fdg_nac_g_epoch_2000",
        "voxel_spacing": [2.80374, 2.80374, 2.00086]
    },
    "nac_psma": {
        "url": "http://0.0.0.0:2781/psma_nac_g_epoch_2000.zip",
        "filename": "psma_nac_g_epoch_2000.zip",
        "model": "psma_nac_g_epoch_2000.pth",
        "directory": "psma_nac_g_epoch_2000",
        "voxel_spacing": [3.3, 3.3, 2]
    },
    "nac_fluciclovine": {
        "url": "http://0.0.0.0:2781/fluciclovine_nac_g_epoch_2000.zip",
        "filename": "fluciclovine_nac_g_epoch_2000.zip",
        "model": "fluciclovine_nac_g_epoch_2000.pth",
        "directory": "fluciclovine_nac_g_epoch_2000",
        "voxel_spacing": [2.34375, 2.34375, 2.344]
    },
    "nac_dotatate": {
        "url": "http://0.0.0.0:2781/dotatate_nac_g_epoch_2000.zip",
        "filename": "dotatate_nac_g_epoch_2000.zip",
        "model": "dotatate_nac_g_epoch_2000.pth",
        "directory": "dotatate_nac_g_epoch_2000",
        "voxel_spacing": [2.34375, 2.34375, 2.344]
    },
    "nac_agnostic": {
        "url": "http://0.0.0.0:2781/agnostic_nac_g_epoch_2000.zip",
        "filename": "agnostic_nac_g_epoch_2000.zip",
        "model": "agnostic_nac_g_epoch_2000.pth",
        "directory": "agnostic_nac_g_epoch_2000",
        "voxel_spacing": [2.80374, 2.80374, 2.00086]
    },
}


def check_cuda(print_flag=False) -> str:
    """
    This function checks if CUDA is available on the device and prints the device name and number of CUDA devices
    available on the device.

    Returns:
        str: The device to run predictions on, either "cpu" or "cuda".
    """
    if not torch.cuda.is_available():
        print(
            f"{constants.ANSI_ORANGE}CUDA not available on this device. Predictions will be run on CPU.{constants.ANSI_RESET}") if print_flag else None
        return "cpu"
    else:
        device_count = torch.cuda.device_count()
        print(
            f"{constants.ANSI_GREEN} CUDA is available on this device with {device_count} GPU(s). Predictions will be run on GPU.{constants.ANSI_RESET}") if print_flag else None
        return "cuda"
