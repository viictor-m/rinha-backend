"""Módulo de testes da regra de negócio da transação."""

import pytest

from fastapi.exceptions import HTTPException

from src.clientes.esquemas import Transacao


@pytest.mark.parametrize(
    ("modelo", "valor", "esperado"),
    [
        (Transacao(limite=10, saldo=0), 10, 10),
        (Transacao(limite=10, saldo=-5), -5, -10),
        (Transacao(limite=10, saldo=0), -10, -10),
        (Transacao(limite=10, saldo=-5), 10, 5),
    ],
)
def test_transacoes_aceitas(modelo: Transacao, valor: int, esperado: int) -> None:
    modelo.saldo += valor
    assert modelo.saldo == esperado


@pytest.mark.parametrize(
    ("modelo", "valor"),
    [
        (Transacao(limite=10, saldo=0), -11),
        (Transacao(limite=10, saldo=-5), -6),
        (Transacao(limite=10, saldo=0), -100),
        (Transacao(limite=10, saldo=-5), -10),
    ],
)
def test_transacoes_nao_aceitas(modelo: Transacao, valor: int) -> None:
    with pytest.raises(HTTPException) as e:
        modelo.saldo += valor
