# Gunakan base image Python 3.12
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install dependensi sistem untuk membangun paket Python (terutama aiohttp)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy semua file ke dalam container
COPY . /app

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Set environment agar log tidak di-buffer
ENV PYTHONUNBUFFERED=1

# Jalankan bot
CMD ["python", "-m", "bot.main"]
