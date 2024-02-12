"""Esquemas pydantic utilizados para padronização de entradas e saídas da API."""

from datetime import datetime
from typing import Literal

from dateutil import tz
from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import ValidationInfo
from pydantic import field_validator


class CorpoTransacao(BaseModel):
    """
    Corpo da requisição /clientes/{id}/transacoes.

    Parameters
    ----------
    valor : int
        Valor a ser creditado/debitado do saldo do cliente. Deve sempre ser um número
        inteiro positivo.
    tipo : Literal["c", "d"]
        Tipo de transação a ser feita. c = Crédito | d = Débito.
    descricao : str
        Breve descrição da transação. Deve ter no mínimo 1 caracter e no máximo 10.
    """

    valor: int = Field(gt=0)
    tipo: Literal["c", "d"]
    descricao: str = Field(min_length=1, max_length=10)


class RegistroTransacao(CorpoTransacao):
    """
    Registro do banco de dados da transação efetuada.

    Parameters
    ----------
    valor : int
        Valor a ser creditado/debitado do saldo do cliente. Deve sempre ser um número
        inteiro positivo.
    tipo : Literal["c", "d"]
        Tipo de transação a ser feita. c = Crédito | d = Débito.
    descricao : str
        Breve descrição da transação. Deve ter no mínimo 1 caracter e no máximo 10.
    registrada_em : datetime
    """

    registrada_em: datetime = Field(
        default_factory=datetime.now
    )


class Transacao(BaseModel):
    """
    Registro para efeturar uma transação.

    Parameters
    ----------
    limite : int
        Limite de crédito do usuário.
    saldo : int
        Saldo do usuário
    """

    limite: int
    saldo: int
    model_config = ConfigDict(validate_assignment=True)

    @field_validator("saldo")
    def checar_limite_saldo(cls, valor: int, info: ValidationInfo) -> None:
        if valor < (-1 * info.data["limite"]):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Saldo insuficiente para completar transação.",
            )
        return valor
