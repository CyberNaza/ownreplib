# Base image
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for mysqlclient and poppler-utils
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libmariadb3 \
    poppler-utils \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN apt update && apt install nano -y


# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Start app with Gunicorn
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]
