#!/usr/bin/env python
import os
import click


@click.command()
@click.option("-p", "--path", type=click.Path(exists=True), required=True,
              help="a path to a project folder containing raw dicom files")
def main(path):
    """find all the dicom sub-diretories under a project folder"""
    cmd = f"find {path} -name DICOM > dicomlist.txt"
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
