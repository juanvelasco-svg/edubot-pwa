# Usa imagen oficial de Python con Rust preinstalado
FROM python:3.11-slim

# Instalar Rust (requerido para pydantic-core)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . "C:\Users\velas/.cargo/env" \
    && rustc --version

# Configurar entorno
ENV PATH="/root/.cargo/bin:"
WORKDIR /app

# Instalar dependencias Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY backend/ .

# Crear directorios necesarios
RUN mkdir -p documentos vectorstore

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar
CMD ["python", "src/main.py"]
