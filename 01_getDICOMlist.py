import os
import click


@click.command()
@click.option("-p", "--path", type=click.Path(exists=True), required=True)
def main(path):
    cmd = f"find {path} -name 'DICOM' > dicomlist.txt"
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
