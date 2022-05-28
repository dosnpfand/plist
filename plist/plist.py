#!/usr/local/bin/python3.7
"""
GOAL refactor: make it possible to add pyQT GUI for windows

TODOS refactor:
    - test pyQT Gui

"""
import os
import sys
from controller import PlistController


# def get_video_length(fname):
#
#     try:
#         result = subprocess.Popen(["ffprobe", fname], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
#         res = [x.decode('UTF-8') for x in result.stdout.readlines() if 'Duration' in x.decode('UTF-8')]
#         match = re.search(r'Duration: ([\d:.]+)\, start', res[0])
#         duration = time.strptime(match.group(1), '%H:%M:%S.%f')
#         return duration
#     except Exception as e:
#         return None


if __name__ == '__main__':

    str_opts = [s for s in sys.argv if '=' in s]
    opts = dict()
    for s in str_opts:
        k = s.split("=")[0]
        v = s.split("=")[1]
        opts[k] = v

    if 'target' not in opts.keys():
        print("specify location to write playlist to using target=")
        sys.exit(0)

    if 'wd' in opts.keys():
        os.chdir(opts['wd'])

    PlistController(opts)
