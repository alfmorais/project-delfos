# Project Delfos - API Conector e Banco de Dados Fonte

Projeto tem como objetivo implementar a API para expor dados de registros histórico de geração de energia.

## Tecnologias:

- Python 3.12
- FastAPI 0.111.0
- Docker version 26.1.4, build 5650f9b
- Docker Compose version v2.27.1-desktop.1
- Postgres latest
- Pytest 8.2.2

## Rode o projeto:

- Renome o arquivo `.env.example` para -> `.env`
- Faça o build do projeto com o comando: `task build`
- Rode os testes com o comando: `task test`
- Suba o projeto com o comando: `task run`

## Dados de Testes:

- Use o endpoint POST `/v1/data/bulk-data` para criar os dados de testes:

Payload:
```python
{
    "start_day": "2024-07-19T19:05:19.432Z",
    "duration": 0
}
```

Após criar os dados de testes pegue o range de timestamps para fazer a chamada no endpoint de listar registros: 

- Inicial: `1721408898`
- Final: `1722308718`