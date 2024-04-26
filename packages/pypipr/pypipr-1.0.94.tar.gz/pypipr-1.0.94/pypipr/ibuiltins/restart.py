import os
import sys


def restart():
    e = sys.executable
    a = sys.argv
    os.execl(e, e, *a)
