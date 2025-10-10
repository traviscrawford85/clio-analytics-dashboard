[ Dash Frontend (DMC + Plotly + React Components) ]
          ↓
[ Dash Backend (Python) – Unified Analytics API Layer ]
          ↓
 ┌─────────────────────────────────────────────┐
 |  ClioCore Polyglot Backend                  |
 |─────────────────────────────────────────────|
 |  • SQLite: clio-analytics.db                |
 |  • Neo4j Graph: matter relationships        |
 |  • ChromaDB: semantic retrieval (RAG)       |
 |─────────────────────────────────────────────|
 |  Unified Service Layer (Python Services)    |
 |  - MatterLifecycleService                   |
 |  - TaskActivityService                      |
 |  - AnalyticsService                         |
 |  - SemanticInsightsService (Chroma)         |
 └─────────────────────────────────────────────┘

🔗 3️⃣ Integration Strategy

Each persistence layer should expose a service module inside ClioCore, not be called directly from Dash.

For example:

```
services/
  ├── dashboard/
  │   ├── domains/
  │   │   ├── matter_lifecycle.py
  │   │   ├── task_activity.py
  │   │   ├── analytics_service.py
  │   │   └── semantic_insights.py

```

Each service wraps its respective data source:

SQLite → pandas DataFrame queries

Neo4j → Cypher queries (via neo4j or py2neo)

ChromaDB → semantic vector lookups

Then, your Dash callbacks (or layout initialization) can call a unified service layer, not each DB independently.

🧠 Example: Unified Service Layer Pattern


```
# services/dashboard/domains/unified_service.py
from .matter_lifecycle import MatterLifecycle
from .task_activity import TaskActivity
from .analytics_service import AnalyticsService
from .semantic_insights import SemanticInsights

class ClioUnifiedService:
    def __init__(self):
        self.matter = MatterLifecycle(backend="sqlite")
        self.task = TaskActivity(backend="sqlite")
        self.analytics = AnalyticsService(backend="sqlite")
        self.semantic = SemanticInsights(db_path="chromadb")

    def get_kpis(self):
        kpis = self.analytics.get_overview_kpis()
        graph_summary = self.matter.get_graph_summary()  # Neo4j
        return {**kpis, **graph_summary}

    def get_matter_network(self, limit=100):
        return self.matter.get_relationship_graph(limit=limit)

    def get_task_heatmap(self):
        return self.task.get_department_loads()

    def get_semantic_summary(self, matter_id):
        return self.semantic.query_related(matter_id)
```

Your Dash layout can now call:

```
service = ClioUnifiedService()
kpi_data = service.get_kpis()
matter_graph = service.get_matter_network()
semantic_notes = service.get_semantic_summary("12345")
```
This decouples the UI from your persistence design entirely.

🔄 4️⃣ Data Flow Example (Multi-Source Query)

Let’s take an example of how a dashboard “widget” like “Matter Lifecycle KPI” would aggregate across these systems.

| Step                                          | Source                                               | Role                           |
| --------------------------------------------- | ---------------------------------------------------- | ------------------------------ |
| Fetch all active matters                      | SQLite (`clio-analytics.db`)                         | Structured                     |
| Query Neo4j for connected departments + staff | Neo4j (`MATCH (m:Matter)-[:ASSIGNED_TO]->(s:Staff)`) | Relational Graph               |
| Pull semantic summary for each matter         | ChromaDB (`similarity_search`)                       | Text Insights                  |
| Merge                                         | pandas merge / join                                  | Unified view for visualization |


The resulting DataFrame can then be fed into Plotly or your React components.

📊 5️⃣ Example — Combining SQLite + Neo4j + Chroma

```
from neo4j import GraphDatabase
import sqlite3
import chromadb
import pandas as pd

class AnalyticsService:
    def __init__(self):
        self.sqlite_conn = sqlite3.connect("clio-analytics.db")
        self.neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        self.chroma = chromadb.Client(path="chromadb")

    def get_combined_insight(self, matter_id):
        # 1. Structured data
        sql = f"SELECT * FROM matters WHERE id = '{matter_id}'"
        matter_data = pd.read_sql(sql, self.sqlite_conn).to_dict("records")[0]

        # 2. Graph relationships
        cypher = """
        MATCH (m:Matter {id: $matter_id})-[:ASSIGNED_TO]->(s:Staff)
        RETURN s.name AS staff, s.department AS dept
        """
        with self.neo4j_driver.session() as session:
            staff_data = session.run(cypher, matter_id=matter_id).data()

        # 3. Semantic summary
        semantic_summary = self.chroma.query(
            collection_name="matter_notes",
            query_texts=[matter_data["description"]],
            n_results=3
        )

        return {
            "matter": matter_data,
            "staff": staff_data,
            "semantic": semantic_summary
        }

```

🧩 6️⃣ Best Practice: “Analytics API Layer”

Even though Dash runs in Python, treat this unified layer like an API inside your app:

Each visualization queries a method, not a database.

Each method returns normalized JSON or DataFrame, ready for charting.

Each service can evolve (swap SQLite for Postgres, or add Elasticsearch) without touching your dashboards.

🧠 7️⃣ Advanced: Use Neo4j as a “Relationship Engine” for Contextual Views

Neo4j can provide context like:

“Which matters are connected by shared adjusters, clients, or staff?”

“Which matters have overlapping tasks or delays in the same department?”

“How does workload cluster across staff nodes?”

You can visualize those relationships as an interactive Plotly Network Graph (or via Dash Cytoscape).