import os
import sys
from plist.controller import PlistController


def main():
    str_opts = [s for s in sys.argv if "=" in s]
    opts = dict()
    for s in str_opts:
        k = s.split("=")[0]
        v = s.split("=")[1]
        opts[k] = v

    if "target" not in opts.keys():
        print("specify location to write playlist to using target=")
        sys.exit(0)

    if "wd" in opts.keys():
        os.chdir(opts["wd"])

    PlistController(opts)


if __name__ == "__main__":
    main()
