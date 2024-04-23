from pydantic import BaseModel
from typing import List

class Case(BaseModel):
    id: int
    meta: dict[str, list[list[str]]]
    steps: List[dict]

class Suite(BaseModel):
    name: str
    case_list: List[Case]
