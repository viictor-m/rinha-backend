"""Módulo responsável por rodar a API."""

from fastapi import FastAPI


app = FastAPI(title="API de crébitos da rinha de backend.")


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
