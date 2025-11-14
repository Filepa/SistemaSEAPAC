# Sistema SEAPAC

Sistema SEAPAC é uma aplicação web desenvolvida com o framework Django, voltada para o monitoramento dos processos de transição agroecológica de pequenos agricultores do Alto Oeste Potiguar.
O projeto integra o Trabalho de Conclusão de Curso (TCC) dos alunos Felipe Raposo e Ana Maria Rafael Dias da Silva, do curso Técnico Integrado em Informática do Instituto Federal do Rio Grande do Norte (IFRN) - Campus Pau dos Ferros.

## Sobre o Sistema

O Sistema SEAPAC surgiu a partir de uma parceria com o Serviço de Apoio a Projetos Comunitários (SEAPAC), organização civil sem fins lucrativos que atua em projetos de convivência com o Semiárido e promoção da agroecologia.

A ferramenta tem como objetivo facilitar o gerenciamento de informações das famílias assistidas pela instituição, oferecendo visões gráficas e dinâmicas sobre os processos produtivos e os estágios de transição agroecológica de cada agricultor.

## Recursos Utilizados

* Django 4.2.2
* Python 3.x
* SQLite
* HTML/CSS/Bootstrap
* Django Mermaid
* Panzoom
* Calendar

## Funcionalidades

* CRUD completo para
    * Famílias 
    * Subsistemas
    * Projetos
    * Técnicos
    * Visitas
    * Eventos (timeline)
    * Fluxo
* Visualização dinâmica dos sistemas produtivos familiares através de fluxogramas interativos (via Django Mermaid).
* Linha do tempo das atividades e visitas.
* Painel de administração customizado com níveis de acesso (técnico e administrador).
* Design responsivo e intuitivo, com foco na simplicidade e na acessibilidade.



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

6. **Carregue os dados iniciais de muncípios e subsistemas**

```bash
python manage.py loaddata dados_iniciais.json
```

7. **Inicie o servidor**

```bash
python manage.py runserver
```

Agora, o sistema estará disponível em `http://localhost:8000`.