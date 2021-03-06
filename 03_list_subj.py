
import config


def main():
    dash = "-" * 80
    print(dash)
    print(f"{'Index' : <6}{'DICOM Directories':^60}{'SubjID':^7}{'Session':^7}")
    print(dash)
    count = 0
    for subjinfo in config.datasets:
        shortpath = subjinfo[0]
        subjid = subjinfo[1]
        session = subjinfo[2]
        print(f"{count:<6}{shortpath:<60}{subjid:^7}{session:^7}")
        count += 1


if __name__ == '__main__':
    main()
