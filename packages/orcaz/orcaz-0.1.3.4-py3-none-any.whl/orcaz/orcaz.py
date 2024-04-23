#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# **********************************************************************************************************************
# File: orca.py
# Project: Optimized Registration through Conditional Adversarial networks (ORCA)
# Author: Zacharias Chalampalakis | Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 04.07.5023
# Version: 0.1.0
# Email: zacharias.chalampalakis@meduniwien.ac.at, lalith.shiyamsundar@meduniwien.ac.at
# Description: 
# ORCA is a deep learning based image registration framework for the co-registration between CT and PET images.
# License: Apache 2.0
# Usage:
# python orca.py --mode coreg --ct /path/to/ct.nii.gz --pet /path/to/pet.nii.gz --dout /path/to/output_dir
# python orca.py --mode pred --pet /path/to/pet.nii.gz --dout /path/to/output_dir
# python orca.py --mode train --data_path /path/to/data --output /path/to/checkpoints_dir
# **********************************************************************************************************************

# Importing required libraries
import logging
import sys
import emoji
import time

from datetime import datetime
from orcaz import train
from orcaz import predict_single_image
from orcaz import display,constants,file_utilities
from orcaz import download,resources
from orcaz.options import Options
from orcaz import image_conversion, input_validation
from orcaz import settings
from orcaz import image_processing
from pathlib import Path
import os 
import glob


import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')

import resource
rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, rlimit[1]))

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO,
                    filename=datetime.now().strftime('orca-%H-%M-%d-%m-%Y.log'),
                    filemode='w')
# uncomment the following line to print the logs to the console
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def main():

    display.logo()
    logging.info("----------------------------------------------------------------------------------------------------")
    logging.info("                                         STARTING ORCA 0.1.0                                        ")
    logging.info("----------------------------------------------------------------------------------------------------")
    logging.info(' ')

    # ----------------------------------
    # INPUT ARGUMENTS and SWITCH BETWEEN MODES
    # ----------------------------------
   
    opt = Options().parse_options()
    # TODO: Add subparsers for the different options.
    if opt.mode =='train':
        logging.info('-'*50)
        logging.info('          Using ORCA in training mode             ')
        logging.info('-'*50)
        train.train(opt)

    elif opt.mode=='coreg':
        logging.info('-'*50)
        logging.info('        Using ORCA in co-registration mode        ')
        logging.info('-'*50)

        # ----------------------------------
        # INPUT STANDARDIZATION
        # ----------------------------------
        # calculate elapsed time for the entire procedure below
        start_time = time.time()
        print('')
        print(f'{constants.ANSI_BLUE} {emoji.emojize(":magnifying_glass_tilted_left:")} STANDARDIZING INPUT DATA TO '
            f'NIFTI:{constants.ANSI_RESET}')
        print('')
        logging.info(' ')
        logging.info(' STANDARDIZING INPUT DATA:')
        logging.info(' ')
        download.download_binaries()
        dcm_flag = image_conversion.standardize_to_nifti(opt.subject_directory)
        print(f"{constants.ANSI_GREEN} Standardization complete.{constants.ANSI_RESET}")
        logging.info(" Standardization complete.")
        
        pet_type =  input_validation.validate_orca_compliant_files(opt.subject_directory)
        if pet_type == None:
            return 1

        tracer_tag = input_validation.validate_orca_tracer_type(opt.subject_directory)
        if tracer_tag == None:
            return 1
        
        # Select the approriate model type based on the PET type and tracer tag
        model_id = input_validation.combine_pet_type_tag(pet_type, tracer_tag)
        models_path = constants.MODEL_PATH
        file_utilities.create_directory(models_path)
        download.download(item_name=model_id, item_path=constants.MODEL_PATH, item_dict=resources.ORCA_MODELS)
        settings.model_path = os.path.join(constants.MODEL_PATH,resources.ORCA_MODELS[model_id]['directory'],resources.ORCA_MODELS[model_id]['model'])

        # ---------------------------------------------------
        # RUNNING PREPROCESSING AND CO-REGISTRATION PIPELINE
        # ---------------------------------------------------
        start_time = time.time()
        print('')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":rocket:")} RUNNING PREPROCESSING AND CO-REGISTRATION PIPELINE:{constants.ANSI_RESET}')
        print('')

        logging.info(' ')
        logging.info(' RUNNING PREPROCESSING AND CO-REGISTRATION PIPELINE:')
        logging.info(' ')
        orca_dir, ct_dir, pt_dir, mask_dir = image_processing.preprocess(opt.subject_directory,dicom_files_flag=dcm_flag)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} Preprocessing complete.{constants.ANSI_RESET}')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":robot:")} Generating syntheticCT.{constants.ANSI_RESET}')
        predict_single_image.predict(opt, orca_dir, ct_dir, pt_dir)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} synthetic CT generation complete.{constants.ANSI_RESET}')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":whale:")} Co-registering CT to synthetic CT.{constants.ANSI_RESET}')
        image_processing.align(orca_dir, ct_dir, pt_dir, mask_dir,opt.workers)
        image_processing.postprocess(orca_dir, ct_dir, mask_dir)
        # Check if input ct is in DICOM format, if so export the co-registered CT to DICOM
        subject_directory = os.path.abspath(opt.subject_directory)
        if dcm_flag and image_conversion.is_dicom(glob.glob(os.path.join(subject_directory, '*_CT/*'))[0]):
            image_processing.export_dicom(orca_dir, opt.subject_directory)
        end_time = time.time()
        elapsed_time = end_time - start_time
        # show elapsed time in minutes and round it to 2 decimal places
        elapsed_time = round(elapsed_time / 60, 2)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} Co-registration complete.'
            f' Elapsed time: {elapsed_time} minutes! {emoji.emojize(":partying_face:")} \n Co-registered images are stored in'
            f' {constants.ALIGNED_CT_FOLDER}! {constants.ANSI_RESET}')

    else:
        logging.error("*** !Unknown mode option requested, exiting now! ***")
        print(f'{constants.ANSI_ORANGE} {emoji.emojize(":warning:")} Unknown mode option requested, exiting now! {constants.ANSI_RESET}')
        return 1; 

if __name__ == '__main__':
  main()