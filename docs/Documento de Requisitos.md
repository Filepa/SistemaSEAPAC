**Documento de Requisitos**

**1 Introdução**

**1.1 Propósito do documento**

Este documento propõe a especificação dos requisitos do \<*Sistema SEAPAC*, um sistema de monitoramento de transição agroecológica de pequenos agricultores, que será utilizado nos escritórios da SEAPAC\>

**1.2 Escopo do produto**

O sistema tem como objetivo auxiliar, de forma online, o monitoramento e registro de informações sobre pequenos agricultores que estão passando pelo processo de transição agroecológica.

**1.3 Visão geral do documento**

Este documento apresenta uma visão geral do sistema, descrevendo suas funcionalidades e delimitações de requisitos, seja pelo contexto no qual será aplicado ou por questões de segurança.

**2 Descrição Geral**

O sistema auxilia no monitoramento da transição agroecológica, no qual somente técnicos e administradores da SEAPAC poderão controlar informações importantes do sistema e terão acesso a diagnósticos e análises aprofundadas sobre os agricultores cadastrados.

**2.1 Perspectiva do Produto**

O sistema opera com uma máquina-servidor que gerencia o banco de dados e controla o acesso a informações, as quais podem ser consultadas, modificadas ou excluídas, de acordo com o grau de permissão do usuário logado. 

**2.2 Restrições Gerais**

Para acessar o sistema, cada técnico terá que fazer seu cadastro no sistema com um administrador da SEAPAC. O somente o administrador terá acesso às funcionalidades de gerenciamento de cadastro dos técnicos e dos dados dos agricultores. Tanto técnicos quanto administradores poderão visualizar informações das visitas de monitoramento e, além disso, terão acesso a relatórios sobre o estado de transição em que os agricultores cadastrados se encontram, o nível de participação desses indivíduos nas atividades promovidas pela própria SEAPAC, as tecnologias que usam no(a) cultivo/criação de animais e, por fim, sobre as atividades produtivas que estão sendo realizadas e o destino final delas.

**3 Requisitos**

**3.1 Requisitos Funcionais**

| RF001 | Administrador deve poder realizar o cadastro e a manutenção de dados sensíveis dos técnicos |
| :---- | ----- |
| **Detalhes** | Dados dos técnicos: nome, CPF, data de nascimento, endereço, cargo. |
| **Restrições** | \- |
| **Responsável** | Administrador |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF002 | Administradores e técnicos devem poder realizar o cadastro, manutenção e a modificação de dados da Unidade Produtiva Familiar de cada agricultor inserido no sistema |
| :---- | ----- |
| **Detalhes** | Dados da UPF: informações sobre a terra (localização, se é própria ou não, tamanho…), cultivos realizados (tipo, quantidade, destino…), tecnologias utilizadas (quais são, se são fornecidas pela SEAPAC, para quê servem…), criações realizadas (tipo, destino, produtos gerados…) e sobre a relação entre os sistemas produtivos existentes. |
| **Restrições** | \- |
| **Responsável** | Administrador e técnico |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF003 | Administradores e técnicos devem poder acessar os dados dos agricultores cadastrados e de suas respectivas UPFs |
| :---- | ----- |
| **Detalhes** | Os dados variam entre dados pessoais e dados sobre a terra, cultivo, tecnologias e práticas agroecológicas. |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF004 | Administrador deve cadastrar, editar e visualizar projetos desenvolvidos pela SEAPAC |
| :---- | ----- |
| **Detalhes** | Incluirá a manipulação de dados como: nome do projeto, período de execução, agricultores contemplados, técnicos envolvidos, locais de aplicação e investimento realizado. |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF005 | Administradores e técnicos devem poder marcar as visitas a serem feitas |
| :---- | ----- |
| **Detalhes** | A solicitação deve, obrigatoriamente, conter dados do responsável pela visita (nome, cargo) e do agricultor (nome, CPF e UPF). |
| **Importância** | \[  \] Obrigatório **\[ X \] Importante**  \[  \] Desejável |

	

| RF006 | Administrador deve poder consultar as visitas realizadas e os técnicos envolvidos em cada uma delas |
| :---- | ----- |
| **Detalhes** | Pesquisa deve escolher o período (o mês, ano, semana e dia), técnico envolvido (nome) e agricultores (nome).   |
| **Importância** | \[  \] Obrigatório **\[ X \] Importante**  \[  \] Desejável |

| RF007 | Administradores e técnicos devem poder gerar e visualizar relatórios sobre as visitas realizadas  |
| :---- | ----- |
| **Detalhes** | Dados do relatório: identificador do agricultor, identificador do técnico, informações da família visitada (membros, idade, nível de escolaridade e afins), atividades realizadas na UPF, cuidados feitos nas produções, destino do que é produzido e observações.  |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF008 | Administradores e técnicos devem poder gerar, visualizar e editar um mapeamento/fluxo visual das informações dos sistemas produtivos de um determinado agricultor |
| :---- | ----- |
| **Detalhes** | O fluxo irá reunir, de forma acessível e clara, informações de um determinado agricultor e dos sistemas produtivos que ele possui em sua UPF, incluindo todo o fluxo de entrada e saída de produtos e as ligações entre os sistemas produtivos. O fluxo visual será essencialmente formado a partir de informações já cadastradas sobre os agricultores, mas não irá impossibilitar que técnicos e administradores adicionem novas informações. |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF009 | Administradores e técnicos devem poder gerar e visualizar relatórios sobre o fluxo de determinado agricultor |
| :---- | ----- |
| **Detalhes** | O relatório irá mostrar o nível de transição agroecológica e analisar as conexões entre: os sistemas produtivos do agricultor e como estes são utilizados e obtidos; produtos que entram e saem da UPF e sua relação com os sistemas existentes;  |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF010 | Administrador e técnicos devem ter acesso a uma linha do tempo dos agricultores |
| :---- | ----- |
| **Detalhes** | A linha irá organizar os relatórios, datas de cadastro, registros de participação dos agricultores nas atividades da SEAPAC e dados das visitas realizadas ao longo do tempo. Através dele também será possível monitorar o nível de transição dos agricultores. |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

| RF011 | Administrador e técnicos devem ter acesso a um relatório da linha do tempo dos agricultores |
| :---- | ----- |
| **Detalhes** | O relatório irá mostrar a evolução do agricultor no processo de transição agroecológica ao longo do tempo, a análise dessa evolução e as mudanças ocorridas no sistema produtivo de cada família agricultora.Ex: Se no ano Y agricultor X usava agrotóxicos, agora ele usa biofertilizantes. |
| **Importância** | **\[ X \] Obrigatório** \[  \] Importante  \[  \] Desejável |

**3.1 Requisitos não Funcionais**

| RNF001 | Serviço deve resumir e mostrar, visualmente, um breve resumo da quantidade de projetos realizados, dos técnicos cadastrados, das famílias atendidas e cidades alcançadas |
| :---- | :---- |
| **Detalhes** | Praticidade e melhor meio de demonstrar os resultados e capacidades da SEAPAC.   |

	

| RNF002 | O administrador deve poder deixar uma notificação para os técnicos marcarem as próximas visitas |
| :---- | :---- |
| **Detalhes** | Tais notificações devem ser mostradas de forma assíncrona. |

	

| RNF003 | Deve ser feito o backup do banco de dados a cada 7 dias |
| :---- | :---- |
| **Detalhes** | Os backup serão feitos de forma automática em um dia específico. |

	

| RNF004 | Identificação de acesso deve ser feito via login |
| :---- | :---- |
| **Detalhes** | Os tipos de identificações são referentes a administradores e técnicos. |

			

| RNF005 | Serviço deve estar disponível 24 horas por dia |
| :---- | :---- |
| **Detalhes** | Disponibilidade |

	

| RNF006 | Somente administradores podem ver os dados pessoais dos técnicos e de outros administradores |
| :---- | :---- |
| **Detalhes** | Privacidade |

