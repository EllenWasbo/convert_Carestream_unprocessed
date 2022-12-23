# convert_Carestream_unprocessed
Fix SOP class of unprocessed images exported from Carestream DX which causes issues for different dicom readers (e.g. IDLffDICOM, pydicom).
The essential fix was found [here](https://stackoverflow.com/questions/71053788/extracting-data-from-a-dicomdir-file-using-pydicom). And this is baked into this script to find, convert and re-save these files. New file name is date_time_kVp_mA.dcm (parameters found from the DICOM header) and put directly in the selected folder.

(This fix is integrated in [imageQCpy](https://github.com/EllenWasbo/imageQCpy/wiki) so unprocessed images will be accepted, but not saved).

# Requirements
pydicom

# What the script does
You will be asked to locate a folder where the DICOM images are. The script will search for all .dcm files within that folder/subfolders. Each file that trigger an AttributeError of pydicom.dcmread(file) will be subject to the fix and saved with the new name.

