import platform
import os

__version__ = "1.1.0"

config_root = ''
if 'linux' in platform.system().lower():
    config_root = os.path.join(os.path.expanduser('~'), '.magic-toolkit')
