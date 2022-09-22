# Environment ------------------------------------------------------------------
import os
import click


# Main -------------------------------------------------------------------------

@click.command()
@click.option('-p', '--path', type=click.Path(exists=True), required=True,
              help='a path to a project folder containing raw dicom files')
@click.option('-k1', '--keyword1', default='DICOM', required=True,
              help='a path to a project folder containing raw dicom files')
@click.option('-k2', '--keyword2', default='A', required=True,
              help='a path to a project folder containing raw dicom files')
def main(path, keyword1, keyword2):
    '''find all the dicom sub-diretories under a project folder'''
    cmd = f'find {path} \( -name {keyword1} -o -name {keyword2} \) > dicomlist.txt'
    print(cmd)
    os.system(cmd)


# Terminal Function ------------------------------------------------------------
if __name__ == '__main__':
    main()
