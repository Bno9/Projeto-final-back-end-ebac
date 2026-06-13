# Projeto-final-back-end-ebac

# Proposta do curso

Desenvolver uma API completa, inspirada na PokéAPI.

## Desenvolvimento da API

Utilizar o framework FastAPI para construir a API

Criar endpoints que permitam operações como criação, listagem, busca, atualização e exclusão de registros de pokémons.

## Gestão de Dados

Implementar o SQLAlchemy como ORM, garantindo uma interação eficiente com o banco de dados relacional.

## Dockerização

Criar um Dockerfile funcional e utilizar um arquivo docker-compose.yml para orquestrar a aplicação e o banco de dados em containers separados.

## Testes Unitários

Desenvolver testes unitários para as principais funcionalidades da API.

## Boas Práticas de Desenvolvimento

Estruture bem o projeto, seguindo boas práticas de organização e versionamento com Git.

Documente os endpoints utilizando os recursos nativos do FastAPI.

Configure corretamente as variáveis de ambiente.






# Como utilizar a aplicação

## Link da aplicação

https://projeto-final-back-end-ebac.onrender.com/

---

# Métodos de utilização

## 1. Utilizando o Swagger do FastAPI

Acesse:

https://projeto-final-back-end-ebac.onrender.com/docs

Todas as rotas da API serão exibidas na interface do Swagger, permitindo visualizar a documentação e testar cada endpoint diretamente pelo navegador.


## 2. Utilizando Postman ou Insomnia

1. Copie a URL base da API:

   https://projeto-final-back-end-ebac.onrender.com/

2. Selecione o método HTTP adequado (GET, POST, PUT ou DELETE).

3. Utilize uma das rotas descritas abaixo.

4. Para rotas que exigem um corpo de requisição (Body), envie os dados em formato JSON.


# Rotas disponíveis

## GET /pokeapi/all

### Parâmetros opcionais

- `limit` (padrão: 10)
- `offset` (padrão: 10)

Retorna uma lista de Pokémon da API pública PokeAPI com paginação.

### Exemplo

```http
GET /pokeapi/all?limit=10&offset=0
```

## GET /pokeapi/{id}

Retorna um Pokémon específico da PokeAPI utilizando o ID informado.

### Exemplo

```http
GET /pokeapi/25
```


## POST /criar-pokemon

Permite criar um Pokémon personalizado no banco de dados da aplicação.

Os dados devem ser enviados no corpo da requisição em formato JSON.

### Exemplo

```json
{
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "types": ["electric"],
    "level": 5
}
```


## PUT /atualizar-pokemon/{nome}

Atualiza os dados de um Pokémon já cadastrado.

O nome do Pokémon deve ser informado na URL e os novos dados devem ser enviados no corpo da requisição.

### Exemplo

```http
PUT /atualizar-pokemon/pikachu
```

---

## DELETE /deletar-pokemon/{nome}

Remove um Pokémon do banco de dados utilizando seu nome.

### Exemplo

```http
DELETE /deletar-pokemon/pikachu
```

---

## GET /pokemons-criados

Retorna todos os Pokémon cadastrados pelos usuários.

---

## GET /pokemons-criados/{nome}

Retorna um Pokémon específico cadastrado pelo usuário utilizando o nome informado.

### Exemplo

```http
GET /pokemons-criados/pikachu
```

---

# Observações

- Os Pokémon retornados pelas rotas `/pokeapi/all` e `/pokeapi/{id}` são obtidos diretamente da PokeAPI, e cacheados com redis.
- Os Pokémon criados através da rota `/criar-pokemon` são armazenados em um banco de dados.
- Recomenda-se utilizar o Swagger (`/docs`) para testar a API de forma rápida e visualizar o formato esperado das requisições.


# Tecnologias Utilizadas

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Pytest
- Render
- PokeAPI
- Redis