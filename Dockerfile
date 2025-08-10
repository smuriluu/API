# Imagem base
FROM python:3.12-slim

# Define diretório de trabalho dentro do container
WORKDIR /api

# Copia arquivos para o container
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código
COPY . .

# Expõe a porta da API
EXPOSE 8081

# Comando para iniciar a API
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8081", "api:app"]
