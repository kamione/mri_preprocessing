# Commandline python wrappers for fmriprep
---
## Usage:

Requirements: dcm2niix, dcm2bids and fmriprep (version: 20.2.1)

Step 0:
```bash
# install required modules
pip install -r requirements.txt
# change directory to the script folder
cd /path/to/script_folder
```

Step 1:
```bash
python 01_get_dicom.py -p /path/to/dicom_directory
```

Step 2:
```bash
python 02_prep_config.py 1 -i dicomlist.txt
# prompt will be popped up
```

Step 3:
```bash
python 03_list_subj.py --listing

# Sample Output of Step 3:
# Indice can be used in the Step 4 and 5 to indicate which subjects you would
# like to include and process
# --------------------------------------------------------------------------------
# Index                      DICOM Directories                      SubjID Session
# --------------------------------------------------------------------------------
# 0     /home/user/projects/rpp_C002/DICOM                            001   0000  
# 1     /home/user/projects/rpp_C002_GE/DICOM                         002   0000  
# 2     /home/user/projects/rpp_C003/DICOM                            003   0000
```

Step 4:
```bash
# transform dicom to nii with a BIDS structure
python 04_run_dcm2bids.py 0-2 config.json --forcecopy
```

Step 5:
```bash
# run fmriprep
# this script will check if FreeSurfer license.txt exit in the output folder
# if not, it will copy the current license.txt file to the output folder
python 05_run_fmriprep.py 0-2
```

---
*REMARKS*: config.json is a project specfic config file, specifying how the dim2bids
function organizes the output nifti files

---
adapted from <https://github.com/kelvinlim/bids_scripts>
