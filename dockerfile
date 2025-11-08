# Dockerfile
FROM python:3.12-bookworm

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable PORT if needed (Leapcell default port)
ENV PORT=8080

# Jalankan bot menggunakan script utama Anda, ganti main.py dengan file Anda
CMD ["python", "main.py"]
