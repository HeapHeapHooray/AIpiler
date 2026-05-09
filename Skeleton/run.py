#!/usr/bin/env python3


import sys
import os
import subprocess
from pathlib import Path

management_folder = Path(__file__).parent / "Management"

sys.path.append(management_folder)
os.environ['PATH'] = str(management_folder.resolve()) + os.pathsep + os.environ['PATH']

os.chdir(management_folder)

os.system("""init_documentation.py && add_to_documentation.py --loop-till-all-are-tagged && echo "FULLY PROCESSED FOR NOW !" """)
