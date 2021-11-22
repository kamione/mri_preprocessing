# Environment ------------------------------------------------------------------
import os
import click


# Main -------------------------------------------------------------------------

@click.command()
@click.option('-p', '--path', type=click.Path(exists=True), required=True,
              help='a path to a project folder containing raw dicom files')
@click.option('-k', '--keyword', default='DICOM', required=True,
              help='a path to a project folder containing raw dicom files')
def main(path, keyword):
    '''find all the dicom sub-diretories under a project folder'''
    cmd = f'find {path} -name {keyword} > dicomlist.txt'
    print(cmd)
    os.system(cmd)


# Terminal Function ------------------------------------------------------------
if __name__ == '__main__':
    main()
