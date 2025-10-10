FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY dash_clio_dashboard/ ./dash_clio_dashboard/
COPY src/ ./src/

# Create volume mount point for database
RUN mkdir -p /data/analytics

# Expose port
EXPOSE 8050

# Set environment variables
ENV DASH_PORT=8050
ENV DASH_DEBUG=False
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8050/health || exit 1

# Run dashboard
CMD ["python", "dash_clio_dashboard/app.py"]
