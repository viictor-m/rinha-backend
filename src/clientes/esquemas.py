"""Esquemas pydantic utilizados para padronização de entradas e saídas da API."""

from datetime import datetime
from typing import Any
from typing import Literal

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import ValidationInfo
from pydantic import computed_field
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

    registrada_em: datetime = Field(default_factory=datetime.now)


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


class Extrato(BaseModel):
    """
    Classe para estrutura de dados do extrato.

    Parameters
    ----------
    saldo : int
        Saldo atualizado do usuário.
    limite : int
        Limite de crédito do usuário.
    ulimas_transacoes : list[RegistroTransacao]
        Registro das últimas 10 transações.
    """

    saldo: int
    limite: int
    ultimas_transacoes: list[RegistroTransacao]

    @computed_field
    def resposta(self) -> dict[str, Any]:
        """
        Resposta da API no formato pedido da rinha.

        Returns
        -------
        dict[str, Any]
            Reposta no fomato correto.
        """
        return {
            "saldo": {
                "total": self.saldo,
                "data_extrato": datetime.now(),
                "limite": self.limite,
            },
            "ultimas_transacoes": self.ultimas_transacoes,
        }
