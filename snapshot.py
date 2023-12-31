# Creator: Ape Toshi
# Last edited: December 31st, 2023
# License: MIT

import argparse
import json
import os

from dotenv import load_dotenv
from web3 import Web3

if __name__ == "__main__":
    load_dotenv()

    with open("abi.json") as f:
        ABI = json.loads(f.read())

    parser = argparse.ArgumentParser(
        description="Create ERC-721 ownership snapshot.")

    parser.add_argument("-k", "--key", type=str, help="Infura API key.")
    parser.add_argument("-c", "--contract", type=str,
                        help="Ethereum contract address.")
    parser.add_argument("-f", "--first", type=int, help="First `tokenId`.")
    parser.add_argument("-l", "--last", type=int, help="Last `tokenId`.")

    args = parser.parse_args()

    INFURA_ID = args.key if args.key else os.getenv(
        "INFURA_ID") if os.getenv("INFURA_ID") else input("Infura API key: ")
    CONTRACT_ADDR = args.contract if args.contract else input(
        "Ethereum smart contract address: ")
    START = args.first if args.first else int(input("First `tokenId`: "))
    END = args.last if args.last else int(input("Last `tokenId`: "))

    w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_ID}"))

    multicall = w3.eth.contract(w3.to_checksum_address(
        "0x01e035926a4e5ae088dbb764a1f607510798cea8"), abi=ABI)

    collection = w3.to_checksum_address(CONTRACT_ADDR)

    response = multicall.functions.getOwners(collection, START, END).call()

    snapshot = {}
    for i, owner in enumerate(response, start=START):
        snapshot.update({i: owner})

    with open(f"{collection}_{START}-{END}.json", "w") as f:
        f.write(json.dumps(snapshot, indent=4))
    print(f"* Saved to: {collection}_{START}-{END}.json")
