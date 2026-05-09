#!/usr/bin/env python3

import pyghidra
from pathlib import Path
import shutil
import json
import os

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


def create_ghidra_project(binary_path_raw: str):
    binary_path = Path(binary_path_raw)

    aipiler_folder = Path(__file__).parent

    custom_storage = aipiler_folder / "Workspaces" / binary_path.stem
    custom_storage.mkdir(parents=True,exist_ok=False)

    workspace = custom_storage / (binary_path.stem+"-Workspace")
    ghidra_project_name = binary_path.stem + "-Ghidra"

    shutil.copytree(aipiler_folder / "Skeleton",workspace)

    project_data = {"project_name":ghidra_project_name,
                    "project_location":str(custom_storage / ghidra_project_name),
                    "program_location":"/"+binary_path.name
                    }

    with open(workspace/"project.aipiler","w") as f:
        f.write(json.dumps(project_data))


    pyghidra.start()

    from ghidra.base.project import GhidraProject
    from ghidra.program.flatapi import FlatProgramAPI
    from ghidra.program.util import GhidraProgramUtilities
    from ghidra.app.script import GhidraScriptUtil

    project_dir = custom_storage / ghidra_project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    project = GhidraProject.createProject(str(project_dir), ghidra_project_name, False)
    try:
        program = project.importProgram(binary_path)
        if program is None:
            raise RuntimeError(f"Ghidra failed to import '{binary_path}'.")
        project.saveAs(program, "/", binary_path.name, True)

        flat_api = FlatProgramAPI(program)
        if GhidraProgramUtilities.shouldAskToAnalyze(program):
            GhidraScriptUtil.acquireBundleHostReference()
            try:
                flat_api.analyzeAll(program)
                GhidraProgramUtilities.markProgramAnalyzed(program)
            finally:
                GhidraScriptUtil.releaseBundleHostReference()

        print(f"Project stored at: {custom_storage}")
    finally:
        project.save(program)
        project.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a Ghidra project for a binary.")
    parser.add_argument("binary_path", help="Path to the binary file to analyze")
    args = parser.parse_args()
    
    create_ghidra_project(args.binary_path)
