# Environment ------------------------------------------------------------------
import click
import os
from pathlib import Path

# Main -------------------------------------------------------------------------
def intro(projname, rawdir, outdir, containerdir, fmriprep_ver, mriqc_ver, scriptdir):
    """
Samples:

projname = "Project A"
srcdir = "/home/oldserver/projects"
destdir = "/home/olderserver/Project_A"
container = "/home/share/Containers"
fmriprep = "20.2.1"
mriqc = "0.16.1"
    """
    str = []
    tmp = f'projname = "{projname}"\n'
    str.append(tmp)
    tmp = f'rawdir = "{rawdir}"\n'
    str.append(tmp)
    tmp = f'outdir = "{outdir}"\n'
    str.append(tmp)
    tmp = f'container = "{containerdir}"\n'
    str.append(tmp)
    fmriprep_dir = Path(containerdir, f"fmriprep-{fmriprep_ver}.simg")
    tmp = f'fmriprep = "{fmriprep_dir}"\n'
    str.append(tmp)
    mriqc_dir = Path(containerdir, f"mriqc-{mriqc_ver}.simg")
    tmp = f'mriqc = "{mriqc_dir}"\n'
    str.append(tmp)
    tmp = f'scriptdir = "{scriptdir}"\n'
    str.append(tmp)
    return ''.join(str)


@click.command()
@click.argument("subjid_init", type=int, required=True)
@click.option("-i", "--input", type=click.Path(exists=True),
              help="dicomlist.txt", required=True)
@click.option("--projname", prompt="Project Name", required=True)
@click.option("--rawdir", prompt="Raw Directory", required=True)
@click.option("--outdir", prompt="Output Directory", required=True)
@click.option("--containerdir", prompt="Container Directory", required=True)
@click.option("--fmriprep_ver", prompt="fMRIprep Version", required=True)
@click.option("--mriqc_ver", prompt="MRIQC Version", required=True)
@click.option("--scriptdir", prompt="Script Directory", required=True)
def main(subjid_init, input, projname, rawdir, outdir, containerdir,
         fmriprep_ver, mriqc_ver, scriptdir):
    """
Prepare a config.py from a dicomlist.py generated in the source directory
(e.g. /home/oldserver/eyegazetask) with the following command:
$ find /home/oldserver/eyegazetask -name "DICOM" > dicomlist.txt

P.S. fmriprep 1.2.5 and 20.2.1 were tested
    """
    # read in dicom directory paths
    dicomdirs = []
    f = open(input)
    for line in f.readlines():
        dicomdirs.append(line.rstrip())
    f.close()

    dicomdirs = sorted(dicomdirs)

    fo = open("config.py", "w")
    fo.write(
        intro(projname, rawdir, outdir, containerdir, fmriprep_ver, mriqc_ver,
              scriptdir)
    )
    fo.write("datasets = [\n")
    for dir_ in dicomdirs:
        session_init = 0
        fo.write(
            f'    ["{dir_}", "{subjid_init:03d}", "{session_init:04d}"],\n')
        subjid_init += 1
        session_init += 1
    fo.write("]")
    fo.close()

    print("\nMESSAGE: A config.py file is written!")


if __name__ == '__main__':
    main()
