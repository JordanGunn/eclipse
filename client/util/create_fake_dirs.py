import os
from client.copy import *


ROOT = r"/home/jordan/work/geobc/sandbox/drive"


def create_dirs(root: str, n_files: int, n_bytes: int = 0):

    for d in GeoBCDirName.ALL:
        riprocess_dirs = RiProcessSourceDir.__dict__[d]
        riprocess_exts = RiProcessExtName.__dict__[d]

        for rd in riprocess_dirs:
            if rd.endswith('*'):
                rd = rd.replace('*', '')
            odir = os.path.join(root, rd)
            os.makedirs(odir, exist_ok=True)

            for ext in riprocess_exts:

                for n in range(n_files):
                    if ext.startswith("pos"):
                        ext = ext.replace('*', '')
                        fname = ext + "00" + str(n)
                    else:
                        fname = "file_" + str(n) + ext
                    out = os.path.join(odir, fname)
                    data = 'a' * n_bytes if n_bytes else 0
                    with open(out, 'w') as f:
                        if data:
                            f.write(data)


def main():
    create_dirs(ROOT, n_files=5, n_bytes=50)


if __name__ == "__main__":
    main()
