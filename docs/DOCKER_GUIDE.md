# Docker Deployment Guide - Clio KPI Dashboard

## Quick Start

### Production Mode

```bash
# Build and start the dashboard
docker-compose up -d

# View logs
docker-compose logs -f dashboard

# Stop
docker-compose down
```

Access at: **http://localhost:8050**

### Development Mode (with hot reload)

```bash
# Use development compose file
docker-compose -f docker-compose.dev.yml up

# View logs (attached)
# Press Ctrl+C to stop
```

---

## Files Overview

| File | Purpose |
|------|---------|
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Production deployment configuration |
| `docker-compose.dev.yml` | Development mode (hot reload) |
| `.dockerignore` | Files to exclude from build |
| `DOCKER_GUIDE.md` | This file |

---

## Docker Setup

### 1. Build the Image

```bash
# Build the image
docker-compose build

# Or build with no cache (fresh build)
docker-compose build --no-cache

# Check image size
docker images | grep clio
```

### 2. Run the Container

#### Production Mode

```bash
# Start in detached mode
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f dashboard

# Stop
docker-compose down
```

#### Development Mode (Hot Reload)

```bash
# Start with source code mounted (hot reload)
docker-compose -f docker-compose.dev.yml up

# Code changes will automatically reload the app
```

### 3. Access the Dashboard

- **URL**: http://localhost:8050
- **Health Check**: http://localhost:8050/health

---

## Configuration

### Environment Variables

Customize in `docker-compose.yml`:

```yaml
environment:
  - DASH_PORT=8050              # Dashboard port
  - DASH_DEBUG=False            # Debug mode (True/False)
  - CLIO_SQLITE=/data/analytics/clio-analytics.db  # Database path
  - DATA_BACKEND=sqlite         # Backend type
  - PYTHONUNBUFFERED=1         # Python output buffering
```

### Volume Mounts

The dashboard expects the database at:

```yaml
volumes:
  - ../dashboard-neo4j/data/analytics:/data/analytics:ro
```

**Important**: Ensure the path `../dashboard-neo4j/data/analytics/` exists and contains `clio-analytics.db`

If your database is elsewhere, update the volume mount:

```yaml
volumes:
  - /path/to/your/data:/data/analytics:ro
```

### Port Mapping

Change the exposed port:

```yaml
ports:
  - "8080:8050"  # Access via port 8080
```

---

## Docker Commands Cheat Sheet

### Building

```bash
# Build image
docker-compose build

# Build with specific service
docker-compose build dashboard

# Build without cache
docker-compose build --no-cache

# Pull base images
docker-compose pull
```

### Running

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Start specific service
docker-compose up dashboard

# Restart services
docker-compose restart

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Monitoring

```bash
# View logs
docker-compose logs

# Follow logs
docker-compose logs -f dashboard

# View container status
docker-compose ps

# View resource usage
docker stats clio-kpi-dashboard

# Execute commands in container
docker-compose exec dashboard bash

# Run one-off command
docker-compose run dashboard python --version
```

### Debugging

```bash
# Access container shell
docker-compose exec dashboard /bin/bash

# View container details
docker inspect clio-kpi-dashboard

# Check health status
docker-compose exec dashboard curl http://localhost:8050/health

# View environment variables
docker-compose exec dashboard env

# Check database connection
docker-compose exec dashboard ls -la /data/analytics/
```

---

## Troubleshooting

### Issue: Container won't start

**Check logs**:
```bash
docker-compose logs dashboard
```

**Common causes**:
- Database path incorrect
- Port 8050 already in use
- Insufficient permissions on volume mount

**Solutions**:
```bash
# Check if port is in use
lsof -i :8050

# Verify database exists
ls -la ../dashboard-neo4j/data/analytics/clio-analytics.db

# Check container status
docker-compose ps
```

---

### Issue: Database not found

**Error**: `No such file or directory: clio-analytics.db`

**Solutions**:

1. **Verify database path**:
```bash
# Check if database exists
ls -la ../dashboard-neo4j/data/analytics/clio-analytics.db

# Update volume mount in docker-compose.yml if needed
volumes:
  - /correct/path/to/data:/data/analytics:ro
```

2. **Check file permissions**:
```bash
# Make sure database is readable
chmod 644 ../dashboard-neo4j/data/analytics/clio-analytics.db
```

3. **Verify mount inside container**:
```bash
docker-compose exec dashboard ls -la /data/analytics/
```

---

### Issue: ClioCore not available

**Warning**: `Warning: ClioCore not available`

**This is expected** if ClioCore domain services aren't in the Docker image. The dashboard will use mock data.

**Solutions**:

**Option 1**: Accept mock data (dashboard still works)

**Option 2**: Copy ClioCore into Docker image

Update `Dockerfile`:
```dockerfile
# Copy ClioCore domain services
COPY ../dashboard-neo4j/services/dashboard /app/cliocore
ENV PYTHONPATH="/app:/app/cliocore"
```

**Option 3**: Mount ClioCore as volume

Update `docker-compose.yml`:
```yaml
volumes:
  - ../dashboard-neo4j/services/dashboard:/app/cliocore:ro
```

---

### Issue: Port already in use

**Error**: `Bind for 0.0.0.0:8050 failed: port is already allocated`

**Solutions**:

1. **Stop conflicting service**:
```bash
# Find process using port
lsof -i :8050
kill -9 <PID>
```

2. **Use different port**:

Edit `docker-compose.yml`:
```yaml
ports:
  - "8051:8050"  # Use port 8051 instead
```

Access at: http://localhost:8051

---

### Issue: Changes not reflecting (development mode)

**Solutions**:

1. **Ensure development mode**:
```bash
docker-compose -f docker-compose.dev.yml up
```

2. **Verify volume mounts**:
```bash
docker-compose exec dashboard ls -la /app/dash_clio_dashboard/
```

3. **Restart container**:
```bash
docker-compose restart dashboard
```

---

## Production Deployment

### With Nginx Reverse Proxy

Uncomment the nginx service in `docker-compose.yml`:

```yaml
nginx:
  image: nginx:alpine
  container_name: clio-nginx
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl:ro
  depends_on:
    - dashboard
  networks:
    - clio-network
  restart: unless-stopped
```

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream dashboard {
        server dashboard:8050;
    }

    server {
        listen 80;
        server_name dashboard.yourdomain.com;

        location / {
            proxy_pass http://dashboard;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### SSL/HTTPS Setup

1. **Get SSL certificates** (Let's Encrypt):
```bash
certbot certonly --standalone -d dashboard.yourdomain.com
```

2. **Update nginx.conf**:
```nginx
server {
    listen 443 ssl http2;
    server_name dashboard.yourdomain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    location / {
        proxy_pass http://dashboard;
        # ... proxy headers ...
    }
}

server {
    listen 80;
    server_name dashboard.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

3. **Start services**:
```bash
docker-compose up -d
```

Access at: https://dashboard.yourdomain.com

---

## Resource Management

### Limit Container Resources

Already configured in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Monitor Resource Usage

```bash
# Real-time stats
docker stats clio-kpi-dashboard

# Check memory usage
docker-compose exec dashboard ps aux

# Check disk usage
docker system df
```

---

## Backup & Maintenance

### Backup Database

```bash
# Copy database from host
cp ../dashboard-neo4j/data/analytics/clio-analytics.db \
   ./backups/clio-analytics-$(date +%Y%m%d).db
```

### Update Dashboard

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verify
docker-compose logs -f dashboard
```

### Clean Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything (careful!)
docker system prune -a
```

---

## Testing the Deployment

### 1. Health Check

```bash
# From host
curl http://localhost:8050/health

# From container
docker-compose exec dashboard curl http://localhost:8050/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "cliocore_available": true
}
```

### 2. Access Dashboard

Open browser: http://localhost:8050

**Check**:
- [ ] Dashboard loads without errors
- [ ] All 4 tabs visible (Overview, Lifecycle, Department, Bottlenecks)
- [ ] KPI cards display values
- [ ] Charts render correctly
- [ ] No errors in browser console

### 3. Database Connection

```bash
# Check database mount
docker-compose exec dashboard ls -la /data/analytics/

# Check database content
docker-compose exec dashboard sqlite3 /data/analytics/clio-analytics.db "SELECT COUNT(*) FROM Matters;"
```

---

## Performance Tuning

### 1. Increase Workers (for higher traffic)

Update `Dockerfile`:
```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8050", "dash_clio_dashboard.app:server"]
```

Install gunicorn:
```bash
# Add to requirements.txt
echo "gunicorn>=21.2.0" >> requirements.txt
```

### 2. Enable Caching

Add Redis:

```yaml
services:
  redis:
    image: redis:alpine
    container_name: clio-redis
    networks:
      - clio-network
    restart: unless-stopped
```

Update app to use Redis cache (future enhancement).

### 3. Database Optimization

For large databases, consider migrating to PostgreSQL:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    container_name: clio-postgres
    environment:
      - POSTGRES_DB=clio
      - POSTGRES_USER=clio
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - clio-network
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## Security Best Practices

1. **Use read-only volumes**:
```yaml
volumes:
  - ../dashboard-neo4j/data/analytics:/data/analytics:ro  # ← :ro = read-only
```

2. **Run as non-root user**:

Add to `Dockerfile`:
```dockerfile
RUN useradd -m -u 1000 dashuser
USER dashuser
```

3. **Use secrets for sensitive data**:
```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  dashboard:
    secrets:
      - db_password
```

4. **Enable firewall**:
```bash
# Only allow localhost
sudo ufw allow from 127.0.0.1 to any port 8050
```

5. **Use HTTPS in production** (see SSL setup above)

---

## Summary

### Quick Commands

```bash
# Production
docker-compose up -d              # Start
docker-compose logs -f dashboard  # View logs
docker-compose down               # Stop

# Development
docker-compose -f docker-compose.dev.yml up

# Rebuild
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

### Access Points

- **Dashboard**: http://localhost:8050
- **Health Check**: http://localhost:8050/health

### Support

For issues, check:
1. Container logs: `docker-compose logs dashboard`
2. Database mount: `docker-compose exec dashboard ls -la /data/analytics/`
3. Health endpoint: `curl http://localhost:8050/health`

---

**You're all set!** 🚀

The dashboard is now containerized and ready to deploy anywhere Docker runs.
