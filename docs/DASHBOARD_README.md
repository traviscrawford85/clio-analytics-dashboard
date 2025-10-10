# Clio KPI Dashboard

A modern, animated KPI dashboard for Clio legal practice management, built with Plotly Dash + React + Anime.js.

## Features

✨ **8 Animated React Components**
- `AnimatedKPI` - Sleek KPI cards with number count-up animations
- `StageProgressBar` - Interactive horizontal progress bar for matter stages
- `TaskTracker` - Task list with status indicators and overdue highlighting
- `WorkloadCard` - Staff workload cards with completion rate rings
- `MatterBudget` - Circular budget progress indicators
- `TaskTimeline` - Mini Gantt-style task timeline
- `BottleneckRadar` - Radar chart for bottleneck visualization
- `WorkloadMatrix` - Heatmap showing workload distribution

🎯 **4 Dashboard Views**
- **Overview** - Executive KPIs and high-level metrics
- **Lifecycle** - Matter progression through workflow stages
- **Department** - Team workload and performance analytics
- **Bottlenecks** - Process bottleneck identification and stuck matters

🔌 **ClioCore Integration**
- Seamless integration with modular ClioCore backend
- Domain service architecture (`MatterLifecycle`, `TaskActivity`)
- SQLite database support (`clio-analytics.db`)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
python dash_clio_dashboard/app.py

# Visit: http://localhost:8050
```

## Architecture

```
dash-component-boilerplate/
├── src/lib/components/          # React components (Anime.js)
├── dash_clio_dashboard/         # Dash application
│   ├── app.py                   # Main Dash app
│   ├── layouts/                 # Dashboard layouts
│   │   ├── overview.py
│   │   ├── lifecycle.py
│   │   ├── department.py
│   │   └── bottlenecks.py
│   └── callbacks/               # Dash callbacks (future)
└── requirements.txt
```

See full documentation in DASHBOARD_README.md
