# Documentation Directory

This directory contains all project documentation organized for easy reference.

## Table of Contents

### Architecture & Design
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture overview
- **[ARCHITECTURE_AUDIT.md](./ARCHITECTURE_AUDIT.md)** - Architecture audit findings
- **[ARCHITECTURE_AUDIT_COMPLETE.md](./ARCHITECTURE_AUDIT_COMPLETE.md)** - Complete architecture audit report
- **[MULTIDIMENSIONAL_DESIGN.md](./MULTIDIMENSIONAL_DESIGN.md)** - Multidimensional data visualization design
- **[NEW_DESIGN.md](./NEW_DESIGN.md)** - Latest design specifications
- **[CORPORATE_REDESIGN.md](./CORPORATE_REDESIGN.md)** - Corporate branding and design

### Implementation Guides
- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** - Main implementation guide
- **[BUILD_GUIDE.md](./BUILD_GUIDE.md)** - Build and deployment instructions
- **[DOCKER_GUIDE.md](./DOCKER_GUIDE.md)** - Docker containerization guide

### Features & Components
- **[ANIMATIONS_README.md](./ANIMATIONS_README.md)** - Animation system documentation
- **[ANIMATION_STRATEGY.md](./ANIMATION_STRATEGY.md)** - Animation implementation strategy
- **[HEATMAP_IMPLEMENTATION.md](./HEATMAP_IMPLEMENTATION.md)** - Heatmap feature documentation
- **[DASHBOARD_README.md](./DASHBOARD_README.md)** - Dashboard component overview
- **[WIREFRAME.md](./WIREFRAME.md)** - UI wireframes and mockups
- **[MERMAIDCHART.md](./MERMAIDCHART.md)** - System diagrams and charts

### Integration & Configuration
- **[CFE_INTEGRATION_SUMMARY.md](./CFE_INTEGRATION_SUMMARY.md)** - CFE Solutions integration summary
- **[cfe_integration_guide.md](./cfe_integration_guide.md)** - Detailed CFE integration guide
- **[CLIO_ANALYTICS_DASHBOARD_INTEGRATION.md](./CLIO_ANALYTICS_DASHBOARD_INTEGRATION.md)** - Clio Analytics dashboard integration

### Project Management
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Project overview and summary
- **[UPDATES_SUMMARY.md](./UPDATES_SUMMARY.md)** - Recent updates and changes
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history and changes

### Additional Resources
- **[README_CFESOLUTIONS.md](./README_CFESOLUTIONS.md)** - CFE Solutions specific documentation

---

## Project Directory Structure

```
dash-component-boilerplate/
├── docs/                       # All documentation (you are here)
├── reports/                    # Business reports and data exports
│   ├── task_reports/          # Task-related reports
│   ├── matter_reports/        # Legal matter data and analysis
│   ├── custom_field_reports/  # Custom field configurations
│   └── contact_reports/       # Contact and client exports
├── scripts/                    # Automation scripts
│   ├── register_with_cfe.py   # CFE registration script
│   ├── validate_config.py     # Configuration validation
│   ├── deploy_to_cfe.sh       # Deployment automation
│   ├── show_final_user_summary.py  # User summary generation
│   └── test_3d_component.py   # 3D component testing
├── dash_clio_dashboard/       # Main dashboard application
├── config/                     # Configuration files
└── src/                        # Source code
```

---

## Contributing to Documentation

When adding new documentation:
1. Place `.md` files in the appropriate category within this `docs/` folder
2. Update this README's table of contents
3. Use clear, descriptive filenames with underscores or hyphens
4. Include a brief summary at the top of each document

For technical diagrams, consider using Mermaid syntax (see [MERMAIDCHART.md](./MERMAIDCHART.md) for examples).
