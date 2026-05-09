# AIpiler     
## A project for automated decompilation of programs using AI and Ghidra.      

# Dependencies
### [ghidra](https://snapcraft.io/ghidra)   
### [pyghidra](https://pypi.org/project/pyghidra/)   
### [OpenCode](https://opencode.ai/)   

# Setting up
### 1. Install dependencies.   
### 2. Configure OpenCode auth, by default the project uses Anthropic Claude.
### 3. Clone the repo `git clone https://github.com/HeapHeapHooray/AIpiler`   
### 4. If the scripts don't find your Ghidra install dir, you may need to do `export GHIDRA_INSTALL_DIR="<path-here>"` before running them.  

# How-to-use
### 1. Run `python3 create_ghidra_project.py <PATH_TO_YOUR_BINARY_HERE>`
### 2. Wait a little, and you should have a fully working project at the newly created *Workspaces* folder inside the repo.
### 3. Navigate (`cd`) to `Workspaces/Project/Project-Workspace`
### 4. Run `python3 run.py`
### 5. You are already automatically documenting your first binary !
   
