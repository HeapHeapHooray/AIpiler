# AIpiler

**Automated binary decompilation and reverse engineering, powered by AI and Ghidra.**

AIpiler feeds a compiled binary into Ghidra for static analysis, then turns an AI agent loose on the decompiled output. The agent reads decompiled C, builds an architectural understanding of the program, documents every function, renames symbols to meaningful names, and — ultimately — produces compilable source code that matches the original binary. All without opening the Ghidra GUI.

---

## Architecture

```
AIpiler/
├── create_ghidra_project.py     # Ingest a binary: import into Ghidra, stamp out workspace
├── Skeleton/                    # Template copied per binary into Workspaces/
│   ├── run.py                   # Orchestrator: runs the full documentation pipeline
│   ├── Management/
│   │   ├── model.json           # AI model selection
│   │   ├── init_documentation.py
│   │   ├── add_to_documentation.py
│   │   ├── init_annotation_weights.py
│   │   └── annotate.py
│   ├── Tools/                   # CLI tools bridging the AI agent to Ghidra
│   │   ├── aipiler_list_functions
│   │   ├── aipiler_read_function_code
│   │   ├── aipiler_get_entry_function_name
│   │   ├── aipiler_add_tag_to_function
│   │   ├── aipiler_get_all_tags
│   │   ├── aipiler_get_with_tag / aipiler_get_without_tag
│   │   ├── aipiler_get_less_than_n_tags
│   │   └── aipiler_rename_function
│   ├── 1-Documentation/
│   │   └── opencode.json        # AI sandbox policy for phase 1
│   └── 2-Annotation/
│       └── opencode.json        # AI sandbox policy for phase 2
└── Workspaces/                  # Generated — one subdirectory per analyzed binary
```

Each binary gets its own isolated workspace cloned from `Skeleton/`, so multiple binaries can be analyzed in parallel without interference.

The AI agent is sandboxed per phase via `opencode.json`: it may only read/write specific markdown files and its own `other_files/` directory, and may only invoke `aipiler_*` tools — no arbitrary shell access.

---

## Dependencies

- [Ghidra](https://snapcraft.io/ghidra) — static analysis engine
- [pyghidra](https://pypi.org/project/pyghidra/) — Python bindings for Ghidra's Java API
- [OpenCode](https://opencode.ai/) — AI agent framework

---

## Setup

**1. Install dependencies**

```bash
snap install ghidra           # or download from https://ghidra-sre.org
pip install pyghidra
# install OpenCode per https://opencode.ai/docs
```

**2. Configure OpenCode authentication**

The default model has been changed to `deepseek-v4-flash` (`deepseek/deepseek-v4-flash`) because it is extraordinarily cheaper and able to decompile effectively. Set up your API key per the [OpenCode auth docs](https://opencode.ai/docs).

**3. Clone the repo**

```bash
git clone https://github.com/HeapHeapHooray/AIpiler
cd AIpiler
```

**4. (Optional) Set Ghidra install path**

The scripts auto-detect common install locations (`/snap/ghidra/current/ghidra_12.0_PUBLIC`, `/opt/ghidra`, `~/ghidra`). If yours differs:

```bash
export GHIDRA_INSTALL_DIR="/path/to/ghidra"
```

---

## Usage

**Step 1 — Ingest a binary**

```bash
python3 create_ghidra_project.py /path/to/your/binary
```

This imports the binary into Ghidra, runs full auto-analysis, and creates a workspace at `Workspaces/<binary_name>/`.

**Step 2 — Run the AI documentation loop**

```bash
cd Workspaces/<binary_name>/<binary_name>-Workspace
python3 run.py
```

The agent will:
1. Generate `ARCHITECTURE.md` — a high-level map of the binary's structure
2. Iterate over every function in batches (largest first), reading decompiled C and documenting each in `FUNCTION_SIGNATURES.md`
3. Tag each function `Documented-1` inside Ghidra as it goes

The loop runs until all functions are tagged. You can interrupt and re-run `run.py` at any time — already-tagged functions are skipped.

---

## Changing the AI model

By default, the model is set to `"deepseek/deepseek-v4-flash"`. You can change this by editing `Management/model.json` inside your workspace:

```json
{"model_used": "deepseek/deepseek-v4-flash"}
```

Any model supported by OpenCode can be used here (e.g., `"anthropic/claude-3-5-sonnet"`).

---

## Current status

AIpiler currently **annotates and documents** the Ghidra project — it renames symbols, tags functions, and produces architecture and function signature documentation. **It does not yet compile or reconstruct source code.** The end goal of generating compilable source that matches the original binary is planned but not yet implemented.

---

## Design notes

**Tag-based progress tracking** — AIpiler uses Ghidra's native function tagging as a persistent progress store. No external database needed; tags survive process restarts and are visible inside the Ghidra GUI.

**Batched processing, largest first** — Functions are sorted by decompiled body size descending and processed in batches of 10. Large functions carry the most semantic weight and establish the architectural context that makes smaller functions easier to understand.

**Lock-retry robustness** — All `Tools/` scripts detect Ghidra project lock contention and retry automatically, so the AI agent never crashes on a busy project.

**Fully headless** — The entire pipeline runs without the Ghidra GUI. All analysis, decompilation, and symbol mutation happens through `pyghidra` and Ghidra's `FlatProgramAPI`.
