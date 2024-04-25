# ARQUIVO CONTROLADOR. BASE DA APLICACAO

from flask import Flask, redirect, request, make_response, jsonify
from flask_openapi3 import OpenAPI, Info, Tag
from flask_restx import Api, Resource, fields

import requests
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError, NoResultFound

from pydantic import ValidationError

from model import Session, Alunos
from schemas import *
from flask_cors import CORS

from datetime import datetime, timedelta

import json


info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)



# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
aluno_tag = Tag(name="Aluno", description="Adição, visualização e remoção de alunos à base")
treinos_tag = Tag(name="Treinos", description="Elaborar treino, visualizar, adicionar e excluir exercícios da API secundária")
academias_tag = Tag(name="Academias", description="Informações sobre as academias da rede")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/add_aluno', tags=[aluno_tag], responses={"201": AlunosViewSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def add_aluno(form: AlunosSchema): # O uso de form faz os parâmetros serem passados pelo corpo da requisicao, se eu usasse query seria por URL
    """Adiciona um novo Aluno à base de dados.

    Retorna a lista de alunos
    """
    aluno = Alunos(
        cpf=form.cpf,
        nome=form.nome,
        nivel=form.nivel,
        telefone=form.telefone
    )

    try: # Nao eh necessario, mas uso para tratar excecoes que possam vir a acontecer
        # Conecta-se com o BD
        session = Session()
        # Adiciona o aluno a lista
        session.add(aluno)
        # Commita
        session.commit()
        
        return apresenta_aluno(aluno), 201

    except IntegrityError as e:
        # Duplicidade
        error_msg = "CPF ja cadsatrado"
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Ocorreu um erro e nao foi possivel concluir a solicitacao"
        return {"message": f"Aconteceu um erro. {e}"}, 400

    finally:
        session.close()
        
        
@app.get('/get_alunos', tags=[aluno_tag],
         responses={"200": ListagemAlunosSchema, "400": ErrorSchema, "404": ErrorSchema})
def get_alunos():
    """Faz a busca por todos os Alunos cadastrados

    Retorna uma representação da listagem de alunos.
    """
    try:
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        alunos = session.query(Alunos).all() # SELECT * FROM Alunos 

        if not alunos:
            return "Nao ha alunos cadastrados", 404
        else:
           # retorna a representação de aluno
            return apresenta_alunos(alunos), 200
    
    except Exception as e:
        return {"message": f"Aconteceu um erro. {e}"}, 400
    
    finally:
        session.close()
        

@app.get('/get_aluno', tags=[aluno_tag], responses={"200": AlunosViewSchema, "400": ErrorSchema, "404": ErrorSchema})
def get_aluno(query:AlunosBuscaSchema): # Uso query pois nao posso passar parametros pelo corpo com um GET
    """Procura um aluno a partir do seu CPF

    Retorna o aluno buscado.
    """
    aluno_cpf = query.cpf

    try:
        session = Session()
        aluno = session.query(Alunos).filter(Alunos.cpf == aluno_cpf).one()
        # SELECT * FROM Alunos WHERE cpf_digitado == cpf__aluno__d-base passando um resultado
        # Caso ao invés do first() fosse um all(), teria uma lista de resultados
        # Se eu quiser ver a query:
        # print (session.query(Alunos).filter(Aluno.cpf == aluno_cpf)

        # Se não achar nenhum
        return apresenta_aluno(aluno), 200
        
    except NoResultFound as e:
        error_msg = "Nao ha aluno cadastrado com o CPF informado"
        return {"message": error_msg}, 404
    
    except MultipleResultsFound:
        error_msg = "Mais de um aluno com o CPF informado"
        return {"message": error_msg}, 404
    
    except Exception as e:
        return {"message": f"Aconteceu um erro. {e}"}, 400
    
    finally:
        session.close()


@app.delete('/del_aluno', tags=[aluno_tag], responses={"200": AlunosDelSchema, "400": ErrorSchema, "404": ErrorSchema})
def del_aluno (query: AlunosBuscaSchema):
    """Deleta um Aluno a partir do CPF informado.

    Retorna a confirmação da remoção
    """ 
    aluno_cpf = query.cpf
    
    try:
        session = Session()
        aluno = session.query(Alunos).filter(Alunos.cpf == aluno_cpf).first()
        count = session.query(Alunos).filter(Alunos.cpf == aluno_cpf).delete()
        session.commit()

        if count:
            return {"message": "Aluno removido da base", "nome": aluno.nome, "cpf": aluno_cpf}


        else: 
            # Para aluno não encontrado:
            error_msg = "Aluno não encontrado na base :/"
            return {"message": error_msg}, 404
        
    except Exception as e:
        return {"message": f"Aconteceu um erro. {e}"}, 400
    
    finally:
        session.close()


@app.put('/update_aluno', tags=[aluno_tag], responses={"200": AlunosViewSchema, "400": ErrorSchema, "404": ErrorSchema})
def update_aluno(form:AlunosSchema):
    """Altera os dados cadastrais de um aluno a partir do CPF.

    Retorna o aluno com os dados modificados.
    """
    aluno_cpf = form.cpf

    try:
        session = Session()
        aluno = session.query(Alunos).filter(Alunos.cpf==aluno_cpf).first()

        if not aluno:
            error_msg = "Aluno não encontrado"
            return {"message": error_msg}, 404

        else:
            aluno.cpf = form.cpf
            aluno.nome = form.nome
            aluno.nivel = form.nivel
            aluno.telefone = form.telefone
            session.commit()
            return apresenta_aluno(aluno), 200
        
    except Exception as e:
        return {"message": f"Aconteceu um erro. {e}"}, 400
    
    finally:
        session.close()


@app.put('/contrata_plano', tags=[aluno_tag], responses={"200":AlunosViewSchema, "400": ErrorSchema, "404": ErrorSchema, "422": ErrorSchema})
def contrata_plano(form:AlunosContrataPlanoSchema):
    """Adiciona a quantidade de meses contratado no plano do aluno.

    Retorna os dados do aluno com a validade do seu plano atualizada.
    """
    aluno_cpf = form.cpf
    qtd_meses = form.qtd_meses
    
    try:
        session = Session()
        aluno = session.query(Alunos).filter(Alunos.cpf==aluno_cpf).first()
        
        if not aluno:
            error_msg = "Aluno não encontrado"
            return {"message": error_msg}, 404

        else:
            if aluno.validade < datetime.now():
                aluno.validade = datetime.now()+timedelta(days=30*qtd_meses)
                session.commit()
            else:
                aluno.validade += timedelta(days=30*qtd_meses)
                session.commit()
            return apresenta_aluno(aluno), 200

    except ValidationError as e: #NAO ESTA FUNCIONANDO AINDA
        error_msg = f"Existem caracteres nao permitidos. Erro de validacao. {e}"
        return {"message": error_msg}, 422
    
    except Exception as e:
        return {"message": f"Aconteceu um erro. {e}"}, 400
    
    finally:
        session.close()



# Utiliza um outro serviço.
@app.get('/monta_treino', tags=[aluno_tag])
def monta_treino(query:MontaTreinoSchema):
    """Requisita um treino para o aluno, com base em seu nível e grupo muscular desejado.
    
    Faz a requisição com:
    - CPF do aluno
    - Grupos musculares: peito, costas, biceps, triceps, trapezio, ombros, pernas.
    """
    aluno_cpf = query.cpf
    
    try:
        session = Session()
        aluno = session.query(Alunos).filter(Alunos.cpf == aluno_cpf).first()
        
        nivel = aluno.nivel
        grupo_muscular = query.grupo
        try:
            req = requests.get(f"http://host.docker.internal:5001/meutreino/{nivel}/{grupo_muscular}")
            return jsonify(req.json()), 200

        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
            return {"message": error_msg}, 400
                
    except Exception as e:
        return {"message": f"Aconteceu um erro. {e}"}, 400
    
    finally:
        session.close()
   

# Utiliza API secundária e mostra todos os exercicios cadastrados
@app.get('/listatreinos', tags=[treinos_tag])
def lista_treinos():
    """Lista todos os treinos
    """
    try:
        req = requests.get("http://host.docker.internal:5001/treinos")
        return jsonify(req.json()), 200
      
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro na requisição: {str(e)}"
        return {"message": error_msg}, 400
    
    except Exception as e:
        return {"message": f"Aconteceu um erro: {e}"}, 400
    

@app.post('/add_treino', tags=[treinos_tag])
def add_treino(form: AddTreinoSchema):
    grupo = form.grupo
    exercicio = form.exercicio
   
    dados = {"grupo_muscular": grupo, 
            "exercicio": exercicio}
    
    try:
        req = requests.post("http://host.docker.internal:5001/add", json=dados)
        return jsonify(req.json()), 200

      
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro na requisição: {str(e)}"
        return {"message": error_msg}, 400
    
    except Exception as e:
        return {"message": f"Aconteceu um erro: {e}"}, 400
    
    
@app.delete('/deleta_treino', tags=[treinos_tag])
def deletra_treino(query: DeletaTreinoSchema):
    id = query.id
    try:
        req = requests.delete(f'http://host.docker.internal:5001/delete/treino/{id}')
        return jsonify(req.json()), 200

    except requests.exceptions.RequestException as e:
        error_msg = f"Erro na requisição: {str(e)}"
        return {"message": error_msg}, 400
    
    except Exception as e:
        error_msg = f"Erro! {e}"
        return {"message": error_msg}, 400
    
       
       


@app.get('/consulta_academias', tags=[academias_tag])
def consulta_academias(query: ConsultaAcademiasSchema):
    """Consulta academias próximas
    Faz a requisição com:
    - CEP do aluno
    """
    cep = query.cep

    try:
        req = requests.get(f"https://viacep.com.br/ws/{cep}/json")
        data = req.json()
        uf_aluno = data.get('uf').upper()
        academias_proximas = []

        with open ('database/academias.json', 'r', encoding='utf-8') as file:
            dados_academias = json.load(file)
            for academia in dados_academias['academias']:
                if (uf_aluno == academia['UF']):
                    academias_proximas.append(academia)
                
        return(jsonify(academias_proximas)), 200
    
    except FileNotFoundError:
        error_msg = "O arquivo não foi encontrado."
        return {"message": error_msg}, 500
    
    except json.JSONDecodeError:
        error_msg = "Requisição não entendida pelo servidor. Sintaxe inválida."
        return {"message": error_msg}, 400
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro na requisição: {str(e)}"
        return {"message": error_msg}, 400
    
    except Exception as e:
        return {"message": f"Aconteceu um erro: {e}"}, 400


    
app.run(host='0.0.0.0', port=5000, debug=True)