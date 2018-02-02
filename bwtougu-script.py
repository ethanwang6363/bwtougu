#!"C:\Program Files\Anaconda3\envs\python3.6\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'bwtougu==0.0.1','console_scripts','bwtougu'
__requires__ = 'bwtougu==0.0.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('bwtougu==0.0.1', 'console_scripts', 'bwtougu')()
    )
