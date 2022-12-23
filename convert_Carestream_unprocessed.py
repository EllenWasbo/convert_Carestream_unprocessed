# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 2022
@author: EllenWasbo
fix_sop_class from https://stackoverflow.com/questions/71053788/extracting-data-from-a-dicomdir-file-using-pydicom
(scaramallion)
"""
from tkinter import Tk
from tkinter import filedialog
import pydicom
from pathlib import Path

pydicom.config.future_behavior(True)

def fix_sop_class(elem, **kwargs):
    """Fix for Carestream DX unprocessed."""
    if elem.tag == 0x00020002:
        # DigitalXRayImageStorageForProcessing
        elem = elem._replace(value=b"1.2.840.10008.5.1.4.1.1.1.1.1")

    return elem


root_tk = Tk()
print('Locate directory with dicom files from Carestream DX (unprocessed)')
directory = filedialog.askdirectory(title='Select folder with unprocessed Carestream DX files')
n_dcm = 0

dcm_files = []
if directory != '':
    p = Path(directory)
    if p.is_dir():
        # glob_string = '**/*' if search_subfolders else '*'
        dcm_files = [
            str(x.resolve()) for x in p.glob('**/*') if x.suffix == '.dcm']

    if len(dcm_files) > 0:
        print(f'Found {len(dcm_files)} DICOM files')
        for file in dcm_files:
            print(f'Testing {file}')
            pd = {}
            try:
                pd = pydicom.dcmread(file)
            except pydicom.errors.InvalidDicomError:
                print('Not recognized as dicom: {filename}')
            except AttributeError:
                pydicom.config.data_element_callback = fix_sop_class

            pd = pydicom.dcmread(file)
            date = pd.AcquisitionDate
            time = pd.AcquisitionTime[:6]
            kV = pd.KVP
            mAs = pd.Exposure
            new_filename = f'{date}_{time}_{kV}kV_{mAs}mAs.dcm'
            print(f'new filename {new_filename}')
            try:
                new_path = p / new_filename
                pd.save_as(str(new_path.resolve()))
                print(f'Converted  to {new_path}')
            except:
                print('Failed saving converted file {file}')
    else:
        print('Found no valid DICOM files in selected directory.')

root_tk.destroy()