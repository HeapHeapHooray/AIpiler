#!/usr/bin/env python3

import json

def get_model():
    model_file = Path(__file__).parent / "model.json"
    with open(model_file) as f:
        return json.loads(f.read())["model_used"]
    # "You never know!" - FALLBACK
    return "anthropic/claude-haiku-4-5"

import sys
import os
import subprocess
from pathlib import Path

tools_folder = Path(__file__).parent.parent / "Tools"
documentation_folder = Path(__file__).parent.parent / "1-Documentation"

 if (documentation_folder / "ARCHITECTURE.md").exists():
        print("Documentation has already been initialized !")
        exit()

sys.path.append(tools_folder)
os.environ['PATH'] = str(tools_folder.resolve()) + os.pathsep + os.environ['PATH']

os.chdir(documentation_folder)

def set_title(title):
    sys.stderr.write(f"\033]0;{title}\007")
    sys.stderr.flush()

set_title("init_documentation — Initializing Documentation...")

with open(documentation_folder / "FUNCTION_SIGNATURES.md","w") as f:
    f.write("""
# FUNCTION_SIGNATURES.md
## This file can be thought of as the index of all functions discussed in ARCHITECTURE.md and QUESTIONS.md.
### -- Signature Body Specification Start --
### <FUNCTION_NAME | FUNCTION_ADDRESS> - Size: LINES_OF_CODE
### TAGS: [...,...]
### Overview: "THE PURPOSE OF THIS FUNCTION"
### (PARAMETER_NAME_1) - "Description of it's purpose"
### (PARAMETER_NAME_2) - "Description of it's purpose"
### (PARAMETER_NAME_3) - "Description of it's purpose"
### ...
### Return: RETURN_TYPE - "Description of what it means in context."
### Special Notes: NONE
### -- Signature Body Specification End --
# SIGNATURES_INDEX   """)

subprocess.run(f"""opencode run -m {get_model()} "
-- Bash Commands --
aipiler_get_entry_function_name, gets the name or address of the entry function/point.
aipiler_list_functions, to see all functions.
aipiler_read_function_code <function_name>, to read a function's code.
--
Describe the architecture of the program in the Ghidra project using aipiler_get_entry_function_name, aipiler_list_functions, and aipiler_read_function_code, save it to ./ARCHITECTURE.md , it must be really precise and full of diagrams, with reviewed functions being specified and documented in ./FUNCTION_SIGNATURES.md (Read the specification in the file before writing.). If it helps, create a ./QUESTIONS.md file to add and answer questions related to the architecture.
Any file other than ./ARCHITECTURE.md , ./FUNCTION_SIGNATURES.md, and ./QUESTIONS.md should be stored in ./other_files
DO NOT ACCESS FILES OUTSIDE OF THE CWD." """, shell=True)
