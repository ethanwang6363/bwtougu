#!"c:\Program Files\Anaconda3\envs\python3.6\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'byrobot==1.0.3','console_scripts','byrobot'
__requires__ = 'byrobot==1.0.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('byrobot==1.0.3', 'console_scripts', 'byrobot')()
    )
