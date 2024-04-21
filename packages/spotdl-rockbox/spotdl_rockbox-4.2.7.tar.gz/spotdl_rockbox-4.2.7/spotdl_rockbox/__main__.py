"""
Main module for spotdl. Exports version and main function.
"""

from spotdl_rockbox._version import __version__
from spotdl_rockbox.console import console_entry_point

if __name__ == "__main__":
    console_entry_point()
