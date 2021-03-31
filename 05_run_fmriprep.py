#!/usr/bin/env python
import click
import os
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


@click.command()
@click.argument("range")
@click.option("--dryrun", is_flag=True, help="print cmd only")
def main(range, dryrun):
    """Run fmriprep"""

    bids_dir = Path(config.outdir, 'BIDS_output')
    fmriprep_dir = Path(config.outdir, 'derivatives')  # fullpath for output
    if not fmriprep_dir.is_dir():
        fmriprep_dir.mkdir(parents=True, exist_ok=True)

    subjlist = _parse_range(range)

    # exit the program if selected subjects are more than the total number
    _check_range(subjlist, config.datasets)

    logdir = Path(config.outdir, "log")
    if not logdir.is_dir():
        logdir.mkdir(parents=True, exist_ok=True)

    if not dryrun:
        pbar = tqdm(total=len(subjlist), unit="subject", desc="Transforming",
                    colour="#BDC0BA")

    for subj in subjlist:
        subjid = config.datasets[subj][1]
        session = config.datasets[subj][2]
        pbar.set_description(f"Processing ID {subjid}-{session}")
        pbar.refresh()

        # import pdb; pdb.set_trace()

        # sample command
        """
        singularity run -B $BIDS/BIDS_output/:/work -B $BIDS/fmriprep_output:/output \
        $CONTAINER /work /output participant \
        --participant_label 013 \
        --fs-license-file /output/license.txt \
        --use-aroma \
        --use-syn-sdc
        """

        # session_id is not a valid argument even for most recent
        # container  fmriprep 20.1.1
        # --session_id
        cmd = f"singularity run -B {bids_dir}:/work -B {fmriprep_dir}:/output \
        -B {config.outdir}:/main \
        {config.container} /work /output participant \
        --participant_label {subjid}\
        --fs-license-file /main/license.txt \
        --use-aroma \
        --ignore slicetiming \
        --cifti-output \
        --skip-bids-validation \
        -w /main/Work \
        --use-syn-sdc"

        if dryrun:
            print(cmd)
        else:
            cmd = f"{cmd} > {logdir}/fmriprep_{subjid}-{session}.log"
            os.system(cmd)
            pbar.update(1)
    if not dryrun:
        pbar.close()


if __name__ == '__main__':
    main()
