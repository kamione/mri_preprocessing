# Commandline python wrappers for fmriprep
---
## Usage:

Step 1:
```bash
cd /path/to/script_folder
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
# like to process
# --------------------------------------------------------------------------------
# Index                          ShortPath                          SubjID Session
# --------------------------------------------------------------------------------
# 0     /home/user/projects/rpp_C002/DICOM                            001   0000  
# 1     /home/user/projects/rpp_C002_GE/DICOM                         002   0000  
# 2     /home/user/projects/rpp_C003/DICOM                            003   0000
```

Step 4:
```bash
python 04_run_dcm2bids.py 0-2 config.json --forcecopy
```

Step 5:
```bash
python 05_run_fmriprep.py 0-2
```

---
config.json is a project specfic config file, specifying how the dim2bids
function organizes the output nifti files

---
adapted from <https://github.com/kelvinlim/bids_scripts>
