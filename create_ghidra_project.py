import pyghidra
from pathlib import Path
import shutil
import json

def create_ghidra_project(binary_path_raw: str):
    binary_path = Path(binary_path_raw)
    custom_storage = Path.cwd() / binary_path.stem
    custom_storage.mkdir(parents=True,exist_ok=False)

    workspace = custom_storage / (binary_path.stem+"-Workspace")
    ghidra_project_name = binary_path.stem + "-Ghidra"

    shutil.copytree(Path.cwd() / "Skeleton",workspace)

    project_data = {"project_name":ghidra_project_name,
                    "project_location":str(custom_storage / ghidra_project_name),
                    "program_location":"/"+binary_path.name
                    }

    with open(workspace/"project.aipiler","w") as f:
        f.write(json.dumps(project_data))


    with pyghidra.open_program(
        binary_path, 
        project_location=custom_storage, 
        project_name=ghidra_project_name,
        analyze=True  # Ensure analysis runs in this specific project
    ) as flat_api:
        program = flat_api.getCurrentProgram()
        print(f"Project stored at: {custom_storage}")
