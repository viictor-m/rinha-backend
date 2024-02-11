"""Testes do corpo da requisição de"""

import pytest

from pydantic import ValidationError

from src.clientes.esquemas import CorpoTransacao


@pytest.mark.parametrize(
    "entrada",
    [
        dict(valor=-10, tipo="c", descricao="teste."),
        dict(valor=10, tipo="a", descricao="teste."),
        dict(valor=10, tipo="d", descricao="testestetesteteste."),
    ],
)
def test_corpo_incorreto(entrada: dict) -> None:
    with pytest.raises(ValidationError) as e:
        CorpoTransacao(**entrada)
