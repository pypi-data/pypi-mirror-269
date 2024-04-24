# import subprocess
import time

from ..ibuiltins.get_filemtime import get_filemtime
from ..iconsole.print_log import print_log
from ..iconsole.console_run import console_run


def auto_reload(filename):
    """
    Menjalankan file python secara berulang.
    Dengan tujuan untuk melihat perubahan secara langsung.
    Pastikan kode aman untuk dijalankan.
    Jalankan kode ini di terminal console.

    ```py
    if __name__ == "__main__":
        auto_reload("file_name.py")
    ```
    """
    mtime = get_filemtime(filename)
    last_mtime = 0
    cmd = f"python {filename}"

    try:
        print_log("Start")
        while True:
            last_mtime = mtime
            console_run(cmd, print_info=False)
            # subprocess.run(cmd, shell=True)
            while mtime == last_mtime:
                time.sleep(1)
                mtime = get_filemtime(filename)
            print_log("Reload")
    except KeyboardInterrupt:
        print_log("Stop")
