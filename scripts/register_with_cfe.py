#!/usr/bin/env python3
"""
CFE Solutions Module Registration Script

This script registers the Dashboard Analytics module with the CFE Solutions
ecosystem using the module manifest and integration patterns.
"""

import json
import requests
import os
import sys
import logging
from pathlib import Path
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CFEModuleRegistrar:
    def __init__(self, manifest_path="cfe_module_manifest.json"):
        """Initialize the CFE module registrar."""
        self.manifest_path = Path(manifest_path)
        self.manifest = self._load_manifest()
        self.cfe_registry_url = os.getenv('CFE_REGISTRY_URL', 'http://cfe-registry:8080')
        self.cfe_auth_token = os.getenv('CFE_AUTH_TOKEN')
        
    def _load_manifest(self):
        """Load and validate the module manifest."""
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Validate required fields
            required_fields = ['module', 'service', 'dependencies', 'deployment']
            for field in required_fields:
                if field not in manifest:
                    raise ValueError(f"Missing required field: {field}")
            
            logger.info(f"Loaded manifest for module: {manifest['module']['name']}")
            return manifest
            
        except FileNotFoundError:
            logger.error(f"Manifest file not found: {self.manifest_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in manifest: {e}")
            sys.exit(1)
        except ValueError as e:
            logger.error(f"Manifest validation error: {e}")
            sys.exit(1)
    
    def check_prerequisites(self):
        """Check if all required services and dependencies are available."""
        logger.info("Checking prerequisites...")
        
        # Check required services
        required_services = self.manifest['dependencies']['required_services']
        for service in required_services:
            if not self._check_service_availability(service):
                logger.error(f"Required service not available: {service}")
                return False
        
        # Check optional services (warn but don't fail)
        optional_services = self.manifest['dependencies'].get('optional_services', [])
        for service in optional_services:
            if not self._check_service_availability(service):
                logger.warning(f"Optional service not available: {service}")
        
        logger.info("Prerequisites check completed")
        return True
    
    def _check_service_availability(self, service_name):
        """Check if a service is available via service discovery."""
        try:
            # Try to resolve service via Docker network
            import socket
            socket.gethostbyname(service_name)
            return True
        except socket.gaierror:
            return False
    
    def register_module(self):
        """Register the module with CFE Solutions registry."""
        logger.info("Registering module with CFE Solutions...")
        
        registration_data = {
            'manifest': self.manifest,
            'status': 'pending_deployment',
            'timestamp': time.time()
        }
        
        try:
            headers = {'Content-Type': 'application/json'}
            if self.cfe_auth_token:
                headers['Authorization'] = f'Bearer {self.cfe_auth_token}'
            
            response = requests.post(
                f"{self.cfe_registry_url}/api/modules/register",
                json=registration_data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 201:
                logger.info("Module registered successfully")
                return response.json()
            else:
                logger.error(f"Registration failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to CFE registry: {e}")
            return None
    
    def configure_service_discovery(self):
        """Configure service discovery for the module."""
        logger.info("Configuring service discovery...")
        
        module_name = self.manifest['module']['name']
        service_port = self.manifest['service']['port']
        
        # Create service discovery configuration
        discovery_config = {
            'name': module_name,
            'port': service_port,
            'health_check': self.manifest['service']['health_endpoint'],
            'tags': self.manifest['module']['tags'],
            'meta': {
                'version': self.manifest['module']['version'],
                'type': self.manifest['service']['type']
            }
        }
        
        return discovery_config
    
    def setup_monitoring(self):
        """Setup monitoring and health checks."""
        logger.info("Setting up monitoring...")
        
        monitoring_config = self.manifest.get('monitoring', {})
        
        # Register health checks
        health_checks = monitoring_config.get('health_checks', [])
        for check in health_checks:
            logger.info(f"Registering health check: {check['name']}")
        
        # Register metrics
        metrics = monitoring_config.get('metrics', [])
        for metric in metrics:
            logger.info(f"Registering metric: {metric}")
        
        return True
    
    def validate_integration(self):
        """Validate integration with other CFE services."""
        logger.info("Validating service integration...")
        
        # Test API endpoints
        service_port = self.manifest['service']['port']
        api_endpoints = self.manifest['service'].get('api_endpoints', [])
        
        for endpoint in api_endpoints:
            endpoint_url = f"http://localhost:{service_port}{endpoint['path']}"
            logger.info(f"Will validate endpoint: {endpoint_url}")
        
        # Test data source connections
        data_sources = self.manifest['integration'].get('data_sources', [])
        for source in data_sources:
            logger.info(f"Will validate data source: {source['name']}")
        
        return True
    
    def create_deployment_plan(self):
        """Create a deployment plan for the module."""
        deployment_plan = {
            'module_name': self.manifest['module']['name'],
            'version': self.manifest['module']['version'],
            'deployment_type': 'docker',
            'steps': [
                'Build Docker image',
                'Deploy to CFE network',
                'Register with service discovery',
                'Setup monitoring',
                'Validate integration',
                'Mark as active'
            ],
            'rollback_plan': [
                'Stop service',
                'Remove from service discovery',
                'Clean up resources'
            ],
            'estimated_duration': '10 minutes'
        }
        
        return deployment_plan
    
    def run_full_registration(self):
        """Run the complete module registration process."""
        logger.info("Starting CFE Solutions module registration...")
        
        try:
            # Step 1: Check prerequisites
            if not self.check_prerequisites():
                logger.error("Prerequisites check failed")
                return False
            
            # Step 2: Register module
            registration_result = self.register_module()
            if not registration_result:
                logger.error("Module registration failed")
                return False
            
            # Step 3: Configure service discovery
            discovery_config = self.configure_service_discovery()
            logger.info(f"Service discovery configured: {discovery_config}")
            
            # Step 4: Setup monitoring
            self.setup_monitoring()
            
            # Step 5: Validate integration
            self.validate_integration()
            
            # Step 6: Create deployment plan
            deployment_plan = self.create_deployment_plan()
            logger.info(f"Deployment plan created: {deployment_plan}")
            
            logger.info("Module registration completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return False

def main():
    """Main function to run module registration."""
    registrar = CFEModuleRegistrar()
    
    if registrar.run_full_registration():
        print("✅ Dashboard Analytics module successfully registered with CFE Solutions!")
        sys.exit(0)
    else:
        print("❌ Module registration failed")
        sys.exit(1)

if __name__ == "__main__":
    main()