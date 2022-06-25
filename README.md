# root-explorer
Explore ROOT files from the terminal

### How to use

The core idea of this project is to explore ROOT files as fast as possible.
In order to do that a very clean cli is required. That is why executing root-explorer is as simple as
```bash
root-explorer /path/to/root/file.root
```
which will automatically select the first TTree of the ROOT file, read all branches
and prompt the user to select them.

Alternatively, if one wants to select a TTree, it is just
```bash
root-explorer /path/to/root/file.root TheTree
```

A preliminar python version is included to give a sneak peak of the advantages of this
script. The final version will be written in rust, though.



### Requirements

- **kitty**, terminal emulator is required to preview plots
- **fzf**, fuzzy finder is required to select branches

#### Python-version requirements
A python3 should be installed. All needed modules can be installed as
```bash
python3 -m pip install -r requirements.txt
```
