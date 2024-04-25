class ConsultaAcademiasSchema(BaseModel):
    """ Define a estrutura para buscar uma academia na UF do aluno
    """ 
    cep: str = Field(default="49000000")