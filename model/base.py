# TUDO QUE É RELATIVO AO MODELO DE DADOS E REGRAS DE ACESSO AO BANCO DEVE ESTAR NO DIR MODEL
# AQUI DEVE ESTAR TODA A LOGICA PARA CRIAR E ACESSAR O BANCO DE DADOS

from sqlalchemy.ext.declarative import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()