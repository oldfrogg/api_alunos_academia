from sqlalchemy import Column, String, Integer, DateTime, Float, create_engine, func

from datetime import datetime

from typing import Union

from model import Base 


from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class Alunos(Base):
    #defino que o objeto Aluno terá um mapeamento direto com um item salvo na tabela aluno
    __tablename__ = 'alunos'

    #no BD a matricula será a coluna 'pk_aluno'. No Python, será 'matricula'.
    matricula = Column("pk_aluno", Integer, primary_key=True)
    cpf = Column(Integer, unique=True, nullable=False)
    nome = Column(String(60), nullable=False)
    nivel = Column(String(16), default='intermediario')
    telefone = Column(String(20))
    validade = Column(DateTime, default=datetime.now().replace(hour=23,minute=59, second=59))


    def __init__ (self, cpf:int, nome:str, nivel:str, telefone:str):
        """
        Cria um aluno
        Arguments:
            Matrícula: Chave que diferencia cada aluno
            CPF: CPF do aluno 
            Nome: Nome completo do aluno 
            Nível: Nível de treinamento do aluno
            Telefone: Telefone do aluno 
            Validade: Até qual data o plano do aluno vigora
        """

        self.cpf = cpf 
        self.nome = nome
        if nivel == "iniciante" or "intermediario" or "avancado":
            self.nivel = nivel
        else:
            self.nivel = "intermediario"
        self.telefone = telefone 
        self.validade = datetime.now().replace(hour=23,minute=59, second=59)