# ERC721-snapshot
Make a snapshot of the current ERC721 token holders distribution.

![Demo gif](https://github.com/0xApeToshi/ERC721-snapshot/blob/main/demo.gif)

# Requirements
Python >=3.7.0

# Setup
It's always a good idea to have a separate environment for each project.
However, I'm feeling a bit lazy so I'll show how to install packages globally

```bash
pip install -r requirements.txt
```

Add a `.env` file with the `INFURA_ID` and `ETHERSCAN_API` variables.
In the `main.py` file change the `CONTRACT_ADDR`, `START` and `END` variables.

Finally, run it with:

```bash
python main.py
```
