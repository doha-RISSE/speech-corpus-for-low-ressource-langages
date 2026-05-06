FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libfst-dev \
    libfst-tools \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir pynini flask

# Exposer le port
EXPOSE 5000

# Lancer l'API au lieu de pipeline.py
CMD ["python", "api.py"]