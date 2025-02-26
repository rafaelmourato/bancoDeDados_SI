# bancoDeDados_SI
Github referente ao projeto de Banco de Dados da cadeira de SI
# Projeto de API RESTful com MySQL e Node.js

Este projeto consiste em uma API RESTful desenvolvida com Node.js e Express.js para gerenciar informações sobre funcionários, clientes e softwares. O banco de dados é gerenciado pelo MySQL.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
  - [Instalando o MySQL](#instalando-o-mysql)
  - [Instalando o MySQL Workbench](#instalando-o-mysql-workbench)
  - [Instalando Node.js e Express](#instalando-nodejs-e-express)
- [Configurando o Banco de Dados](#configurando-o-banco-de-dados)
- [Executando o Servidor](#executando-o-servidor)
- [Dicas Finais](#dicas-finais)

## Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

- Node.js
- MySQL
- MySQL Workbench

## Instalação

### Instalando o MySQL

1. Acesse o site oficial do MySQL: [MySQL Community Downloads](https://dev.mysql.com/downloads/mysql/).
2. Escolha a versão adequada para o seu sistema operacional (Windows, macOS ou Linux) e clique em "Download".
3. Siga as instruções do assistente de instalação.

#### Para Windows:

- Execute o instalador e escolha "Developer Default" durante a instalação. 
- Siga as instruções do assistente e configure uma senha para o usuário `root`.

#### Para macOS:

1. Instale o Homebrew, se ainda não o tiver:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Instale o MySQL:
brew install mysql

3. Inicie o serviço do MySQL:
brew services start mysql

4. Configure uma senha para o usuário root:
mysql_secure_installation

### Instalando o MySQL Workbench

1. Acesse o site de downloads do MySQL e clique na aba **"MySQL Workbench"**.
2. Baixe o instalador correspondente ao seu sistema operacional e siga as instruções do assistente de instalação.

### Instalando Node.js e Express

#### Instalando o Node.js

1. Acesse o site oficial do Node.js: [Node.js Downloads](https://nodejs.org/).
2. Baixe a versão recomendada para o seu sistema operacional e siga as instruções do instalador.

#### Inicializando um projeto Node.js

1. Crie uma nova pasta para o seu projeto e navegue até ela no terminal:
   ```bash
   mkdir nome-do-projeto
   cd nome-do-projeto

2. Inicialize um novo projeto Node.js:
npm init -y

### Instalando as dependências

Instale as bibliotecas necessárias (express e mysql2) usando o seguinte comando:
npm install express mysql2 dotenv

### Configurando o Banco de Dados

1. Abra o MySQL Workbench e conecte-se ao seu servidor MySQL usando o usuário root e a senha que você definiu.

2. Crie um novo banco de dados executando o conteúdo do arquivo **Text** no MySQL Workbench.

3. No arquivo `.env`, defina as seguintes variáveis de ambiente:
   ```plaintext
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=sua_senha
   DB_NAME=nome_do_banco_de_dados
   DB_PORT=3306
   PORT=3000

4. Execute o servidor rodando o arquivo com o seguinte comando:
   ```bash
   node server.js

