# Gunakan image Python yang lengkap (bukan slim)
FROM python:3.12-bookworm

# Set working directory di dalam container
WORKDIR /app

# Install dependency untuk build package Python seperti aiohttp
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy semua file proyek ke dalam container
COPY . /app

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Expose port default (untuk bot yang juga punya webhook)
EXPOSE 8080

# Jalankan bot utama
CMD ["python", "bot/main.py"]
