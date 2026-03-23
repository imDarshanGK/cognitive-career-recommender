FROM python:3.11-slim
# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libopenblas-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, wheel, setuptools to latest
RUN pip install --upgrade pip wheel setuptools

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create instance directory for databases
RUN mkdir -p /app/backend/instance

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD sh -c "python -c \"import os, urllib.request; urllib.request.urlopen('http://localhost:%s/' % os.getenv('PORT', '5000')).read()\""

# Run the application with conservative worker settings for smaller memory environments
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 --threads 2 --worker-class gthread --timeout 120 --graceful-timeout 30 --keep-alive 5 backend.app:app"]
