#!/usr/bin/env python
import os
import click
import shutil
from tqdm import tqdm
from pathlib import Path

# Paremeters are read from the config.py file
import config


def _parse_range(str_):
    """
    Parse a string like numeric index set to a list
    INPUT : "0-2,5,9-11"
    OUTPUT: [0, 1, 2, 5, 9, 10, 11]
    """
    list_ = set()
    for chunk in str_.split(','):
        unit = chunk.split('-')
        list_.update(range(int(unit[0]), int(unit[-1]) + 1))
    return sorted(list_)


def _check_range(select, total):
    if len(select) > len(total):
        print("Error: Your selected range exceeds the total numbers of the dataset")
        exit()


def _copy_allfiles(source, destination):
    """"Copy all files in a directory to a destination"""
    for file in os.listdir(source):
        fp_source = Path(source, file)
        fp_destination = Path(destination, file)
        if fp_source.is_dir():
            shutil.copytree(fp_source, fp_destination)
        else:
            shutil.copy2(fp_source, fp_destination)


@click.command()
@click.argument("range")
@click.argument("dcmconfig", type=click.Path(exists=True))
@click.option("--dryrun", is_flag=True, help="print cmd only")
@click.option("--forcecopy", is_flag=True, help="force copy of dicom data")
def main(range, dryrun, dcmconfig, forcecopy):
    """
Converting DICOM images to a BIDS format\n
range    : a str of index, e.g. 0-2,5,9-11\n
dcmconfig: a path to a config.json for dicom files
    """

    subjlist = _parse_range(range)
    # exit the program if selected subjects are more than the total number
    _check_range(subjlist, config.datasets)

    # make if BIDS_out folder does not exist
    bidsdir = Path(config.outdir, "BIDS_out")
    if not bidsdir.is_dir():
        bidsdir.mkdir(parents=True, exist_ok=True)

    # make if tmp_dcm folder does not exist
    tmpdcm = Path(config.rawdir, "tmp_dcm")
    if not tmpdcm.is_dir():
        tmpdcm.mkdir(parents=True, exist_ok=True)

    # flag dry run without really running the transformation
    if not dryrun:
        pbar = tqdm(total=len(subjlist), unit="subject", desc="Transforming",
                    colour="#BDC0BA")

    for subj in subjlist:
        selected_subj = config.datasets[subj]
        shortpath = selected_subj[0]
        subjid = selected_subj[1]
        session = selected_subj[2]

        subj_tmpdcm = Path(tmpdcm, subjid, session)
        # overwrite the existing temp files
        if forcecopy:
            # check if subj_tmpdcm exists then delete it
            if subj_tmpdcm.is_dir():
                shutil.rmtree(subj_tmpdcm)
            # create the new destinaton directory
            subj_tmpdcm.mkdir(parents=True, exist_ok=True)
            # copy dicom files from raw data to a tmp folder
            try:
                _copy_allfiles(shortpath, subj_tmpdcm)
            except PermissionError:
                # in case _copy_allfiles does not work
                cmdCopy = f"cp -rf {shortpath}/* {subj_tmpdcm}"
                os.system(cmdCopy)
        else:
            if not subj_tmpdcm.is_dir():
                # create the new destinaton directory
                subj_tmpdcm.mkdir(parents=True, exist_ok=True)
                # copy dicom files from raw data to a tmp folder
                try:
                    _copy_allfiles(shortpath, subj_tmpdcm)
                except PermissionError:
                    # in case _copy_allfiles does not work
                    cmdCopy = f"cp -rf {shortpath}/* {subj_tmpdcm}"
                    os.system(cmdCopy)

        # create the conversion command using dcm2bids
        # example:
        #   dcm2bids -d DICOM_DIR -p PARTICIPANT_ID -s SESSION_ID \
        #   -c CONFIG_FILE -o BIDS_DIR

        cmd = f"dcm2bids \
                -d {subj_tmpdcm} \
                -p {subjid} \
                -s {session} \
                -c {dcmconfig} \
                -o {bidsdir} \
                --forceDcm2niix --clobber"

        if dryrun:
            print(cmd)
        else:
            os.system(cmd)
            pbar.update(1)
    if not dryrun:
        pbar.close()


if __name__ == '__main__':
    main()
