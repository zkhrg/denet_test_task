import asyncio
from typing import List, Tuple
from web3 import Web3
#
from third_party_api_conns import infura_connect


async def get_top_addresses_by_balance(web3: Web3, raw_token: str, n: int) -> List[Tuple[str, float]]:
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

    #
    addresses_with_balance = await asyncio.gather(*[token_contract.functions.balanceOf.call(address) for address in web3.eth.accounts])

    #
    sorted_addresses = sorted(
        zip(web3.eth.accounts, addresses_with_balance), key=lambda x: x[1], reverse=True)

    #
    top_addresses = sorted_addresses[:n]

    return top_addresses


async def main():
    web3, _ = infura_connect()  #

    #
    raw_token = '0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0'
    n = 10  #

    top_addresses = await get_top_addresses_by_balance(web3, raw_token, n)
    print(f"Top {n} addresses by balance:")
    for address, balance in top_addresses:
        print(f"{address}: {balance}")

if __name__ == "__main__":
    asyncio.run(main())
