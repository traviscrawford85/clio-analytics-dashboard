#!/bin/bash
# scripts/deploy_to_cfe.sh
# CFE Solutions Dashboard Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CFE_NETWORK="cfesolutions"
SERVICE_NAME="clio-dashboard"
COMPOSE_FILE="docker-compose.cfe.yml"
IMAGE_NAME="cfe-solutions/dashboard"
VERSION="latest"

echo -e "${BLUE}🚀 CFE Solutions Dashboard Deployment${NC}"
echo "======================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Docker is running
check_docker() {
    if ! command_exists docker; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        exit 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to check if CFE network exists
check_cfe_network() {
    if ! docker network ls | grep -q $CFE_NETWORK; then
        echo -e "${YELLOW}⚠️  CFE Solutions network not found. Creating...${NC}"
        docker network create $CFE_NETWORK
        echo -e "${GREEN}✅ Created CFE Solutions network${NC}"
    else
        echo -e "${GREEN}✅ CFE Solutions network exists${NC}"
    fi
}

# Function to check if required services are running
check_dependencies() {
    echo -e "${BLUE}🔍 Checking CFE Solutions service dependencies...${NC}"
    
    local services=("cliocore-intelligence" "neo4j" "chromadb")
    local missing_services=()
    
    for service in "${services[@]}"; do
        if ! docker ps --format "table {{.Names}}" | grep -q $service; then
            missing_services+=($service)
        fi
    done
    
    if [ ${#missing_services[@]} -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Missing required services: ${missing_services[*]}${NC}"
        echo "Please ensure these services are running on the cfesolutions network"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo -e "${GREEN}✅ All required services are running${NC}"
    fi
}

# Function to create required secrets
create_secrets() {
    echo -e "${BLUE}🔐 Setting up secrets...${NC}"
    
    # JWT Secret
    if ! docker secret ls | grep -q "cfe_jwt_secret"; then
        echo "Creating JWT secret..."
        openssl rand -base64 32 | docker secret create cfe_jwt_secret -
        echo -e "${GREEN}✅ Created JWT secret${NC}"
    fi
    
    # Neo4j Password (if not exists)
    if ! docker secret ls | grep -q "cfe_neo4j_password"; then
        echo "Creating Neo4j password secret..."
        echo "neo4j_password_here" | docker secret create cfe_neo4j_password -
        echo -e "${YELLOW}⚠️  Please update Neo4j password secret manually${NC}"
    fi
}

# Function to create required volumes
create_volumes() {
    echo -e "${BLUE}💾 Setting up volumes...${NC}"
    
    if ! docker volume ls | grep -q "cfe-analytics-data"; then
        echo "Creating analytics data volume..."
        docker volume create cfe-analytics-data
        echo -e "${GREEN}✅ Created analytics data volume${NC}"
    else
        echo -e "${GREEN}✅ Analytics data volume exists${NC}"
    fi
}

# Function to build the dashboard image
build_image() {
    echo -e "${BLUE}🔨 Building dashboard image...${NC}"
    
    docker build \
        -f Dockerfile.cfe \
        -t ${IMAGE_NAME}:${VERSION} \
        --build-arg BUILD_ENV=production \
        .
    
    echo -e "${GREEN}✅ Built dashboard image${NC}"
}

# Function to deploy the dashboard
deploy_dashboard() {
    echo -e "${BLUE}📦 Deploying dashboard to CFE Solutions network...${NC}"
    
    # Stop existing containers
    docker-compose -f $COMPOSE_FILE down --remove-orphans
    
    # Deploy with health checks
    docker-compose -f $COMPOSE_FILE up -d
    
    echo -e "${GREEN}✅ Dashboard deployment started${NC}"
}

# Function to wait for service health
wait_for_health() {
    echo -e "${BLUE}⏳ Waiting for dashboard to be healthy...${NC}"
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8050/health >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Dashboard is healthy!${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}❌ Dashboard failed to become healthy${NC}"
    echo "Checking logs..."
    docker-compose -f $COMPOSE_FILE logs --tail=20 clio-dashboard
    return 1
}

# Function to display service status
show_status() {
    echo -e "${BLUE}📊 Service Status${NC}"
    echo "=================="
    
    docker-compose -f $COMPOSE_FILE ps
    
    echo ""
    echo -e "${BLUE}🌐 Access Information${NC}"
    echo "====================="
    echo "Dashboard URL: http://localhost:8050"
    echo "Health Check: http://localhost:8050/health"
    
    if command_exists curl; then
        echo ""
        echo -e "${BLUE}🔍 Health Check Result${NC}"
        curl -s http://localhost:8050/health | python3 -m json.tool 2>/dev/null || echo "Health check endpoint not responding"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  --dev       Deploy in development mode with hot reload"
    echo "  --logs      Show logs after deployment"
    echo "  --status    Show current service status"
    echo "  --stop      Stop the dashboard service"
    echo "  --help      Show this help message"
}

# Main deployment function
main() {
    case "$1" in
        --help)
            show_usage
            exit 0
            ;;
        --status)
            show_status
            exit 0
            ;;
        --stop)
            echo -e "${BLUE}🛑 Stopping dashboard...${NC}"
            docker-compose -f $COMPOSE_FILE down
            echo -e "${GREEN}✅ Dashboard stopped${NC}"
            exit 0
            ;;
        --dev)
            echo -e "${YELLOW}🔧 Development mode deployment${NC}"
            COMPOSE_PROFILES="dev"
            ;;
        --logs)
            echo -e "${BLUE}📋 Showing logs after deployment${NC}"
            SHOW_LOGS=true
            ;;
    esac
    
    # Pre-flight checks
    check_docker
    check_cfe_network
    check_dependencies
    
    # Setup
    create_secrets
    create_volumes
    
    # Build and deploy
    build_image
    deploy_dashboard
    
    # Health check
    if wait_for_health; then
        show_status
        
        if [ "$SHOW_LOGS" = true ]; then
            echo -e "${BLUE}📋 Recent logs:${NC}"
            docker-compose -f $COMPOSE_FILE logs --tail=50 clio-dashboard
        fi
        
        echo ""
        echo -e "${GREEN}🎉 Dashboard successfully deployed to CFE Solutions network!${NC}"
        echo -e "${BLUE}🌐 Dashboard available at: http://localhost:8050${NC}"
    else
        echo -e "${RED}❌ Deployment failed${NC}"
        exit 1
    fi
}

# Check if no arguments provided
if [ $# -eq 0 ]; then
    main
else
    main "$@"
fi