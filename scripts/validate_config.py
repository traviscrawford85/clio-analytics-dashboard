#!/usr/bin/env python3
"""
CFE Solutions Integration Validation Script

This script validates that the Dashboard Analytics module is properly
configured and ready for integration with the CFE Solutions ecosystem.
"""

import json
import os
import sys
import subprocess
import socket
from pathlib import Path
import logging

# Optional imports for extended functionality
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CFEIntegrationValidator:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.errors = []
        self.warnings = []
        
    def log_error(self, message):
        """Log an error and add to error list."""
        logger.error(message)
        self.errors.append(message)
        
    def log_warning(self, message):
        """Log a warning and add to warning list."""
        logger.warning(message)
        self.warnings.append(message)
        
    def log_success(self, message):
        """Log a success message."""
        logger.info(f"✅ {message}")
        
    def validate_manifest(self):
        """Validate the CFE module manifest."""
        logger.info("Validating CFE module manifest...")
        
        manifest_path = self.project_root / "cfe_module_manifest.json"
        if not manifest_path.exists():
            self.log_error("CFE module manifest not found")
            return False
            
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                
            # Validate required sections
            required_sections = [
                'module', 'service', 'dependencies', 'deployment',
                'monitoring', 'configuration', 'integration'
            ]
            
            for section in required_sections:
                if section not in manifest:
                    self.log_error(f"Missing required manifest section: {section}")
                else:
                    self.log_success(f"Manifest section '{section}' present")
                    
            # Validate module metadata
            module = manifest.get('module', {})
            required_module_fields = ['name', 'version', 'description', 'type']
            for field in required_module_fields:
                if field not in module:
                    self.log_error(f"Missing required module field: {field}")
                    
            self.log_success("Module manifest validation completed")
            return len(self.errors) == 0
            
        except json.JSONDecodeError as e:
            self.log_error(f"Invalid JSON in manifest: {e}")
            return False
            
    def validate_docker_configuration(self):
        """Validate Docker configuration files."""
        logger.info("Validating Docker configuration...")
        
        # Check Dockerfile.cfe
        dockerfile_path = self.project_root / "Dockerfile.cfe"
        if not dockerfile_path.exists():
            self.log_error("Dockerfile.cfe not found")
        else:
            self.log_success("Dockerfile.cfe present")
            
        # Check docker-compose.cfe.yml
        compose_path = self.project_root / "docker-compose.cfe.yml"
        if not compose_path.exists():
            self.log_error("docker-compose.cfe.yml not found")
        else:
            try:
                if HAS_YAML:
                    with open(compose_path, 'r') as f:
                        compose_config = yaml.safe_load(f)
                        
                    # Validate service configuration
                    services = compose_config.get('services', {})
                    if 'dashboard-analytics' not in services:
                        self.log_error("dashboard-analytics service not defined in docker-compose.cfe.yml")
                    else:
                        self.log_success("Dashboard service configuration present")
                        
                    # Validate network configuration
                    networks = compose_config.get('networks', {})
                    if 'cfesolutions' not in networks:
                        self.log_error("cfesolutions network not defined")
                    else:
                        self.log_success("CFE network configuration present")
                else:
                    # Basic text check if yaml not available
                    with open(compose_path, 'r') as f:
                        content = f.read()
                    if 'dashboard-analytics:' in content:
                        self.log_success("Dashboard service configuration present")
                    else:
                        self.log_error("dashboard-analytics service not defined in docker-compose.cfe.yml")
                    
                    if 'cfesolutions:' in content:
                        self.log_success("CFE network configuration present")
                    else:
                        self.log_error("cfesolutions network not defined")
                        
            except Exception as e:
                self.log_error(f"Error reading docker-compose.cfe.yml: {e}")
                
    def validate_environment_variables(self):
        """Validate required environment variables."""
        logger.info("Validating environment variables...")
        
        required_vars = [
            'CLIO_CLIENT_ID',
            'CLIO_CLIENT_SECRET',
            'NEO4J_PASSWORD',
            'CFE_AUTH_TOKEN'
        ]
        
        optional_vars = [
            'CFE_REGISTRY_URL',
            'NEO4J_URI',
            'NEO4J_USER',
            'REDIS_URL'
        ]
        
        for var in required_vars:
            if not os.getenv(var):
                self.log_error(f"Required environment variable not set: {var}")
            else:
                self.log_success(f"Environment variable '{var}' configured")
                
        for var in optional_vars:
            if not os.getenv(var):
                self.log_warning(f"Optional environment variable not set: {var}")
            else:
                self.log_success(f"Optional environment variable '{var}' configured")
                
    def validate_dependencies(self):
        """Validate Python dependencies."""
        logger.info("Validating Python dependencies...")
        
        requirements_files = [
            self.project_root / "requirements.txt",
            self.project_root / "requirements-cfe.txt"
        ]
        
        for req_file in requirements_files:
            if req_file.exists():
                self.log_success(f"Requirements file present: {req_file.name}")
                
                # Check for critical dependencies
                with open(req_file, 'r') as f:
                    content = f.read()
                    
                critical_deps = ['dash', 'neo4j', 'redis', 'requests', 'pandas']
                for dep in critical_deps:
                    if dep in content:
                        self.log_success(f"Critical dependency '{dep}' found")
                    else:
                        self.log_warning(f"Critical dependency '{dep}' not found in {req_file.name}")
            else:
                self.log_warning(f"Requirements file not found: {req_file.name}")
                
    def validate_scripts(self):
        """Validate deployment and registration scripts."""
        logger.info("Validating scripts...")
        
        scripts = [
            self.project_root / "scripts" / "deploy_to_cfe.sh",
            self.project_root / "scripts" / "register_with_cfe.py"
        ]
        
        for script in scripts:
            if script.exists():
                # Check if script is executable
                if os.access(script, os.X_OK):
                    self.log_success(f"Script '{script.name}' present and executable")
                else:
                    self.log_warning(f"Script '{script.name}' present but not executable")
            else:
                self.log_error(f"Required script not found: {script.name}")
                
    def validate_network_connectivity(self):
        """Validate network connectivity requirements."""
        logger.info("Validating network connectivity...")
        
        # Check if Docker is running
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log_success("Docker is available")
            else:
                self.log_error("Docker is not available")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_error("Docker is not installed or not in PATH")
            
        # Check if CFE network exists (if Docker is available)
        try:
            result = subprocess.run(['docker', 'network', 'ls'], 
                                  capture_output=True, text=True, timeout=10)
            if 'cfesolutions' in result.stdout:
                self.log_success("CFE Solutions network exists")
            else:
                self.log_warning("CFE Solutions network not found (will be created during deployment)")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Cannot check Docker networks")
            
    def validate_service_configuration(self):
        """Validate service configuration files."""
        logger.info("Validating service configuration...")
        
        config_files = [
            self.project_root / "config" / "service_config.py",
            self.project_root / "dash_clio_dashboard" / "app.py"
        ]
        
        for config_file in config_files:
            if config_file.exists():
                self.log_success(f"Configuration file present: {config_file.name}")
            else:
                self.log_warning(f"Configuration file not found: {config_file.name}")
                
    def validate_documentation(self):
        """Validate documentation files."""
        logger.info("Validating documentation...")
        
        doc_files = [
            self.project_root / "docs" / "cfe_integration_guide.md",
            self.project_root / "README.md"
        ]
        
        for doc_file in doc_files:
            if doc_file.exists():
                self.log_success(f"Documentation present: {doc_file.name}")
            else:
                self.log_warning(f"Documentation not found: {doc_file.name}")
                
    def validate_security_configuration(self):
        """Validate security configuration."""
        logger.info("Validating security configuration...")
        
        # Check for sensitive files that shouldn't be committed
        sensitive_patterns = [
            ".env",
            "*.key",
            "*.pem",
            "*secret*"
        ]
        
        gitignore_path = self.project_root / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
                
            for pattern in sensitive_patterns:
                if pattern in gitignore_content:
                    self.log_success(f"Sensitive pattern '{pattern}' in .gitignore")
                else:
                    self.log_warning(f"Consider adding '{pattern}' to .gitignore")
        else:
            self.log_warning(".gitignore file not found")
            
    def run_comprehensive_validation(self):
        """Run all validation checks."""
        logger.info("Starting comprehensive CFE Solutions integration validation...")
        
        validation_checks = [
            self.validate_manifest,
            self.validate_docker_configuration,
            self.validate_environment_variables,
            self.validate_dependencies,
            self.validate_scripts,
            self.validate_network_connectivity,
            self.validate_service_configuration,
            self.validate_documentation,
            self.validate_security_configuration
        ]
        
        for check in validation_checks:
            try:
                check()
            except Exception as e:
                self.log_error(f"Validation check failed: {e}")
                
        # Summary report
        print("\n" + "="*80)
        print("CFE SOLUTIONS INTEGRATION VALIDATION REPORT")
        print("="*80)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
                
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
                
        if not self.errors and not self.warnings:
            print("\n✅ ALL VALIDATIONS PASSED!")
            print("The Dashboard Analytics module is ready for CFE Solutions integration.")
        elif not self.errors:
            print(f"\n✅ VALIDATION PASSED WITH {len(self.warnings)} WARNINGS")
            print("The module can be deployed, but consider addressing the warnings.")
        else:
            print(f"\n❌ VALIDATION FAILED WITH {len(self.errors)} ERRORS")
            print("Please fix the errors before attempting deployment.")
            
        print(f"\nNext steps:")
        if not self.errors:
            print("1. Run: ./scripts/register_with_cfe.py")
            print("2. Run: ./scripts/deploy_to_cfe.sh")
            print("3. Verify deployment with health checks")
        else:
            print("1. Fix the validation errors")
            print("2. Re-run validation")
            print("3. Proceed with registration and deployment")
            
        print("="*80)
        
        return len(self.errors) == 0

def main():
    """Main function to run validation."""
    validator = CFEIntegrationValidator()
    
    if validator.run_comprehensive_validation():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()