# Usar uma imagem base do Python
FROM python:3.10-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de dependências (requirements.txt) para o container
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto para o container
COPY . .

# Expor a porta da aplicação (por padrão 8000)
EXPOSE 8000

# Comando para rodar o servidor FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
