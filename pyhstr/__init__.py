"""History manager extension for the standard Python shell and IPython"""

__version__ = '0.0.3'

import curses
import sys

from pyhstr.application import main

hh = object()
original = sys.displayhook

def spam(arg):
    if arg == hh:
        curses.wrapper(main)
    else:
        original(arg)

sys.displayhook = spam
