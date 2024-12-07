# Dockerfile (backend)
FROM python:3.11-slim

WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Instale as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do backend
COPY . .

# Comando de entrada do container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:application"]