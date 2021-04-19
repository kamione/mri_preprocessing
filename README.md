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

Sample Output of Step 3:
--------------------------------------------------------------------------------
Index                          ShortPath                          SubjID Session
--------------------------------------------------------------------------------
0     /home/yat/projects/testing/rpp_C002/DICOM                     001   0000  
1     /home/yat/projects/testing/rpp_C002_GE/DICOM                  002   0000  
2     /home/yat/projects/testing/rpp_C003/DICOM                     003   0000
```


---
config.json is a project specfic config file, specifying how the dim2bids
function organizes the output nifti files

---
adapted from <https://github.com/kelvinlim/bids_scripts>
