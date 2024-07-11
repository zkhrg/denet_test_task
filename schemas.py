from pydantic import BaseModel, Field
from typing import List


class GetBalanceBatchModel(BaseModel):
    addresses: List[str]


class GetBalanceBatchAnswer(BaseModel):
    balances: List[float]
