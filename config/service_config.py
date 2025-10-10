# config/service_config.py
import os
from dataclasses import dataclass
from typing import Optional
import yaml

@dataclass
class ServiceEndpoint:
    """Service endpoint configuration"""
    host: str
    port: int
    protocol: str = "http"
    health_endpoint: str = "/health"
    
    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"
    
    @property
    def health_url(self) -> str:
        return f"{self.url}{self.health_endpoint}"

@dataclass 
class CFESolutionsConfig:
    """CFE Solutions network service configuration"""
    
    # Core services
    cliocore_grpc: ServiceEndpoint
    cliocore_rest: ServiceEndpoint
    neo4j: ServiceEndpoint
    chromadb: ServiceEndpoint
    
    # Module services
    custom_fields: ServiceEndpoint
    billables_insight: ServiceEndpoint
    
    # Dashboard configuration
    dashboard_port: int = 8050
    dashboard_debug: bool = False
    dashboard_host: str = "0.0.0.0"
    
    # Security
    auth_enabled: bool = True
    jwt_secret_path: str = "/run/secrets/jwt_secret"
    
    # Database
    sqlite_path: str = "/data/analytics/clio-analytics.db"
    data_backend: str = "hybrid"

def load_cfe_config() -> CFESolutionsConfig:
    """Load configuration from environment variables and files"""
    
    # Load from environment with defaults for CFE Solutions network
    return CFESolutionsConfig(
        cliocore_grpc=ServiceEndpoint(
            host=os.getenv("CLIOCORE_SERVICE_HOST", "cliocore-intelligence"),
            port=int(os.getenv("CLIOCORE_GRPC_PORT", "9090")),
            protocol="grpc"
        ),
        cliocore_rest=ServiceEndpoint(
            host=os.getenv("CLIOCORE_SERVICE_HOST", "cliocore-intelligence"), 
            port=int(os.getenv("CLIOCORE_REST_PORT", "8080")),
            protocol="http"
        ),
        neo4j=ServiceEndpoint(
            host=os.getenv("NEO4J_HOST", "neo4j"),
            port=int(os.getenv("NEO4J_PORT", "7687")),
            protocol="bolt"
        ),
        chromadb=ServiceEndpoint(
            host=os.getenv("CHROMADB_HOST", "chromadb"),
            port=int(os.getenv("CHROMADB_PORT", "8000")),
            protocol="http"
        ),
        custom_fields=ServiceEndpoint(
            host=os.getenv("CUSTOM_FIELDS_HOST", "custom-fields-manager"),
            port=int(os.getenv("CUSTOM_FIELDS_GRPC_PORT", "9091")),
            protocol="grpc"
        ),
        billables_insight=ServiceEndpoint(
            host=os.getenv("BILLABLES_HOST", "billables-insight"),
            port=int(os.getenv("BILLABLES_GRPC_PORT", "9092")),
            protocol="grpc"
        ),
        dashboard_port=int(os.getenv("DASH_PORT", "8050")),
        dashboard_host=os.getenv("DASH_HOST", "0.0.0.0"),
        dashboard_debug=os.getenv("DASH_DEBUG", "false").lower() == "true",
        auth_enabled=os.getenv("AUTH_ENABLED", "true").lower() == "true",
        jwt_secret_path=os.getenv("JWT_SECRET_FILE", "/run/secrets/jwt_secret"),
        sqlite_path=os.getenv("CLIO_SQLITE", "/data/analytics/clio-analytics.db"),
        data_backend=os.getenv("DATA_BACKEND", "hybrid")
    )

# Global configuration instance
CFE_CONFIG = load_cfe_config()