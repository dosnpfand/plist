# platform specific setting here
import platform
import os

if platform.system() == "Linux":
    KEY_BACKSPACE = 263
    CMD = "mplayer -fs -really-quiet -playlist"
else:
    KEY_BACKSPACE = 8

    exec_list = [
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    ]

    for fpath in exec_list:
        if os.path.exists(fpath):
            vlc_exec = fpath
            break

    CMD = f'"{vlc_exec}" --fullscreen'
