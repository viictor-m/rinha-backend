"""Módulo responsável por rodar a API."""

from importlib import import_module

from fastapi import FastAPI

from src.clientes.rotas import rotas


app = FastAPI(title="API de crébitos da rinha de backend.")

app.include_router(rotas, prefix="/clientes", tags=["clientes"])

import_module("src.erros")


@app.get("/")
def hello() -> str:
    """
    Healthcheck da API de crébitos.

    Returns
    -------
    str
        Mensagem de boas-vindas.
    """
    return "API de crébitos da rinha de backend está on e roteando!"
