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
aipiler_get_all_tags, outputs a list of all function tags in the Ghidra project.
Weight the degree of importance of each tag in ./WEIGHTED_TAGS.md, taking ARCHITECTURE.md into consideration.
Any file other than ./ARCHITECTURE.md ,./QUESTIONS.md , and ./WEIGHTED_TAGS.md should be stored in ./other_files
DO NOT ACCESS FILES OUTSIDE OF THE CWD." """)
