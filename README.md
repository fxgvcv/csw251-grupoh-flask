# SARC

Este é o projeto **SARC**.

## Como rodar localmente

1. Crie um ambiente virtual Python (versão 3.11):

  ```bash
  python3.11 -m venv venv
  source venv/bin/activate
  ```

2. Instale as dependências:

  ```bash
  pip install -r requirements.txt
  ```

3. Exporte as variáveis de ambiente e inicie o servidor Flask:

  ```bash
  export FLASK_APP=src.app
  export FLASK_ENV=development
  flask run
  ```

## Deploy

- Utilizamos **Terraform** para criar a base da infraestrutura.
- Utilizamos **Serverless Framework** para provisionar recursos ligados à aplicação, como API Gateway e AWS Lambda.

## Estrutura

```
sarc/
├── psycopg2*             # Arquivos da dependência psycopg2 para uso na função Lambda
├── src/                  # Código-fonte da aplicação
│   ├── app.py            # Ponto de entrada principal (Flask)
│   ├── models/           # Modelos de dados
│   ├── routes/           # Rotas/endpoints da API
│   └── services/         # Lógica de negócio e serviços auxiliares
├── tests/                # Testes automatizados
├── requirements.txt      # Dependências Python
├── serverless.yml        # Configuração do Serverless Framework
├── terraform/            # Scripts e módulos Terraform
└── README.md             # Documentação do projeto
```
