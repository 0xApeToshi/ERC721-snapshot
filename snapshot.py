# Creator: Ape Toshi
# Last edited: July 17th, 2022
# License: MIT

import argparse
import json
import os

from dotenv import load_dotenv
from web3 import Web3

if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Create ERC-721 ownership snapshot.")

    parser.add_argument("-k", "--key", type=str, help="Infura API key.")
    parser.add_argument("-c", "--contract", type=str,
                        help="Ethereum contract address.")
    parser.add_argument("-f", "--first", type=int, help="First `tokenId`.")
    parser.add_argument("-l", "--last", type=int, help="Last `tokenId`.")

    args = parser.parse_args()

    INFURA_ID = args.key
    if not INFURA_ID:
        INFURA_ID = os.getenv("INFURA_ID")
        if not INFURA_ID:
            INFURA_ID = input("Infura API key: ")

    CONTRACT_ADDR = args.contract

    if not CONTRACT_ADDR:
        CONTRACT_ADDR = input("Ethereum smart contract address: ")

    # Start & end tokenId (inclusive)
    START = args.first
    if not START:
        START = int(input("First `tokenId`: "))
    END = args.last
    if not END:
        END = int(input("Last `tokenId`: "))

    with open("abi.json") as f:
        ABI = json.loads(f.read())

    w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_ID}"))

    multicall = w3.eth.contract(w3.toChecksumAddress(
        "0x01e035926a4e5ae088dbb764a1f607510798cea8"), abi=ABI)

    collection = w3.toChecksumAddress(CONTRACT_ADDR)

    response = multicall.functions.getOwners(collection, START, END).call()

    snapshot = {}
    for i, owner in enumerate(response, start=START):
        snapshot.update({i: owner})

    with open(f"{collection}_{START}-{END}.json", "w") as f:
        f.write(json.dumps(snapshot, indent=4))
    print(f"* Saved to: {collection}_{START}-{END}.json")
