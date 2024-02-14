db = db.getSiblingDB('rinha');

db.createCollection('clientes');

db.clientes.createIndex({ id: 1 })

db.clientes.insertMany([
    {"id": 1, "saldo": 0, "limite": 100000, "ultimas_transacoes": []},
    {"id": 2, "saldo": 0, "limite": 80000, "ultimas_transacoes": []},
    {"id": 3, "saldo": 0, "limite": 1000000, "ultimas_transacoes": []},
    {"id": 4, "saldo": 0, "limite": 10000000, "ultimas_transacoes": []},
    {"id": 5, "saldo": 0, "limite": 500000, "ultimas_transacoes": []},
]);