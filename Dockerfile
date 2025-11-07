# Usa uma imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para dentro do container
COPY . .

# Expõe a porta da API Flask
EXPOSE 8000

# Comando de inicialização (executa init, migrate, upgrade e depois inicia o app)
CMD ["bash", "-c", "flask db init || true && flask db migrate -m 'create products table' || true && flask db upgrade && python run.py"]
