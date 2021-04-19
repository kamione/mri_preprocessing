#!/usr/bin/env python
import click
import os
import path


def intro(projname, rawdir, outdir, containerdir):
    """
    projname = "eyegaze"
    srcdir = '/home/oldserver/eyegazetask'
    destdir = '/home/share/eyegaze_BIDS'
    container = "/home/share/Containers/tjhendrickson-BIDS_scripts-master-latest.simg"
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
    return ''.join(str)


@click.command()
@click.argument("subjid_init", type=int, required=True)
@click.option("-i", "--input", type=click.Path(exists=True),
              help="dicomlist.txt", required=True)
@click.option("--projname", prompt="Project Name", required=True)
@click.option("--rawdir", prompt="Raw Directory", required=True)
@click.option("--outdir", prompt="Output Directory", required=True)
@click.option("--containerdir", prompt="Container Directory", required=True)
def main(subjid_init, input, projname, rawdir, outdir, containerdir):
    """
    Prepare a config.py from a dicomlist.py generated in the source directory
    (e.g. /home/oldserver/eyegazetask) with the following command:
    $ find /home/oldserver/eyegazetask -name "DICOM" > dicomlist.txt
    """
    # read in dicom directory paths
    dicomdirs = []
    f = open(input)
    for line in f.readlines():
        dicomdirs.append(line.rstrip())
    f.close()

    dicomdirs = sorted(dicomdirs)

    fo = open("config.py", "w")
    fo.write(intro(projname, rawdir, outdir, containerdir))
    fo.write("datasets = [\n")
    for dir_ in dicomdirs:
        session_init = 0
        fo.write(f'    ["{dir_}", "{subjid_init:03d}", "{session_init:04d}"],\n')
        subjid_init += 1
        session_init += 1
    fo.write("]")
    fo.close()

    print("\nMESSAGE: A config.py file is written!")


if __name__ == '__main__':
    main()
