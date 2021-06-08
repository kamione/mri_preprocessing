# Environment ------------------------------------------------------------------
import os
import click
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


@click.command()
@click.argument("range")
@click.option("--nthreads", default=8, help="Number of Threads", show_default=True)
@click.option("--dryrun", is_flag=True, help="print cmd only")
def main(range, nthreads, dryrun):
    """Run MRIQC"""
    bids_dir = Path(config.outdir, "BIDS_out")
    output_dir = Path(config.outdir, "derivatives", "mriqc")
    work_dir = Path(config.outdir, "Work")

    subjlist = _parse_range(range)
    tmplist = []
    
    # check if output directory exists; if not, make it
    if not output_dir.is_dir():
        output_dir.mkdir(parents=True, exist_ok=True)
        
    for i in config.datasets:
        tmplist.append(i[1])
    labels = _uniq(tmplist)
    
    for subj in subjlist:
        label = labels[subj]

        cmd = f"singularity run --cleanenv \
            -B {bids_dir}:/data:ro \
            -B {output_dir}:/out \
            -B {work_dir}:/work \
            {config.mriqc} \
            /data \
            /out \
            participant \
            --participant-label sub-{label} \
            --n_proc {nthreads} \
            --no-sub \
            -w /work"
        
        if dryrun:
            print(cmd)
        else:
            os.system(cmd)


# Terminal Function ------------------------------------------------------------
if __name__ == "__main__":
    main()



