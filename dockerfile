# Gunakan image Python yang lebih lengkap
FROM python:3.12-bookworm

# Set working directory
WORKDIR /app

# Pastikan semua library build sudah tersedia
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project ke container
COPY . /app

# Install dependencies Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Pastikan log keluar langsung
ENV PYTHONUNBUFFERED=1

# Jalankan bot dengan format modul (seperti yang kamu pakai lokal)
CMD ["python", "-m", "bot.main"]
