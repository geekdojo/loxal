#!/usr/bin/env python3
from pydantic import BaseModel

class Position(BaseModel):
    Value: int