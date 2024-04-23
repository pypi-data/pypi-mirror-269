#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Author:  Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
#
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 07.07.2023
# Version: 1.0.0
#
# Description:
# This module handles image conversion for the orcaz.
#
# Usage:
# The functions in this module can be imported and used in other modules within the orcaz to perform image conversion.
#
# ----------------------------------------------------------------------------------------------------------------------

import contextlib
import io
import os
import re
import unicodedata
import subprocess
from typing import List

import SimpleITK
import dicom2nifti
import pydicom
from rich.progress import Progress
from orcaz.constants import DCM2NIIX_PATH

def clear_ROI1_and_json(input_path: str) -> None:
    """
    Removes ROI1 files from CT convertion of Siemens CT data

    :param input_path: str, Directory to search and delete files from.
    """
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if ("ROI1") in file:
                os.remove(os.path.join(root, file))
            if file.endswith('.json'):
                os.remove(os.path.join(root, file))


def non_nifti_to_nifti(input_path: str, output_directory: str = None) -> None:
    """
    Converts any image format known to ITK to NIFTI

    :param input_path: str, Directory OR filename to convert to nii.gz
    :param output_directory: str, optional output directory to write the image to.
    """

    if not os.path.exists(input_path):
        print(f"Input path {input_path} does not exist.")
        return

    # Processing a directory
    if os.path.isdir(input_path):
        #modality = get_dicom_modality(input_path)
        nifti_dir = dcm2niix(input_path)
        clear_ROI1_and_json(nifti_dir)
        return

    # Processing a file
    if os.path.isfile(input_path):
        # Ignore hidden or already processed files
        _, filename = os.path.split(input_path)
        if filename.startswith('.') or filename.endswith(('.nii.gz', '.nii')):
            return
        else:
            output_image = SimpleITK.ReadImage(input_path)
            output_image_basename = f"{os.path.splitext(filename)[0]}.nii"

    if output_directory is None:
        output_directory = os.path.dirname(input_path)

    output_image_path = os.path.join(output_directory, output_image_basename)
    SimpleITK.WriteImage(output_image, output_image_path)

# this function returns the path of the folder sin the parent directory
def standardize_to_nifti(parent_dir: str) -> bool:
    """
    Converts all images in a parent directory to NIFTI
    """
    # go through the subdirectories
    subjects = os.listdir(parent_dir)
    # get only the directories
    subjects = [subject for subject in subjects if os.path.isdir(os.path.join(parent_dir, subject))]
    with Progress() as progress:
        task = progress.add_task("[white] Processing subjects...", total=len(subjects))
        for subject in subjects:
            subject_path = os.path.join(parent_dir, subject)
            if os.path.isdir(subject_path):
                image_path = os.path.join(parent_dir, subject)
                non_nifti_to_nifti(image_path,os.path.dirname(image_path))
            elif os.path.isfile(os.path.join(parent_dir, subject)):
                image_path = os.path.join(subject_path, subject)
                print(f"Input path {parent_dir} does not contain subdirectories.")
                return []
            else:
                continue
            progress.update(task, advance=1, description=f"[white] Processing {subject}...")
    if len(subjects)!=0:
        return True
    else:
        return False
        

def is_dicom(file_path) -> bool:
    """
    Checks if a given file is a DICOM image.

    :param str file_path: Path to the file.
    :return: True if the file is a DICOM image, False otherwise.
    :rtype: bool
    """
    try:
        _ = pydicom.dcmread(file_path)
        return True
    except:
        return False

def dcm2niix(input_path: str) -> str:
    """
    Converts DICOM files to NIfTI format using dcm2niix.

    Args:
        input_path (str): The path to the input directory.
        output_dir (str): The path to the output directory.

    Returns:
        str: The path to the output directory.

    Raises:
        NiftiConverterError: If there's an error during DICOM to NIFTI conversion.
    """

    output_dir = os.path.dirname(input_path)
    cmd_to_run: List[str] = [DCM2NIIX_PATH, '-z', 'n', '-f', '%f', '-o', output_dir, input_path]

    try:
        subprocess.run(cmd_to_run, capture_output=True, check=True)
    except subprocess.CalledProcessError:
        raise NiftiConverterError(f"Error during DICOM to NIFTI conversion using dcm2niix.")

    return output_dir

class NiftiConverterError(Exception):
    pass

def remove_accents(unicode_filename):
    try:
        unicode_filename = str(unicode_filename).replace(" ", "_")
        cleaned_filename = unicodedata.normalize('NFKD', unicode_filename).encode('ASCII', 'ignore').decode('ASCII')
        cleaned_filename = re.sub(r'[^\w\s-]', '', cleaned_filename.strip().lower())
        cleaned_filename = re.sub(r'[-\s]+', '-', cleaned_filename)
        return cleaned_filename
    except:
        return unicode_filename


def is_dicom_file(filename):
    try:
        pydicom.dcmread(filename)
        return True
    except pydicom.errors.InvalidDicomError:
        return False


def get_dicom_modality(dicom_dir):
    """Create a lookup dictionary from DICOM files.

    Parameters:
    dicom_dir (str): The directory where DICOM files are stored.

    Returns:
    modality:
    """

    # a dictionary to store information from the DICOM files
    # dicom_info = {}

    # loop over the DICOM files
    for filename in os.listdir(dicom_dir):
        full_path = os.path.join(dicom_dir, filename)
        if is_dicom_file(full_path):
            # read the DICOM file
            ds = pydicom.dcmread(full_path)

            # extract the necessary information
            # series_number = ds.SeriesNumber if 'SeriesNumber' in ds else None
            # series_description = ds.SeriesDescription if 'SeriesDescription' in ds else None
            # sequence_name = ds.SequenceName if 'SequenceName' in ds else None
            # protocol_name = ds.ProtocolName if 'ProtocolName' in ds else None
            # series_instance_UID = ds.SeriesInstanceUID if 'SeriesInstanceUID' in ds else None
            if ds.Modality == 'PT':
                modality = 'PET'
            else:
                modality = ds.Modality

            # # anticipate the filename dicom2nifti will produce and store the modality tag with it
            # if series_number is not None:
            #     base_filename = remove_accents(series_number)
            #     if series_description is not None:
            #         anticipated_filename = f"{base_filename}_{remove_accents(series_description)}.nii"
            #     elif sequence_name is not None:
            #         anticipated_filename = f"{base_filename}_{remove_accents(sequence_name)}.nii"
            #     elif protocol_name is not None:
            #         anticipated_filename = f"{base_filename}_{remove_accents(protocol_name)}.nii"
            # else:
            #     anticipated_filename = f"{remove_accents(series_instance_UID)}.nii"

            # dicom_info[anticipated_filename] = modality

    return modality


def rename_nifti_files(nifti_dir):
    """Rename NIfTI files based on a lookup dictionary.

    Parameters:
    nifti_dir (str): The directory where NIfTI files are stored.
    dicom_info (dict): A dictionary where the key is the anticipated filename that dicom2nifti will produce and
                       the value is the modality of the DICOM series.
    """
    quit()
    # loop over the NIfTI files
    for filename in os.listdir(nifti_dir):
        print("for filename in os.listdir(nifti_dir):", filename)
        if filename.endswith('.nii'):
            # create the new filename
            #new_filename = f"{modality}_{filename}"
            new_filename = f"{modality}_img.nii"
            print("Renaming", filename, "to", new_filename)
            # rename the file
            os.rename(os.path.join(nifti_dir, filename), os.path.join(nifti_dir, new_filename))
