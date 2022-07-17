# ERC721-snapshot
Make a snapshot of the current ERC721 token holders distribution.

# Requirements
Python >=3.7.0

# Setup
It's always a good idea to have a separate environment for each project.
However, I'm feeling a bit lazy so I'll show how to install packages globally

```bash
pip3 install -r requirements.txt
```

You can add a `.env` file with the `INFURA_ID="<your_key>"` instead of inputting it every time.

Run it either in interactive mode with

```bash
python3 snapshot.py
```

or parse command line args:

```bash
python3 snapshot.py -c 0xc36cb218848f173148ff55f4dfc18f1540fb7475 -f 1 -l 200
```