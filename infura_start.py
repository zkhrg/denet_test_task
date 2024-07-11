from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()

infura_token = os.getenv('INFURA_TOKEN')
infura_url = f'https://polygon-mainnet.infura.io/v3/{infura_token}'
web3 = Web3(Web3.HTTPProvider(infura_url))

# Проверка подключения
if web3.is_connected():
    print("connected to polygon")
else:
    print("failed to connect polygon")

raw_token_contract_address = '0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0'
token_contract_address = Web3.to_checksum_address(raw_token_contract_address)
token_contract_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    }
]

token_contract = web3.eth.contract(
    address=token_contract_address, abi=token_contract_abi)

raw_address = '0x51f1774249Fc2B0C2603542Ac6184Ae1d048351d'
address = Web3.to_checksum_address(raw_address)

balance = token_contract.functions.balanceOf(address).call()

decimals = 18
balance_in_tokens = balance / (10 ** decimals)

print(f"balance of addr {address}: {balance_in_tokens} tokens")
