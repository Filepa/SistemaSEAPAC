# Sistema SEAPAC

Sistema SEAPAC é uma aplicação django focada no monitoramento de pequenos agricultores e suas práticas para atingir a transição agroecológica. Faz parte do Trabalho de Conclusão de Curso dos alunos Felipe Raposo e Ana Maria do curso de informática do IFRN Pau dos Ferros.

## Sobre o Sistema

Este é um projeto desenvolvido para as disciplinas **Programação para Internet**, **Projeto de Desenvolvimento de Software** e **Fundamentos de Sistemas Operacionais e Sistemas Operacionais de Rede**, as quais têm como projeto final o vigente trabalho. 

## Recursos Utilizados

* Django 4.2.2
* Python 3.x
* SQLite
* HTML/CSS/Bootstrap

## Funcionalidades

* CRUD de Famílias
* CRUD de Subsistemas

## Instalação

### Pré-requisitos

Certifique-se de ter o **Python** e o **Django** instalados em seu computador com Windows.
Se ainda não tiver, instale pelo site oficial:

* [Python](https://www.python.org/downloads/)
* [Django](https://docs.djangoproject.com/en/4.2/topics/install/)

### Passos para instalação

1. **Clone o repositório**

```bash
git clone https://github.com/Filepa/SistemaSEAPAC.git
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

```bash
venv\Scripts\activate
```

4. **Instale as dependências do projeto**

```bash
pip install -r requirements.txt
```

5. **Execute as migrações**

```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Carregue os dados iniciais de famílias, usuários e subsistemas**

```bash
python manage.py loaddata dados_iniciais.json
```

7. **Inicie o servidor**

```bash
python manage.py runserver
```

Agora, o sistema estará disponível em `http://localhost:8000`.
