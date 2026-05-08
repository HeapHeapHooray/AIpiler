#!/usr/bin/env python3

import pyghidra
from pyghidra.api import open_project, program_context
import os
import sys
import json
from pathlib import Path

# Attempt to locate Ghidra if GHIDRA_INSTALL_DIR is not set
if 'GHIDRA_INSTALL_DIR' not in os.environ:
    # Common paths or the one we found
    possible_paths = [
        '/snap/ghidra/current/ghidra_12.0_PUBLIC',
        '/opt/ghidra',
        os.path.expanduser('~/ghidra')
    ]
    for path in possible_paths:
        if os.path.isdir(path):
            os.environ['GHIDRA_INSTALL_DIR'] = path
            break

def get_without_tag(project_location, project_name, program_path, tag_name):
    """
    Opens a Ghidra project and lists all functions that do not have the specified tag.
    """

    output = []

    try:
        # Initialize Ghidra
        pyghidra.start()
    except Exception as e:
        print(f"Error starting Ghidra: {e}")
        print("Please ensure GHIDRA_INSTALL_DIR is set correctly.")
        return

    try:
        # Open the existing project
        with open_project(project_location, project_name, create=False) as project:
            # Open the specific program context
            with program_context(project, program_path) as program:
                print(f"Successfully opened: {program.getName()}")
                print(f"{'Address':<16} | {'Function Name'}")
                print("-" * 40)
                
                fm = program.getFunctionManager()
                # Iterate through all functions in address order
                functions = fm.getFunctions(True)
                
                count = 0
                for func in functions:
                    tags = func.getTags()
                    has_tag = False
                    for tag in tags:
                        if tag.getName() == tag_name:
                            has_tag = True
                            break
                    
                    if not has_tag:
                        output.append(f"{str(func.getEntryPoint()):<16} | {func.getName()}")
                        count += 1
                
                print("-" * 40)
                print(f"Total functions without tag '{tag_name}': {count}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return output

if __name__ == "__main__":
    tag_name = "Documented-1"

    project_aipiler = Path(__file__).parent / "project.aipiler"
    with open(project_aipiler) as f:
        data = json.loads(f.read())

    PROJ_LOC = data["project_location"]
    PROJ_NAME = data["project_name"]
    PROG_PATH = data["program_location"]

    without = get_without_tag(PROJ_LOC, PROJ_NAME, PROG_PATH, tag_name)

    if len(without):
        tools_folder = Path(__file__).parent / "Tools"
        documentation_folder = Path(__file__).parent / "1-Documentation"

        sys.path.append(tools_folder)
        os.environ['PATH'] = str(tools_folder.resolve()) + os.pathsep + os.environ['PATH']

        os.chdir(documentation_folder)

        prompt = f"""opencode run -m anthropic/claude-haiku-4-5 "
aipiler_read_function_code <function_name>, to read a function's code.
Describe the code of the function '<{without[0]}>' using aipiler_read_function_code, especially with regards to context, save it to ./ARCHITECTURE.md as you contribute to it and also refer to the ./QUESTIONS.md file to add and answer questions related to the architecture.
Any file other than ./ARCHITECTURE.md and ./QUESTIONS.md should be stored in ./other_files
DO NOT ACCESS FILES OUTSIDE OF THE CWD." """

        print(prompt)

        os.system(prompt)



