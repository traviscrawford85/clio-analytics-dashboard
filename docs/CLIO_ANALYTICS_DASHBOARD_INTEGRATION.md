# Clio KPI Dashboard Integration Guide

**Date**: October 9, 2025  
**Domain**: portfolio.cfelab.com/clio-analytics-dashboard/  
**Status**: ✅ Ready to Deploy - Container Configured

## Configuration Setup ✅

### 1. Nginx Service Definition
The Clio Analytics Dashboard service has been added to `nginx-services.yml`:

```yaml
clio-analytics-dashboard:
  internal_port: 8501
  public_domain: portfolio.cfelab.com
  path: /clio-analytics-dashboard/
  network: cfesolutions
  purpose: "Clio Analytics Dashboard for live demos"
  preserve_path: false
  tls: true
```

**Key Settings:**
- **Port**: 8501 (typical for Streamlit applications)
- **Path**: `/clio-analytics-dashboard/` (strips prefix when forwarding to container)
- **Domain**: portfolio.cfelab.com (same domain as portfolio site)
- **TLS**: Enabled (HTTPS required)
- **preserve_path**: false (strips `/clio-analytics-dashboard/` prefix)

### 2. Demo Page Integration ✅
Updated `demo.html` to link all "Live Dashboard" buttons to `/clio-analytics-dashboard/`:

- **Hero Section**: "Open Dashboard" button
- **Right Panel**: "View Live Dashboard" button  
- **CTA Section**: "Open Live Dashboard" button

### 3. Generated Nginx Configuration
When uncommented, the generator will create:

```nginx
# Clio Analytics Dashboard for live demos
upstream clio-analytics-dashboard {
    zone clio-analytics-dashboard 64k;
    server clio-analytics-dashboard:8501 resolve;
}

# Inside portfolio.cfelab.com server block:
location /clio-analytics-dashboard/ {
    proxy_pass http://clio-analytics-dashboard/;  # strip prefix
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $connection_upgrade;
    client_max_body_size 250M;
    proxy_read_timeout 120s;
}
```

## Container Requirements ✅

### Docker Container Specifications - CONFIGURED
Your Clio KPI Dashboard container is now configured with:

1. **Container Name**: `clio-analytics-dashboard` ✅
2. **Port**: Expose port `8501` internally ✅
3. **Network**: Joined the `cfesolutions` external network ✅
4. **Bind Address**: `0.0.0.0:8501` ✅
5. **Base Path**: Serves content from root `/` ✅

### Example Docker Compose Entry
```yaml
services:
  clio-analytics-dashboard:
    build: .
    container_name: clio-analytics-dashboard
    ports:
      - "8501:8501"  # Optional: for direct access
    networks:
      - cfesolutions
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped

networks:
  cfesolutions:
    external: true
```

### Streamlit Configuration (if applicable)
If using Streamlit, create `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
baseUrlPath = ""  # Empty since nginx strips the prefix
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

## Activation Steps

### 1. Deploy Your Container
```bash
# From your Clio KPI dashboard project directory
docker compose up -d

# Verify it's running and on the correct network
docker ps | grep clio-analytics-dashboard
docker network inspect cfesolutions | grep clio-analytics-dashboard
```

### 2. Test Container Directly
```bash
# Test the container directly
curl -I http://127.0.0.1:8501/
# Should return 200 OK
```

### 3. Activate in Nginx
```bash
cd /home/oem/nginx

# Uncomment the clio-analytics-dashboard service in nginx-services.yml
# Then regenerate and restart:
/home/oem/nginx/.venv/bin/python scripts/generate_nginx_confs.py
docker compose restart nginx
```

### 4. Test the Integration
```bash
# Test the proxy route
curl -I https://portfolio.cfelab.com/clio-analytics-dashboard/
# Should return 200 OK with content from your dashboard
```

## URL Structure

### Public Access
- **Full URL**: https://portfolio.cfelab.com/clio-analytics-dashboard/
- **From Demo Page**: Click any "Live Dashboard" button
- **Direct Access**: Available via HTTPS only (HTTP redirects to HTTPS)

### Request Flow
```
User: https://portfolio.cfelab.com/clio-analytics-dashboard/
  ↓
nginx (TLS termination)
  ↓
portfolio.cfelab.com.conf location /clio-analytics-dashboard/
  ↓
proxy_pass http://clio-analytics-dashboard/ (strips prefix)
  ↓
clio-analytics-dashboard container receives: GET /
```

## Troubleshooting

### Common Issues

#### 1. "Service not found" (nginx restart fails)
**Cause**: clio-analytics-dashboard container not running  
**Fix**: Start your dashboard container first, then restart nginx

#### 2. "502 Bad Gateway"
**Cause**: Container running but not accessible  
**Fix**: Check container network and port binding
```bash
docker compose exec nginx curl -v http://clio-analytics-dashboard:8501/
```

#### 3. "404 Not Found" 
**Cause**: Dashboard app not serving content at root path  
**Fix**: Ensure your app serves content at `/` (not `/clio-analytics-dashboard/`)

#### 4. "Connection Refused"
**Cause**: App binding to 127.0.0.1 instead of 0.0.0.0  
**Fix**: Update app configuration to bind to `0.0.0.0:8501`

### Debugging Commands
```bash
# Check if container is running
docker ps | grep clio-analytics-dashboard

# Check network connectivity
docker compose exec nginx curl -v http://clio-analytics-dashboard:8501/

# Check nginx logs
docker compose logs nginx --tail=50 --follow

# Test external access
curl -k -I https://portfolio.cfelab.com/clio-analytics-dashboard/
```

## Integration Examples

### Streamlit App Integration
If your dashboard is a Streamlit app:

```python
import streamlit as st

# Configure Streamlit for proxy usage
st.set_page_config(
    page_title="Clio KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Your dashboard code here
st.title("Clio Analytics Dashboard")
st.write("Welcome to the live demo!")
```

### FastAPI Integration
If your dashboard is a FastAPI app:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Clio KPI Dashboard",
    root_path=""  # Empty since nginx strips prefix
)

@app.get("/")
async def dashboard():
    return {"message": "Clio KPI Dashboard"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)
```

## Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Nginx Service Definition | ✅ Ready | In nginx-services.yml (commented) |
| Demo Page Integration | ✅ Complete | All buttons link to /clio-analytics-dashboard/ |
| Nginx Configuration | ✅ Ready | Will generate when uncommented |
| Container Requirements | 📋 Documented | See specifications above |
| Activation Steps | 📋 Documented | Deploy container → uncomment → restart |

## Next Steps

1. **Deploy your Clio KPI Dashboard container** with the specified requirements
2. **Test the container** is accessible on port 8501
3. **Uncomment the service** in nginx-services.yml
4. **Regenerate configs** and restart nginx
5. **Test the integration** via https://portfolio.cfelab.com/clio-analytics-dashboard/

Once activated, visitors to your portfolio site can click any "Live Dashboard" button to see your Clio Analytics Dashboard in action!