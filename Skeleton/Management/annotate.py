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
annotation_folder = Path(__file__).parent.parent / "2-Annotation"

sys.path.append(tools_folder)
os.environ['PATH'] = str(tools_folder.resolve()) + os.pathsep + os.environ['PATH']

os.chdir(annotation_folder)

subprocess.run(f"""opencode run -m {get_model()} "
aipiler_get_with_tag <tag_name>, outputs the list of all functions with the specified tag.
aipiler_read_function_code <function_name>, to read a function's code.
aipiler_rename_function <function_name> <new_name>, rename a function's name or address to a new name.
Use aipiler_get_with_tag with the weighted tags on ./WEIGHTED_TAGS.md, rename functions with aipiler_rename_function, reading their code with aipiler_read_function_code along with the expertise of ARCHITECTURE.md and FUNCTION_SIGNATURES.md for the name choice.
Any file other than ./ARCHITECTURE.md , ./QUESTIONS.md , ./FUNCTION_SIGNATURES.md , and ./WEIGHTED_TAGS.md should be stored in ./other_files
DO NOT ACCESS FILES OUTSIDE OF THE CWD." """, shell=True)
