# Gunakan base image Python versi penuh, bukan slim
FROM python:3.12-bookworm

# Set working directory
WORKDIR /app

# Install dependencies untuk build package (C compiler, header, dll)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy semua file ke container
COPY . /app

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Railway pakai 8080)
EXPOSE 8080

# Jalankan bot
CMD ["python", "main.py"]
