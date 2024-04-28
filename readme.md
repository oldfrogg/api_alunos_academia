# API PUC Academia

## Objetivo
A aplicação tem como objetivo fazer o controle de cadastro dos alunos da Academia da PUC, além de montar seus treinos e encontrar as academias mais próximas.


## Descrição 
Projeto acadêmico de um MVP para a sprint "Desenvolvimento Back End Avançado" da pós graduação de "Desenvolvimento Full Stack" da PUC-RJ.

A API permite adicionar alunos, editar cadastro, remover aluno, requisitar os dados de um ou todos os alunos. Tudo isso através do acesso e manipulação de um banco de dados SQLite.

Por meio dessa API é possível também chamar outras API's, sendo uma a ser executada na porta 5001, e outra de uma fonte externa, a ViaCEP.

Um fluxograma na pasta raiz do projeto, com o nome "Fluxograma.png" exemplifica como acontece a comunicação entre API Principal x API Secundária, e API x Banco de Dados.

Importante: Esta API deve ser executada na porta 5000.



### API Secundária
A API na porta 5001, que deve estar em execução para conseguir acessá-la, é responsável por manipular um banco de dados que cuida do cadastro de exercícios para cada grupo muscular, onde é possível requisitar um treino para um grupo muscular, adicionar novos exercícios e removê-los.

### API Externa
A API externa da ViaCEP é utilizada para obter dados da localização dos alunos, para que assim sejam listadas as academias próximas.
Não há licença de uso e não é necessário cadastro para utilização dessa API.


## Rotas
A seguir lista-se todas as rotas cadastradas que podem ser utilizadas a partir da API principal.

### Rotas da API Principal
* / - GET - Página inicial - Escolha da documentação.
* /add_aluno - POST - Cadastra um novo aluno.
* /get_alunos - GET - Lista todos os alunos.
* /get_aluno - GET - Filtra um aluno através do seu CPF.
* /update_aluno - PUT - Altera os dados cadastrais (nome e telefone) de um aluno.
* /contrata_plano - PUT - Contrata um plano mensal para o aluno.
* /del_aluno - DELETE - Exclui um aluno do cadastro.


### Rotas da API principal que chamam a API Secundária
* /monta_treino - GET - Elabora um treino de um grupo muscular para um aluno.
* /lista_treinos - GET - Lista todos os treinos.
* /add_treino - POST - Adiciona um exercício à base de dados.
* /deleta_treino - DELETE - Exclui um treino do cadastro através do seu id.


### Rotas da API principal que chamam a API Externa - Via CEP
* /consulta_academias - GET - Consulta academias próximas com base no CEP.



## Execução da API Principal
Primeiro será mostrado como executar em modo de desenvolvimento, e depois como executar via Docker. Para ambos os casos o Banco de Dados, caso ainda não exista, será criado. Caso não queira começar com uma carga inicial, basta excluir o banco antes da execução, caso ele já exista.

### Execução em modo de desenvolvimento
Importante: Para poder chamar as rotas principais em modo de desenvolvimento, deve-se alterar as variáveis "req" que chamam a API secundária em "app.py", alterando a chamada à ponte Docker ("host.docker.internal") para "localhost", mantendo as rotas.

Para executar a aplicação, deve-se realizar a instalação dos pacotes necessários e executá-lo em um ambiente virtual.

Para criar um ambiente virtual é necessário navegar no terminal até o diretório da aplicação e dar o comando:
```
python -m venv venv
```

Além de criar é necessário deixá-lo ativado para a instalação das bibliotecas e execução da aplicação.

Para ativar o ambiente virtual, faça o  seguinte:
* No Windows:
```
.\venv\Scripts\activate
```

* No Linux:
```
source venv/bin/activate
```

Pronto, agora deve aparecer um "(venv)" no início da sua linha de comando no terminal. 

Isso indica que o ambiente virtual está ativo.

Caso queira desativá-lo, basta executar:
```
deactivate
```


Agora, com o ambiente virtual ativo, você deve instalar as bibliotecas necessárias na aplicação.

Para isso, execute o comando:
```
pip install -r requirements.txt
```

Com isso, a aplicação estará pronta para a execução.

O banco de dados utilizado é o SQLite, o arquivo db.sqlite3 será criado em sua máquina na primeira execução do programa.

Por fim, para executar a aplicação, basta executar o flask da seguinte forma:
```
flask run
```

Com isso a aplicação ficará ativa em um servidor local. Você poderá acessá-lo através do navegador utilizando:
<http://localhost:5000>
ou:
<http://127.0.0.1:5000/>

Você terá 3 escolhas de documentação, mas é recomendável a utilização do Swagger.

### Execução via Docker
Caso não o tenha, instale o Docker em sua máquina.

##### Para instalar o Docker no Windows
Baixar o wsl com o terminal Windows em modo de administrador
```
wsl --install
```

Siga os passos disponíveis no link a seguir:

<https://docs.docker.com/desktop/install/windows-install/>

De preferência, instalar com componentes requeridos para o WSL 2


Após instalado, o comando "ubuntu" irá transformar o cmd ou powershell em um terminal linux, mas também é possível abrir um terminal no vscode e adicionar um terminal wsl, utilizando a extensão "WSL".



##### Para instalar o Docker no Linux
Siga os passos disponíveis para a sua distribuição informados no link a seguir:

<https://docs.docker.com/desktop/install/linux-install/>


##### Para instalar o Docker no mac
Siga os passos informados no link a seguir:

<https://docs.docker.com/desktop/install/mac-install/>


Para todos os casos, o modo de virtualização precisa estar ativado na BIOS.


#### Com o Docker instalado em sua máquina

Navegue através do terminal até o diretório onde encontra-se o Dockerfile e os arquivos da aplicação e execute como administrador (Coloca 'sudo' antes do comando no Linux) o seguinte comando para construir a imagem Docker com o nome "alunos-api":
```
docker build -t alunos-api .
```

Após criada a imagem, crie e execute um container dessa imagem como admnistrador, com o nome "alunos-api":
```
docker run --network bridge --name alunos-container -d -p 5000:5000 alunos-api
```

Pronto, o container já deve estar ativo! Para verificar, basta abrir o: 
<http://localhost:5000>

Caso queira ver os container em execução execute o comando 
```
docker ps
```


Caso queira parar a execução do container, execute o comando 
```
docker stop alunos-container
```


Caso queira re-executar o container, execute o comando
```
docker start alunos-contaienr
```


Caso queira excluir o container, pare sua execução e o remova com o comando
```
docker rm alunos-container
```


Para listar as imagens construídas no Docker, execute o comando:
```
docker images
```


Caso queira excluir a imagem, execute o comando
```
docker rmi alunos-api
```