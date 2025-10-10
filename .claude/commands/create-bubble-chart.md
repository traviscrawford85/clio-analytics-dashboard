⚖️ How to Translate This Visualization to Legal Operations Data

In your firm’s workflow, each matter represents a node in a multidimensional space — with operational, financial, and performance variables.

We can use the same logic as the population-life expectancy example but remap the dimensions like this:


| Visualization Dimension | Legal Meaning                | Example Variable                                 |
| ----------------------- | ---------------------------- | ------------------------------------------------ |
| **X-axis**              | Workflow or Department Stage | `prelitigation`, `litigation`, `post-settlement` |
| **Y-axis**              | Matter Duration              | Days from open → current stage                   |
| **Z-axis**              | Total Expenses               | Sum of activity costs / fees                     |
| **Bubble Size**         | Workload Intensity           | Active tasks or hours logged                     |
| **Bubble Color**        | Outcome or Completion %      | Stage progress / probability of settlement       |
| **Tooltip**             | Context                      | Client name, staff, key deadlines                |


That turns this chart into a Matter Progress and Performance 3D Map, where managers can see at a glance:

which departments are overloaded,

which stages cost the most time or money, and

how outcomes correlate with workflow complexity.

⚙️ Example: matter_bubble_chart.py (Fully Ready Module)

Here’s a clean example that can slot straight into your Dash project:

```
import plotly.express as px
import pandas as pd
import sqlite3

def create_matter_bubble_chart(db_path="clio-analytics.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("""
        SELECT
            matter_id,
            client_name,
            department,
            stage_name,
            days_in_stage,
            total_expense,
            active_tasks,
            percent_complete,
            responsible_staff
        FROM matter_summary
        LIMIT 1000
    """, conn)
    conn.close()

    fig = px.scatter_3d(
        df,
        x="department",
        y="days_in_stage",
        z="total_expense",
        size="active_tasks",
        color="percent_complete",
        color_continuous_scale="Viridis",
        hover_name="matter_id",
        hover_data={
            "client_name": True,
            "responsible_staff": True,
            "stage_name": True,
            "days_in_stage": ":.0f",
            "total_expense": ":$,.0f",
        },
        title="Matter Progress and Performance 3D Map"
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="Department",
            yaxis_title="Days in Stage",
            zaxis_title="Total Expenses ($)",
            zaxis_type="log",
        ),
        coloraxis_colorbar=dict(title="% Complete"),
        margin=dict(l=0, r=0, b=0, t=40),
        height=700,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig

```
✅ Plug directly into your Dash layout:

```
dcc.Graph(
    id="matter-3d-bubble",
    figure=create_matter_bubble_chart(),
    config={"displayModeBar": False},
    style={"height": "700px"}
)
```
🧩 Enhancements (Optional)

Add Time Animation:
Let users “play through” quarterly or monthly evolution.
```
animation_frame="quarter"
```

This creates a dynamic temporal visualization — showing how matters evolve or cluster over time.

Cluster Highlighting:
Use symbol="department" or different color scales to separate clusters visually.

Crossfilter with Other Components:
When a bubble is clicked, trigger a callback that updates a Matter Detail Sidebar or Task Timeline.

```
@app.callback(
    Output("matter-details", "children"),
    Input("matter-3d-bubble", "clickData")
)
def show_matter_details(clickData):
    if not clickData:
        return "Select a matter to view details."
    matter_id = clickData["points"][0]["hovertext"]
    return get_matter_summary(matter_id)
```
Integrate with Neo4j for Contextual Relationships:
Clicking a node can also fetch connected matters from Neo4j — bridging this with your Cytoscape visualization.


When to Use 3D vs 2D in Dash

| Scenario                      | Visualization    | Rationale                      |
| ----------------------------- | ---------------- | ------------------------------ |
| Operational pattern discovery | 3D Bubble Chart  | Rich, multidimensional insight |
| Workflow bottlenecks          | Gantt / Timeline | Sequential flow clarity        |
| Department load               | 2D Heatmap       | Focused KPI density            |
| Relationship mapping          | Cytoscape Graph  | Entity connection depth        |


So, your Matter 3D Bubble Map becomes the “macro view,” while your Cytoscape graph provides a “relational drilldown.”

🧩 3️⃣ Your Adapted Version

Here’s a fully functional Plotly Graph Objects implementation using the same structure — ready to drop into your Dash dashboard.

```
import plotly.graph_objects as go
import pandas as pd
import sqlite3

def create_matter_3d_bubble_chart(db_path="clio-analytics.db"):
    # Connect to your analytics DB
    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        matter_id,
        department,
        days_in_stage,
        total_expense,
        active_tasks,
        percent_complete,
        client_name,
        responsible_staff
    FROM matter_summary
    LIMIT 1000
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Build the 3D bubble chart
    fig = go.Figure(data=go.Scatter3d(
        x=df['department'],
        y=df['days_in_stage'],
        z=df['total_expense'],
        text=df.apply(lambda row:
                      f"Matter: {row['matter_id']}<br>"
                      f"Client: {row['client_name']}<br>"
                      f"Staff: {row['responsible_staff']}<br>"
                      f"Stage Days: {row['days_in_stage']}<br>"
                      f"Expenses: ${row['total_expense']:,}<br>"
                      f"Progress: {row['percent_complete']}%",
                      axis=1),
        mode='markers',
        marker=dict(
            sizemode='diameter',
            sizeref=500,
            size=df['active_tasks'],
            color=df['percent_complete'],
            colorscale='Viridis',
            colorbar_title='Completion %',
            line_color='rgba(60,60,80,0.5)',
            line_width=0.5
        )
    ))

    fig.update_layout(
        title=dict(
            text="Matter Complexity and Progress Map",
            font=dict(size=18)
        ),
        scene=dict(
            xaxis_title="Department",
            yaxis_title="Days in Stage",
            zaxis_title="Total Expense ($)",
            zaxis_type="log",
            xaxis=dict(showgrid=True, zeroline=False),
            yaxis=dict(showgrid=True, zeroline=False),
            zaxis=dict(showgrid=True, zeroline=False),
        ),
        height=800,
        width=900,
        margin=dict(l=0, r=0, b=0, t=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    return fig

```

✅ Axes (3D): define the three spatial dimensions
✅ Marker attributes: control bubble size, color, and style
✅ Tooltips: show contextual data (city info)
✅ Colorscale + colorbar: maps numeric range to color intensity

⚖️ 2️⃣ How to Translate This for Your Legal Data Model

We’ll map the same structure to your matter attributes like this:

| Dimension        | Legal Meaning                | Example Variable                    |
| ---------------- | ---------------------------- | ----------------------------------- |
| **X-axis**       | Department or Workflow Stage | “Prelitigation”, “Litigation”, etc. |
| **Y-axis**       | Matter Duration              | `days_in_stage`                     |
| **Z-axis**       | Expenses or Settlement       | `total_expense`                     |
| **Bubble Size**  | Workload                     | Number of active tasks              |
| **Bubble Color** | Progress / Completion        | `percent_complete`                  |
| **Tooltip**      | Context                      | Matter ID, Client, Staff            |

Then in your Dash layout:

dcc.Graph(
    id="matter-3d-bubble",
    figure=create_matter_3d_bubble_chart(),
    config={"displayModeBar": False},
    style={"height": "700px"}
)

🧭 4️⃣ Notes on Enhancements

You can evolve this visualization further:

| Enhancement               | Method                                                   | Benefit                      |
| ------------------------- | -------------------------------------------------------- | ---------------------------- |
| **Dynamic filtering**     | Add dropdowns for department/staff                       | Focus on subsets of data     |
| **Color encoding switch** | Button toggle between completion %, expense, or workload | Different KPIs, same plot    |
| **Animate over time**     | Add `frames` by quarter or month                         | Show temporal trends         |
| **Neo4j integration**     | Color or size by relationship count                      | Visualize interconnectivity  |
| **Hover enrichment**      | Query Chroma summaries in callbacks                      | Semantic insights in tooltip |


🧩 5️⃣ If You’re Using Dash Mantine Components (DMC)

You can embed this in a modern DMC Paper card:

```
dmc.Paper([
    dmc.Title("Matter 3D Analytics", order=4, mb="sm"),
    dcc.Graph(figure=create_matter_3d_bubble_chart())
], shadow="xs", radius="md", withBorder=True)
```
That gives it consistent styling with your existing dashboard.