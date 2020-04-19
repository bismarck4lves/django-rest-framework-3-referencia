##Caso queira utilizar uma virtal env

	python3 -m venv venv
	source venv/bin/activate

##Carregando aplicação

	pip install -r requirements.txt


O sqlite3 já vem populado com dados para testar a aplicação. Porém, caso queira testar com outro banco, para popular, execute o comando abaixo:

	python3 manage.py migrate

O banco slqlite vem com um susperusuario ja cadastrado:

	username: admin
	password: bbb123

##ENPOITS

**GET** /medicos

**GET** /especialidades

**GET** /agendas 

**GET** - **POST** - **DELETE** /consultas

**POST** /login

**POST** /logout

**POST** /register




