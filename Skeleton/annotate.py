#!/usr/bin/env python3

import sys
import os
from pathlib import Path

tools_folder = Path(__file__).parent / "Tools"
annotation_folder = Path(__file__).parent / "2-Annotation"

sys.path.append(tools_folder)
os.environ['PATH'] = str(tools_folder.resolve()) + os.pathsep + os.environ['PATH']

os.chdir(annotation_folder)

os.system("""opencode run -m anthropic/claude-haiku-4-5 "
aipiler_get_with_tag <tag_name>, outputs the list of all functions with the specified tag.
aipiler_read_function_code <function_name>, to read a function's code.
aipiler_rename_function <function_name> <new_name>, rename a function's name or address to a new name.
Use aipiler_get_with_tag with the weighted tags on ./WEIGHTED_TAGS.md, rename functions with aipiler_rename_function, reading their code with aipiler_read_function_code alomg with taking all what was learned through the process of making ARCHITECTURE.md into consideration of the name choice.
Any file other than ./ARCHITECTURE.md ,./QUESTIONS.md , and ./WEIGHTED_TAGS.md should be stored in ./other_files
DO NOT ACCESS FILES OUTSIDE OF THE CWD." """)
