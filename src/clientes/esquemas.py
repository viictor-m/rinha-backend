"""Esquemas pydantic utilizados para padronização de entradas e saídas da API."""

from typing import Literal

from pydantic import BaseModel
from pydantic import Field


class CorpoTransacao(BaseModel):

    valor: int = Field(gt=0)
    tipo: Literal["c", "d"]
    descricao: str = Field(min_length=1, max_length=10)
