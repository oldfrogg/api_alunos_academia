from pydantic import BaseModel, Field
from typing import Optional, List
from model.alunos import Alunos
from datetime import datetime


class AlunosSchema(BaseModel):
    """ Define como um novo aluno será representado
    """
    cpf: int = Field(default=12345678900)
    nome: str = Field(default="Neil Peart")
    nivel: str = Field(enum=['iniciante', 'intermediario', 'avancado'], default="intermediario")
    telefone: Optional[str] = Field(default="79 999999999")



class AlunosBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no cpf do aluno.
    """
    cpf: int = Field(default=12345678900)



class ListagemAlunosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    alunos:List[AlunosSchema]


class AlunosViewSchema(BaseModel):
    """ Define como um aluno será retornado
    """
    matricula: int = Field(default=000000)
    cpf: int = Field(default=12345678900)
    nome: str = Field(default="Jhonatta Tavares")
    nivel: str = Field(default="Intermediário")
    telefone: Optional[str] = Field(default="79 999998888")
    validade: datetime = Field(default=datetime.now())



class AlunosDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    nivel:str
    cpf: int


class AlunosContrataPlanoSchema(BaseModel):
    """ Define a estrutura a ser informada para a contratacao de plano mensal
    """
    cpf: int = Field(default=12345678900)
    qtd_meses: int = Field(default=3)


class MontaTreinoSchema(BaseModel):
    """ Define a estrutura para requisição de um treino
    """
    cpf: str = Field(default="12345678900")
    grupo: str = Field(enum=['peito', 'costas', 'biceps', 'triceps', 'trapezio', 'ombro', 'perna'], default="peito")    


class AddTreinoSchema(BaseModel):
    """ Define a estrutura para requisitar que a API de treinos adicione um exercicio em seu BD
    """ 
    grupo: str = Field(enum=['peito', 'costas', 'biceps', 'triceps', 'trapezio', 'ombro', 'perna'], default="peito")
    exercicio: str = Field(default="Supino Reto")


class DeletaTreinoSchema(BaseModel):
    """ Deleta um treino da base a partir do seu ID
    """
    id: str = Field(default=60)


class ConsultaAcademiasSchema(BaseModel):
    """ Define a estrutura para buscar uma academia na UF do aluno
    """ 
    cep: str = Field(default="49010450")


def apresenta_alunos(alunos: List[Alunos]):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunosViewSchema.
    """
    result = []
    for aluno in alunos:
        result.append({
            "matricula": aluno.matricula,
            "cpf": aluno.cpf,
            "nome": aluno.nome,
            "nivel": aluno.nivel,
            "telefone": aluno.telefone,
            "validade": aluno.validade
        })

    return {"alunos": result}




def apresenta_aluno(aluno: Alunos):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunosViewSchema.
    """
    return {
            "matricula": aluno.matricula,
            "cpf": aluno.cpf,
            "nome": aluno.nome,
            "nivel": aluno.nivel,
            "telefone": aluno.telefone,
            "validade": aluno.validade
        }

