FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl build-essential git && rm -rf /var/lib/apt/lists/*

# Instalar Rust para pydantic-core
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:"

WORKDIR /app

# Copiar e instalar dependencias
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY backend/ .

# Crear directorios necesarios
RUN mkdir -p documentos vectorstore

EXPOSE 8000

CMD ["python", "src/main.py"]
