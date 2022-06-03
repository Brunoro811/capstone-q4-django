# Stokar - Api de Controle de Estoque

### A Stokar de Estoque Api faz o controle do estoque e vendas de várias lojas de pertencentes a uma mesma empresa. Possui dois tipos de usuários administrador e vendedor.

<br/>

> Status: Versão 1.0

> [![NPM](https://img.shields.io/github/license/Brunoro811/capstone-q4-django?style=for-the-badge)](https://github.com/Brunoro811/capstone-q4-django/blob/development/LICENSE)

<br/>

# Sobre o Projeto

### Base url da api

https://stokar-app.herokuapp.com/

### Documentação da API

https://stokar-app.herokuapp.com/docs/

**Controle de Estoque Api** é uma aplicação de serviço construida para controle de estoque de uma micro empresa com uma ou vários lojas. Esta aplicação foi desenvolvida com o Python, Django e Rest Framework.

# Metodologias Ágeis

- Kanban
- SCRUM

# Tecnologias Utilizadas

- Python
- Django
- Django Rest Framework
- Banco de dados Relacional
- Lucidchart
- CI Github Actions
- CD Heroku
- Notion
- TDD
- Generics View

# Bibliotecas Utilizadas

- python-dotenv
- rest_framework
- coreapi
- openapi
- Faker
- Django
- Dotenv ( conferir a integração de arquivos .env com Django )
- Pylint ( Linter )
- Black ( Formatter )
- Django On Heroku Lib

# Como executar

Pré-requisitos : python 3.9, biblioteca pip.

Executa:
1 - Criar um ambiente vitual venv :

```bash
python -m venv venv
```

2 - Ativar um ambiente vitual venv :

```bash
source venv/bin/activate
```

3 - Instalar as bibliotecas que estão no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

4 - Criar um arquivo .env com os dados de .env.example e subistituie pelos seus dados os campos:

|       Variavel | Descrição                       |
| -------------: | :------------------------------ |
|       DATABASE | Nome do ando de dados           |
|           PORT | Porta do banco                  |
|           HOST | host                            |
|           USER | Usuário do banco                |
|       PASSWORD | Senha do banco                  |
|     ADMIN_NAME | Administrador padrão do sistema |
| ADMIN_PASSWORD | Senha do administrador          |
|    ADMIN_EMAIL | Email do administrador          |
|     SECRET_KEY | Secret key                      |
|           TEST | Para ambiente de test           |

5 - Rodar as migrações

```bash
    python manage.py migrate

```

9 - Rodar o servidor

```bash
python manage.py runserver
```

## Authors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table textAlign="center" style="margin: 0 auto;">
  <tr>
    <td align="center" title="Bruno"><a href="https://github.com/Brunoro811"><img  src="https://avatars.githubusercontent.com/u/82813383?v=4" width="100px;" alt=""/><br />
    </td>    
    <td align="center" title="Julia"><a href="https://github.com/juliagamaol"><img src="https://avatars.githubusercontent.com/u/86054348?v=4" width="100px;" alt=""/><br />
    </td>    
    <td align="center" title="Bruno"><a href="https://github.com/pedromenimen"><img src="https://avatars.githubusercontent.com/u/77471145?v=4" width="100px;" alt=""/><br />
    </td>
    <td align="center" title="Bruno"><a href="https://github.com/Poketnans"><img src="https://avatars.githubusercontent.com/u/82735052?v=4" width="100px;" alt=""/><br />
    </td>    
  </tr>
</table>
<hr/>
