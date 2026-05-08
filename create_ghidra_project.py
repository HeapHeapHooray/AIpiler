import pyghidra
from pathlib import Path


def create_ghidra_project(binary_path_raw: str):
    binary_path = Path(binary_path_raw)
    custom_storage = Path.cwd() / binary_path.stem
    custom_storage.mkdir(parents=True,exist_ok=False)

    with pyghidra.open_program(
        binary_path, 
        project_location=custom_storage, 
        project_name=binary_path.stem + "-Ghidra",
        analyze=True  # Ensure analysis runs in this specific project
    ) as flat_api:
        program = flat_api.getCurrentProgram()
        print(f"Project stored at: {custom_storage}")
