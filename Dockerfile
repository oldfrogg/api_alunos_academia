# Define a imagem base
FROM python:3.9

# Define o diretorio de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos para o diretorio de trabalho
COPY requirements.txt .

# Instala as dependencias do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o codigo-fonte para o diretorio de trabalho
COPY . .

# Expoe a porta que a aplicacao Flask esta rodando
EXPOSE 5000

# Define o comando de execução da API
CMD ["flask", "run", "--host=0.0.0.0", "--port", "5000"]



# Apos isso, na linha de comando: 
# docker build -t alunos-api .
# docker run --network bridge --name alunos-container -d -p 5000:5000 alunos-api