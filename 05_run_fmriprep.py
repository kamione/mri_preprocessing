import click
import os
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


@click.command()
@click.argument("range")
@click.option("--dryrun", is_flag=True, help="print cmd only")
def main(range, dryrun):
    """Run fMRIPrep"""

    bids_dir = Path(config.outdir, 'BIDS_out')
    derivatives_dir = Path(config.outdir, "derivatives")  # fullpath for output
    if not derivatives_dir.is_dir():
        derivatives_dir.mkdir(parents=True, exist_ok=True)

    subjlist = _parse_range(range)

    # exit the program if selected subjects are more than the total number
    _check_range(subjlist, config.datasets)

    # copy the license.txt to output
    license = Path(config.outdir, "license.txt")
    if not license.is_file():
        shutil.copy2(Path(config.scriptdir, "license.txt"), license)

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
        # container fmriprep 20.2.1
        # --session_id
        cmd = f"singularity run -B {bids_dir}:/work -B {derivatives_dir}:/output \
        -B {config.outdir}:/main \
        {config.fmriprep} /work /output participant \
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
            os.system(cmd)
            pbar.update(1)
    if not dryrun:
        pbar.close()


if __name__ == "__main__":
    main()
