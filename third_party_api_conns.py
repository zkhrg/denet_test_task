from dotenv import load_dotenv
from typing import Tuple
import os
from web3 import Web3, HTTPProvider


def infura_connect() -> Tuple[Web3, bool]:
    infura_token = os.getenv('INFURA_TOKEN')
    infura_url = f'https://polygon-mainnet.infura.io/v3/{infura_token}'
    web3 = Web3(Web3.HTTPProvider(infura_url))

    return (web3, web3.is_connected())
