import click
import os
import shutil
from tqdm import tqdm
from pathlib import Path

# Paremeters are read from the config.py file
import config

# Main -------------------------------------------------------------------------


def _uniq(input):
    """Search for unique subject ID"""
    output = []
    for x in input:
        if x not in output:
            output.append(x)
    return output


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
@click.option("--nthreads", default=8, help="Number of Threads", show_default=True)
@click.option("--out_res", default=2, help="Output Resolution", show_default=True)
@click.option("--dryrun", is_flag=True, help="print cmd only")
def main(range, nthreads, out_res, dryrun):
    """Run QSIPrep"""

    bids_dir = Path(config.outdir, 'BIDS_out')
    output_dir = Path(config.outdir, "derivatives")  # fullpath for output
    work_dir = Path(config.outdir, "Work")

    if not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)

    subjlist = _parse_range(range)

    # exit the program if selected subjects are more than the total number
    _check_range(subjlist, config.datasets)

    if not dryrun:
        pbar = tqdm(total=len(subjlist), unit="subject", desc="Transforming",
                    colour="#BDC0BA")

    for subj in subjlist:
        subjid = config.datasets[subj][1]
        session = config.datasets[subj][2]
        pbar.set_description(f"Processing ID {subjid}-{session}")
        pbar.refresh()

        # import pdb; pdb.set_trace()

        # container qsiprep
        # --session_id
        cmd = f"singularity run --cleanenv\
        -B {bids_dir}:/data:ro \
        -B {output_dir}:/output \
        -B {work_dir}:/work \
        {config.qsiprep} \
        /data \
        /output \
        participant \
        --participant_label {subjid} \
        --skip_bids_validation \
        --output-space T1w \
        --template MNI152NLin2009cAsym \
        --fs-license-file {config.scriptdir}/license.txt \
        --output-resolution {out_res} \
        --skip_bids_validation \
        --nthreads {nthreads} \
        --b0-motion-corr-to iterative \
        -w /work"

        if dryrun:
            print(cmd)
        else:
            os.system(cmd)
            pbar.update(1)
    if not dryrun:
        pbar.close()


if __name__ == "__main__":
    main()
