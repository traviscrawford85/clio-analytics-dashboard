# Clio KPI Dashboard - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │              Browser (Chrome, Firefox, Safari)                 │ │
│  │  http://localhost:8050                                         │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTP/WebSocket
┌────────────────────────────────▼────────────────────────────────────┐
│                      Dash Application Server                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  app.py (Main Application)                                     │ │
│  │  - Flask server                                                │ │
│  │  - Routing & navigation                                        │ │
│  │  - Auto-refresh (30s interval)                                 │ │
│  │  - Callback management                                         │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Dashboard Layouts (Python)                                    │ │
│  │  ├─ overview.py       → Executive KPIs                         │ │
│  │  ├─ lifecycle.py      → Matter progression                     │ │
│  │  ├─ department.py     → Team analytics                         │ │
│  │  └─ bottlenecks.py    → Process bottlenecks                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ Function Calls
┌────────────────────────────────▼────────────────────────────────────┐
│                     ClioCore Domain Services                         │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  MatterLifecycle (domain service)                              │ │
│  │  - get_matters_overview()                                      │ │
│  │  - get_stage_distribution()                                    │ │
│  │  - get_available_stages()                                      │ │
│  │  - get_stale_matters(days_threshold)                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  TaskActivity (domain service)                                 │ │
│  │  - get_task_metrics()                                          │ │
│  │  - get_urgency_summary()                                       │ │
│  │  - get_user_workload()                                         │ │
│  │  - get_tasks_by_urgency()                                      │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ SQL Queries
┌────────────────────────────────▼────────────────────────────────────┐
│                    SQLite Database (clio-analytics.db)               │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Core Tables:                                                  │ │
│  │  - Matters (ID, Status, Practice_Area, Matter_Stage_ID,...)   │ │
│  │  - Tasks (ID, Matter, Status, Due_At, Assignee,...)           │ │
│  │  - MatterStages (ID, Name, Order, Type)                       │ │
│  │  - Users (ID, Name, Email, Role)                              │ │
│  │  - Activities (ID, Matter, Date, Total)                       │ │
│  │  - PracticeAreas (ID, Name)                                   │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ Data Ingestion (External)
┌────────────────────────────────▼────────────────────────────────────┐
│                         Clio API (External)                          │
│  - Matters API                                                       │
│  - Tasks API                                                         │
│  - Activities API                                                    │
│  - Users API                                                         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                   React Component Library (Anime.js)                  │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │
│  │  AnimatedKPI    │  │ StageProgress   │  │  TaskTracker    │      │
│  │                 │  │      Bar        │  │                 │      │
│  │ • Number count  │  │ • Width grow    │  │ • Stagger fade  │      │
│  │ • Fade-in       │  │ • Interactive   │  │ • Pulse overdue │      │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘      │
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │
│  │  WorkloadCard   │  │  MatterBudget   │  │  TaskTimeline   │      │
│  │                 │  │                 │  │                 │      │
│  │ • Ring progress │  │ • Circular prog │  │ • Bar growth    │      │
│  │ • Scale entrance│  │ • Stroke offset │  │ • Shimmer effect│      │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘      │
│                                                                       │
│  ┌─────────────────┐  ┌─────────────────┐                           │
│  │ BottleneckRadar │  │ WorkloadMatrix  │                           │
│  │                 │  │                 │                           │
│  │ • Canvas render │  │ • Grid stagger  │                           │
│  │ • Radar animate │  │ • Heatmap color │                           │
│  └─────────────────┘  └─────────────────┘                           │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Architecture

```
┌──────────────┐
│  Clio API    │ (External system)
└──────┬───────┘
       │ Periodic Sync (Ingestion Pipeline)
       ▼
┌──────────────────────────────────────────┐
│  clio-analytics.db (SQLite)              │
│  ┌────────────────────────────────────┐  │
│  │ Matters     Tasks      Activities  │  │
│  │ Users       Stages     PracticeAreas│ │
│  └────────────────────────────────────┘  │
└──────┬───────────────────────────────────┘
       │ Domain Service Queries
       ▼
┌──────────────────────────────────────────┐
│  ClioCore Domain Services                │
│  ┌────────────────────────────────────┐  │
│  │ MatterLifecycle                    │  │
│  │ • Aggregate matter data            │  │
│  │ • Calculate stage metrics          │  │
│  │ • Identify stale matters           │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ TaskActivity                       │  │
│  │ • Compute task urgency             │  │
│  │ • Calculate user workload          │  │
│  │ • Analyze completion rates         │  │
│  └────────────────────────────────────┘  │
└──────┬───────────────────────────────────┘
       │ Processed DataFrames
       ▼
┌──────────────────────────────────────────┐
│  Dash Layouts (Python)                   │
│  ┌────────────────────────────────────┐  │
│  │ • Transform data for visualization │  │
│  │ • Create Plotly figures            │  │
│  │ • Build component props            │  │
│  └────────────────────────────────────┘  │
└──────┬───────────────────────────────────┘
       │ JSON Props
       ▼
┌──────────────────────────────────────────┐
│  React Components (Browser)              │
│  ┌────────────────────────────────────┐  │
│  │ • Render visualizations            │  │
│  │ • Apply Anime.js animations        │  │
│  │ • Handle user interactions         │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

---

## Animation Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    Anime.js Animation Pipeline                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Component Mount (useEffect)                                     │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────┐                            │
│  │ Identify target DOM elements    │                            │
│  │ (via className or ref)          │                            │
│  └────────────┬────────────────────┘                            │
│               │                                                  │
│               ▼                                                  │
│  ┌─────────────────────────────────┐                            │
│  │ Configure anime() parameters:   │                            │
│  │ • targets                        │                            │
│  │ • properties to animate          │                            │
│  │ • duration (ms)                  │                            │
│  │ • easing function                │                            │
│  │ • delay / stagger                │                            │
│  └────────────┬────────────────────┘                            │
│               │                                                  │
│               ▼                                                  │
│  ┌─────────────────────────────────┐                            │
│  │ Execute animation:               │                            │
│  │ • Interpolate values             │                            │
│  │ • Update DOM on each frame       │                            │
│  │ • Apply easing function          │                            │
│  └────────────┬────────────────────┘                            │
│               │                                                  │
│               ▼                                                  │
│  ┌─────────────────────────────────┐                            │
│  │ Animation complete               │                            │
│  │ (final state rendered)           │                            │
│  └─────────────────────────────────┘                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

Example: AnimatedKPI Number Count-Up

1. Component mounts with value=145
2. anime() targets the DOM element
3. Animates innerHTML from 0 → 145
4. Duration: 1200ms
5. Easing: easeOutExpo (fast start, slow end)
6. Result: Smooth number count animation
```

---

## Deployment Architecture

### Development Environment

```
┌─────────────────────────────────────────────┐
│  Developer Workstation                      │
│  ┌───────────────────────────────────────┐  │
│  │  dash-component-boilerplate/          │  │
│  │  ├── src/lib/components/ (React)      │  │
│  │  ├── dash_clio_dashboard/ (Dash app)  │  │
│  │  └── venv/ (Python virtualenv)        │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  dashboard-neo4j/                     │  │
│  │  ├── services/dashboard/domains/      │  │
│  │  └── data/analytics/                  │  │
│  │      └── clio-analytics.db            │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘

Run: ./run_dashboard.sh
Access: http://localhost:8050
```

### Production Environment (Docker)

```
┌─────────────────────────────────────────────────────────┐
│  Docker Host                                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  clio-dashboard (Container)                       │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Dash App (Python)                          │  │  │
│  │  │  Port: 8050 → 80                            │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  Volume Mount:                              │  │  │
│  │  │  /data → ../dashboard-neo4j/data/analytics  │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Nginx Reverse Proxy (Optional)                   │  │
│  │  Port: 80 → 8050 (clio-dashboard)                │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

Access: https://dashboard.yourdomain.com
```

---

## Security Architecture

```
┌────────────────────────────────────────────────────────┐
│  Security Layers                                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Layer 1: Network Security                            │
│  ┌──────────────────────────────────────────────────┐ │
│  │ • Firewall rules (allow port 8050 only)         │ │
│  │ • HTTPS/TLS encryption (reverse proxy)          │ │
│  │ • Rate limiting (prevent DoS)                    │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Layer 2: Application Security                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ • Input validation (Dash callbacks)              │ │
│  │ • SQL injection prevention (parameterized)       │ │
│  │ • XSS protection (React escaping)                │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Layer 3: Data Access Security                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ • Read-only database connection                  │ │
│  │ • Domain service abstraction                     │ │
│  │ • No direct SQL from UI                          │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  Future: Layer 4 - Authentication (Phase 2)           │
│  ┌──────────────────────────────────────────────────┐ │
│  │ • OAuth 2.0 / OIDC                               │ │
│  │ • Role-based access control (RBAC)               │ │
│  │ • Session management                             │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## Performance Optimization Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Performance Optimization Strategies                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. Data Layer                                           │
│  ┌────────────────────────────────────────────────────┐ │
│  │ • Indexed database queries                         │ │
│  │ • Result set limits (e.g., LIMIT 500)             │ │
│  │ • Aggregation in SQL (not Python)                 │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  2. Application Layer                                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │ • @lru_cache for expensive functions               │ │
│  │ • Lazy loading of dashboard views                  │ │
│  │ • Debounced filter inputs (300ms)                  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  3. Frontend Layer                                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │ • React memoization (useMemo, useCallback)         │ │
│  │ • Throttled animations (skip frames if needed)     │ │
│  │ • Virtualized lists (for long tables)              │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  4. Network Layer                                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │ • Gzip compression                                  │ │
│  │ • CDN for static assets (future)                   │ │
│  │ • WebSocket for real-time updates (future)         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Scalability Architecture (Future)

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Horizontal Scaling                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Load Balancer (Nginx/HAProxy)                       │ │
│  └─────┬─────────────────────────────────────────┬───────┘ │
│        │                                         │         │
│  ┌─────▼─────────┐                       ┌──────▼────────┐ │
│  │ Dash Instance │                       │ Dash Instance │ │
│  │ (Container 1) │                       │ (Container 2) │ │
│  └─────┬─────────┘                       └──────┬────────┘ │
│        │                                         │         │
│        └────────────┬────────────────────────────┘         │
│                     │                                      │
│            ┌────────▼─────────┐                            │
│            │  Redis Cache     │ (Shared session storage)   │
│            └────────┬─────────┘                            │
│                     │                                      │
│            ┌────────▼─────────┐                            │
│            │  PostgreSQL DB   │ (Migrated from SQLite)     │
│            └──────────────────┘                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack Details

### Backend

```
Python 3.11+
├── dash (2.14+)              # Web framework
├── dash-bootstrap-components # UI components
├── plotly (5.18+)            # Visualizations
├── pandas (2.0+)             # Data processing
└── sqlite3 (built-in)        # Database driver
```

### Frontend

```
React 18+
├── anime.js (4.2+)           # Animation library
├── prop-types                # Type checking
└── Bootstrap 5               # CSS framework
```

### Infrastructure

```
Operating System: Linux/macOS/Windows
Web Server: Flask (development) / Gunicorn (production)
Database: SQLite (development) / PostgreSQL (production)
Reverse Proxy: Nginx (optional, production)
Containerization: Docker (optional)
```

---

## File Structure Mapping

```
dash-component-boilerplate/
│
├── src/lib/components/              ← React Components (Anime.js)
│   ├── AnimatedKPI.react.js
│   ├── StageProgressBar.react.js
│   ├── TaskTracker.react.js
│   ├── WorkloadCard.react.js
│   ├── MatterBudget.react.js
│   ├── TaskTimeline.react.js
│   ├── BottleneckRadar.react.js
│   ├── WorkloadMatrix.react.js
│   └── index.js
│
├── dash_clio_dashboard/             ← Dash Application
│   ├── app.py                       ← Main entry point
│   ├── __init__.py
│   │
│   ├── layouts/                     ← Dashboard views
│   │   ├── __init__.py
│   │   ├── overview.py              ← Executive KPIs
│   │   ├── lifecycle.py             ← Matter progression
│   │   ├── department.py            ← Team analytics
│   │   └── bottlenecks.py           ← Bottleneck analysis
│   │
│   ├── callbacks/                   ← Interactive callbacks (future)
│   │   └── __init__.py
│   │
│   └── utils/                       ← Helper functions (future)
│       └── __init__.py
│
├── requirements.txt                 ← Python dependencies
├── package.json                     ← Node.js dependencies
├── run_dashboard.sh                 ← Quick start script
│
├── DASHBOARD_README.md              ← Quick start guide
├── IMPLEMENTATION_GUIDE.md          ← Technical documentation
├── PROJECT_SUMMARY.md               ← Project overview
└── ARCHITECTURE.md                  ← This file
```

---

## Integration Points

### ClioCore Domain Services

```python
# Location: ../dashboard-neo4j/services/dashboard/domains/

MatterLifecycle
  ├── get_matters_overview(limit, practice_area)
  ├── get_available_stages()
  ├── get_stage_distribution()
  ├── get_litigation_stage_analysis()
  ├── get_litigation_summary()
  └── get_stale_matters(days_threshold)

TaskActivity
  ├── get_task_metrics()
  ├── get_urgency_summary()
  ├── get_tasks_by_urgency()
  ├── get_all_tasks(limit, order_col, order_dir)
  ├── get_tasks_by_practice_area()
  ├── get_tasks_by_assignee()
  ├── get_user_workload()
  └── get_top_users_by_overdue(limit)
```

### Database Schema Integration

```sql
-- Core relationships

Matters 1──┬──* Tasks
           ├──1 MatterStages
           ├──1 PracticeAreas
           ├──1 Users (Responsible_Staff)
           └──* Activities

Tasks *──1 Users (Assignee)

Activities *──1 Matters
```

---

## Monitoring & Observability (Future)

```
┌────────────────────────────────────────────┐
│  Application Monitoring                    │
├────────────────────────────────────────────┤
│                                            │
│  Logs                                      │
│  ├─ Application logs (stdout/stderr)      │
│  ├─ Error tracking (Sentry/Rollbar)       │
│  └─ Access logs (Nginx)                   │
│                                            │
│  Metrics                                   │
│  ├─ Request rate (requests/sec)           │
│  ├─ Response time (avg, p95, p99)         │
│  ├─ Error rate (5xx errors)               │
│  └─ Database query performance            │
│                                            │
│  Health Checks                             │
│  ├─ /health endpoint                      │
│  ├─ Database connectivity                 │
│  └─ ClioCore availability                 │
│                                            │
└────────────────────────────────────────────┘
```

---

## Conclusion

This architecture provides a **solid foundation** for the Clio KPI Dashboard with:

✅ **Scalability** - Can handle growth in data volume and user base
✅ **Maintainability** - Clean separation of concerns (data / business logic / presentation)
✅ **Performance** - Optimized queries, caching, lazy loading
✅ **Security** - Multiple layers of protection (network, application, data)
✅ **Extensibility** - Easy to add new components, views, and integrations

**Next Steps**: Deploy to production and begin Phase 2 enhancements (real-time updates, advanced filtering, export functionality).
