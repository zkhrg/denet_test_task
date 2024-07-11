from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import GetBalanceBatchModel, GetBalanceBatchAnswer
from infura_start import get_balance_batch_internal, get_balance_async, logger
from third_party_api_conns import infura_connect
import asyncio


raw_token = "0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0"
web3, conn = infura_connect()
router = APIRouter()


@router.get("/get_balance")
async def get_balance(address: str = Query(None)):
    """ Returns a balance by address"""

    if conn:
        return await get_balance_async(web3, raw_token, address)
    logger.info("cant connect to infura")
    return "err"


@router.post("/get_balance_batch/", response_model=GetBalanceBatchAnswer)
async def get_balance_batch(arg: GetBalanceBatchModel):
    """Async returns a balance batch by address batch"""

    if conn:
        return {"balances": await get_balance_batch_internal(web3, raw_token, arg.addresses)}
    logger.info("cant connect to infura")
    return {"balances": [0.0]}
