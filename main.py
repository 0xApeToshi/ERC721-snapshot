# Creator: Ape Toshi
# Last edited: February 14th, 2022
# License: MIT

import json
import os
from collections import deque
from time import time

import requests
from dotenv import load_dotenv
from web3 import Web3


class QueueWindow:
    def __init__(self, max_size):
        self.q = deque()
        self.max_size = max_size
        self._len = 0

    def get_len(self):
        # len starts at 0 and increases up to max_size
        return self._len

    def get_sum(self):
        return sum(self.q)

    def __repr__(self):
        return str(list(self.q))

    def add(self, element):
        """Add an element to the queue. Caps the max size."""
        self.q.append(element)
        self._len += 1

        if self._len == self.max_size:
            # Update the function, just for fun :)
            def add(element):
                self.q.append(element)
                self.q.popleft()
            self.add = add


if __name__ == "__main__":
    load_dotenv()

    # Start & end tokenId (inclusive)
    START = 1
    END = 15

    TOTAL = END - START + 1

    # Contract address (needs to be verified to get ABI)
    CONTRACT_ADDR = "0x1cBB182322Aee8ce9F4F1f98d7460173ee30Af1F"

    # Needs a .env file in the same folder
    INFURA_ID = os.getenv("INFURA_ID")

    url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={CONTRACT_ADDR}"

    w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_ID}"))

    response = requests.get(url)
    ABI = json.loads(response.json().get("result"))

    contract = w3.eth.contract(w3.toChecksumAddress(CONTRACT_ADDR), abi=ABI)

    snapshot = {}
    window = QueueWindow(10)

    eta = "?"
    animation = "|/-\\"
    for i, tokenId in enumerate(range(START, END+1)):
        t1 = time()

        wallet_owner = contract.functions.ownerOf(tokenId).call()
        if snapshot.get(wallet_owner):
            # If the wallet owns multiple tokens
            snapshot[wallet_owner].append(tokenId)
        else:
            # If the wallet appears for the first time,
            # make a list and add the found token to it
            snapshot.update({wallet_owner: [tokenId]})
        t2 = time()
        window.add(t2-t1)
        remaining = TOTAL - i - 1
        # Find the average time and multiply by remaining

        if i % 10 == 0:
            eta = round(remaining * window.get_sum()/window.get_len(), 1)

        print(
            f"{animation[i % len(animation)]} {tokenId:5}/{END} | ETA: {eta:9.2f}s", end="\r")

    print("--> Saving to snapshot.txt")
    with open("snapshot.txt", "w") as f:
        f.write(json.dumps(snapshot))
    print("--> Done!")
