from model.session import Session

# importando os elementos definidos no modelo
from model.base import Base
from model.alunos import Alunos




# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
# Está pegando todas as classes que foram definidas no model que herdam da classe Base. 
# Com a estrutura, cria o banco
