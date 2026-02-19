FROM python:3.11-slim
# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libatlas-base-dev \
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
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').read()"

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "backend.app:app"]
