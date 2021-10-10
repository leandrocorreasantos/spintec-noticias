# spintec-noticias
API de notícias para Spintec - Exemplo de Projeto

## Instalação

### Requisitos

Para utilização do sistema em ambiente de testes/desenvolvimento, você precisará instalar o [Docker] e o [Git].

Primeiramente, faça o download do código-fonte clonando o repositório.

```bash
git clone https://github.com/leandrocorreasantos/spintec-noticias.git
```

Em seguida, entre na pasta do projeto

```bash
cd spintec-noticias
```

Dentro da pasta do projeto, você precisará inicializar o docker e baixar os containers necessários para o funcionamento da aplicação.

```bash
make build
```

Uma bez baixados os containers, utilize o comando abaixo para fazer a configuração interna do sistema, baixando os pacotes necessários, como o Flask.

```bash
make setup
```

Agora, execute a migração do banco de dados para que as tabelas sejam criadas.

```bash
make migrate-apply
```

Você precisará criar um usuário com permissão para acessar os endpoints protegidos. O comando abaixo cria um usuário que possui o username "admin" e a senha "12345678".

```bash
make seed
```

Após criar o usuário padrão, o sistema estará pronto para iniciar.

```bash
make start
```

## Endpoints

Uma vez incializado, os endpoints abaixo ficarão disponíveis no endereço [http://localhost:5000](http://localhost:5000). Apenas os endpoints de busca (GET) e o login estão liberados. Os demais estão protegidos e é necessário informar o token JWT no header para acessar. 

Faça login com o usuário padrão para receber o token JWT necessário para autenticação. Em seguida, basta informar o token no cabeçalho da requisição, utiliando o método 'Bearer Token', ou seja, o cabeçalho deve conter a seguinte declaração:

```http
Authorization: Bearer JWT
```

A sigla **JWT** representa o valor do token.


### Módulo User

Utilizado para manutenir o usuário adminstrador do sistema, possui os seguintes endpoints:

Método | Endereço | Requer Autenticação? 
--|--|--
POST | /v1/user/login | Não
GET | /v1/user | Sim 
POST | /v1/user | Sim
PUT | /v1/user/<user_id> | Sim
DELETE | /v1/user/<user_id> | Sim

O parâmetro **<user_id>** corresponde ao ID do usuário, do tipo inteiro.

Formato do JSON contendo os dados de login:

```json
{
	"username": "admin",
	"password": "12345678"
}
```
Formato do JSON contendo os dados do usuário:

```json
{
  "username": "admin",
  "password": "12345678",
  "email": "admin@localhost",
  "first_name": "Admin",
  "last_name": "Manager"
}
```

### Módulo Autor

Utilizado para gerenciar os autores das notícias

Método | Endereço | Requer Autenticação? 
--|--|--
GET | /v1/autor | Não
GET | /v1/autor/autor_id | Não
POST | /v1/autor | Sim 
PUT | /v1/autor/<autor_id> | Sim
DELETE | /v1/autor/<autor_id> | Sim 

O parâmetro **<autor_id>** corresponse ao ID do autor, to tipo inteiro.

Formato do JSON com os dados do autor:

```json
{
  "id": 1,
  "email": "autor@localhost",
  "nome": "Primeiro Autor"
}
```

Os dados acima são utilizados no cadastro ou alteração do autor. O endpoint que faz a listagem (GET /v1/autor) retorna os dados no seguinte formato:
```json
{
  "data": [
    {
      "email": "lispector@localhost",
      "id": 3,
      "nome": "Lipsum Suassuna"
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 1,
  "total_pages": 0
}
```
Os dados adicionais correspondem à paginação, enquanto i item **data** contém os itens encontrados.

### Módulo Noticia

Utilizado para gerenciar as notícias

Método | Endereço | Requer Autenticação? 
--|--|--
GET | /v1/noticia | Não
GET |  /v1/noticia/<noticia_slug> | Não
POST | /v1/noticia | Sim 
PUT | /v1/autor/<noticia_slug> | Sim
DELETE | /v1/autor/<noticia_slug> | Sim 

O parâmetro **<noticia_slug>** corresponse ao slug da notícia, do tipo string. O campo slug é obtido com base no título da notícia, onde os espaços são substituídos por um traço e os demais caracteres especiais são removidos.

Formato do JSON com os dados da notícia:

```json
{
	"titulo": "lorem ipsum",
	"texto": "lorem ipsum dolor sit amet",
	"autor_id": 3
}
```
Os dados acima são utilizados no cadastro ou alteração da notícia. Os endpoints de exibição (GET) retornam os dados no seguinte formato:

```json
{
  "autor": {
    "email": "autor@localhost",
    "id": 1,
    "nome": "Primeiro autor"
  },
  "id": 1,
  "titulo": "lorem ipsum",
  "slug": "lorem-ipsum",
  "texto": "lorem ipsum dolor sit amet"
}
```

No caso da listagem geral de notícias, os dados são retornados no seguinte formato:

```json
{
  "data": [
    {
      "autor": {
        "email": "lispector@localhost",
        "id": 3,
        "nome": "Lipsum Suassuna"
      },
      "id": 1,
      "slug": "lorem-ipsum-dolor",
      "texto": "lorem ipsum dolor sit amet",
      "titulo": "lorem ipsum dolor"
    }
  ],
  "page": 1,
  "per_page": 10,
  "total": 1,
  "total_pages": 0
}
```

Os dados adicionais correspondem à paginação, enquanto o campo **data** contém os itens encontrados.

### Paginação

Os dados da listagem de autores e notícias são paginados e seus valores correspondem à tabela abaixo:

Campo | Descrição
--|--
data | Os dados paginados
page | págian atual (1 por padrão)
per_page | Quantidade de itens por página
total | Total de itens
total_pages | Total de páginas

Os parâmetros **page** e **per_page** podem ser enviados via parâmetros GET para controlar a paginação das listagens.

### Filtros

É possível filtrar as notícias enviando parâmetros via GET (juntamente com a paginação) conforme indicado na tabela abaixo:

Campo | Descrição | Exemplo
--|--|--
titulo | Título da notícia | Lorem Ipsum 
texto | Trecho do corpo da notícia | lorem ipsum dolor
autor | Nome do autor | admin