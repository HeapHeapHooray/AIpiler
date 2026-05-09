#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

tools_folder = Path(__file__).parent.parent / "Tools"
documentation_folder = Path(__file__).parent.parent / "1-Documentation"

sys.path.append(tools_folder)
os.environ['PATH'] = str(tools_folder.resolve()) + os.pathsep + os.environ['PATH']

os.chdir(documentation_folder)

subprocess.run("""opencode run -m anthropic/claude-haiku-4-5 "
aipiler_get_entry_function_name, gets the name or address of the entry function/point.
aipiler_list_functions, to see all functions.
aipiler_read_function_code <function_name>, to read a function's code.
Describe the architecture of the program in the Ghidra project using aipiler_get_entry_function_name, aipiler_list_functions, and aipiler_read_function_code, save it to ./ARCHITECTURE.md, it must be really precise and full of diagrams. If it helps, create a ./QUESTIONS.md file to add and answer questions related to the architecture.
Any file other than ./ARCHITECTURE.md and ./QUESTIONS.md should be stored in ./other_files
DO NOT ACCESS FILES OUTSIDE OF THE CWD." """, shell=True)
