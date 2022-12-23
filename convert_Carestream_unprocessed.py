# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 10:31:58 2022

@author: ellen
"""
import glob
import os
from tkinter import filedialog
import pydicom
from pathlib import Path

def fix_sop_class(elem, **kwargs):
    """Fix for Carestream DX unprocessed."""
    if elem.tag == 0x00020002:
        # DigitalXRayImageStorageForProcessing
        elem = elem._replace(value=b"1.2.840.10008.5.1.4.1.1.1.1.1")

    return elem

print('Locate directory with dicom files from Carestream DX (unprocessed)')
directory = filedialog.askdirectory(title='Select folder with unprocessed Carestream DX files')
n_dcm = 0
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".dcm"):
            n_dcm += 1
            filename = os.path.join(root, file)
            pd = {}
            try:
                pd = pydicom.dcmread(filename)
            except pydicom.errors.InvalidDicomError:
                print('Not recognized as dicom: {filename}')
            except AttributeError:
                pydicom.config.data_element_callback = fix_sop_class
                pd = pydicom.dcmread(filename)
                date = pd.AcquisitionDate
                time = pd.AcquisitionTime[:6]
                kV = pd.KVP
                mAs = pd.Exposure
                new_filename = f'{date}_{time}_{kV}kV_{mAs}mAs.dcm'
                try:
                    new_path = Path(directory) / new_filename
                    pd.save_as(new_path)
                    print('Converted {filename}')
                    print('Written to {new_filename}')
                except:
                    print('Failed saving converted file {filename}')
if n_dcm == 0:
    print('Found no valid DICOM files in selected directory.')