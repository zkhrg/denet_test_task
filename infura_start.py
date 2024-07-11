from dotenv import load_dotenv
import os
from web3 import Web3
from time import time
import asyncio
from typing import List
from concurrent.futures import ThreadPoolExecutor
from third_party_api_conns import infura_connect

load_dotenv()


async def get_balance_async(web3: Web3, raw_token: str, raw_address: str) -> float:
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, get_balance, web3, raw_token, raw_address)


def get_balance(web3: Web3, raw_token: str, raw_address: str) -> float:
    token_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        }
    ]
    token = Web3.to_checksum_address(raw_token)
    token_contract = web3.eth.contract(
        address=token,
        abi=token_abi,
    )
    address = Web3.to_checksum_address(raw_address)
    balance = token_contract.functions.balanceOf(address).call()
    decimals = 18
    balance_in_tokens = balance / (10 ** decimals)

    return balance_in_tokens


async def get_balance_batch(web3: Web3, raw_token: str, raw_addresses: List[str]):
    tasks = [get_balance_async(web3, raw_token, address)
             for address in raw_addresses]
    return await asyncio.gather(*tasks)


async def main():
    web3, _ = infura_connect()

    raw_token = '0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0'
    raw_address = '0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d'
    addresses = [raw_address] * 10

    t = time()
    r = await get_balance_batch(web3, raw_token, addresses)
    v = time()
    print(r)
    print(f"Time taken for asynchronous calls: {v - t}")

    t = time()
    for _ in range(10):
        get_balance(web3, raw_token, raw_address)
    v = time()
    print(f"Time taken for synchronous calls: {v - t}")

if __name__ == "__main__":
    asyncio.run(main())
