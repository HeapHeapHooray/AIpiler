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


def get_without_tag(project_location, project_name, program_path, tag_name, sort_size=False):
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

                fm = program.getFunctionManager()
                # Iterate through all functions in address order
                functions = fm.getFunctions(True)

                results = []
                for func in functions:
                    tags = func.getTags()
                    has_tag = False
                    for tag in tags:
                        if tag.getName() == tag_name:
                            has_tag = True
                            break

                    if not has_tag:
                        results.append({
                            "address": str(func.getEntryPoint()),
                            "name": func.getName(),
                            "size": func.getBody().getNumAddresses()
                        })

                if sort_size:
                    results.sort(key=lambda x: x["size"], reverse=True)
                    print(f"{'Address':<16} | {'Size':<10} | {'Function Name'}")
                    print("-" * 55)
                else:
                    print(f"{'Address':<16} | {'Function Name'}")
                    print("-" * 40)

                for res in results:
                    if sort_size:
                        entry = {"entry_point": f"{res['address']:<16}","function_size": f"{res['size']:<10}","function_name": res['name'] }
                        print(f"{res['address']:<16} | {res['size']:<10} | {res['name']}")
                    else:
                        entry = {"entry_point": f"{res['address']:<16}","function_name": res['name'] }
                    output.append(entry)

                print("-" * (55 if sort_size else 40))
                print(f"Total functions without tag '{tag_name}': {len(results)}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return output

def add_tag_to_function(project_location, project_name, program_path, function_name_or_address, tag_name):
    """
    Opens a Ghidra project and adds a tag to a specific function.
    """
    try:
        pyghidra.start()
    except Exception as e:
        print(f"Error starting Ghidra: {e}")
        return

    from pyghidra.api import open_project, program_context

    try:
        with open_project(project_location, project_name, create=False) as project:
            with program_context(project, program_path) as program:
                fm = program.getFunctionManager()
                target_func = None

                # Try to parse as an address first
                try:
                    addr = program.getAddressFactory().getAddress(function_name_or_address)
                    if addr is not None:
                         target_func = fm.getFunctionContaining(addr)
                except Exception:
                    pass

                # If it wasn't found by address, search by name
                if target_func is None:
                    functions = fm.getFunctions(True)
                    for func in functions:
                        if func.getName() == function_name_or_address:
                            target_func = func
                            break

                if target_func is None:
                    print(f"Error: Function '{function_name_or_address}' not found.")
                    return

                print(f"Adding tag '{tag_name}' to function: {target_func.getName()} at {target_func.getEntryPoint()}")

                # In Ghidra, all modifications must be in a transaction
                tx_id = program.startTransaction(f"Add tag {tag_name}")
                success = False
                try:
                    target_func.addTag(tag_name)
                    success = True
                except Exception as tx_err:
                    print(f"Failed to add tag: {tx_err}")
                finally:
                    program.endTransaction(tx_id, success)

                if success:
                    print(f"Successfully added tag '{tag_name}'.")
                    # Save the program to persist changes to the project
                    program.save("Added tag via AIpiler tool", None)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    tag_name = "Documented-1"

    project_aipiler = Path(__file__).parent / "project.aipiler"
    with open(project_aipiler) as f:
        data = json.loads(f.read())

    PROJ_LOC = data["project_location"]
    PROJ_NAME = data["project_name"]
    PROG_PATH = data["program_location"]

    without = get_without_tag(PROJ_LOC, PROJ_NAME, PROG_PATH, tag_name,sort_size=True)

    if len(without):
        tools_folder = Path(__file__).parent / "Tools"
        documentation_folder = Path(__file__).parent / "1-Documentation"

        sys.path.append(tools_folder)
        os.environ['PATH'] = str(tools_folder.resolve()) + os.pathsep + os.environ['PATH']

        os.chdir(documentation_folder)

        import shlex

        prompt_text = f"""
        aipiler_read_function_code <function_name>, to read a function's code.
        aipiler_add_tag_to_function <function_name> <tag_name>, to add a tag to a function in the Ghidra project.
        Describe the code of the function '<{without[0]}>' using aipiler_read_function_code, especially with regards to context, save it to ./ARCHITECTURE.md as you contribute to it and also refer to the ./QUESTIONS.md file to add and answer questions related to the architecture.
        Any file other than ./ARCHITECTURE.md and ./QUESTIONS.md should be stored in ./other_files
        Annotate the function being analyzed with aipiler_add_tag_to_function.
        DO NOT ACCESS FILES OUTSIDE OF THE CWD."""

        prompt = f"opencode run -m anthropic/claude-haiku-4-5 {shlex.quote(prompt_text)}"

        print(prompt)

        output = os.system(prompt)

        if not output:
            add_tag_to_function(PROJ_LOC, PROJ_NAME, PROG_PATH, str(without[0]["entry_point"]).strip(), tag_name)




