# Multi-View Dimension-Aware Dashboard System

## Executive Summary

Transform the Clio Legal Analytics dashboard into a **multi-dimensional visual intelligence platform** where each visualization reveals a different analytical perspective of legal practice operations. Users can seamlessly navigate between views to explore matters, departments, tasks, budgets, and relationships.

---

## Design Philosophy

**Core Principle**: Each visualization is a "window" into a specific dimension of the multidimensional data cube:

```
Data Dimensions:
├── Time (matter lifecycle, task duration)
├── Department (intake → prelitigation → litigation)
├── People (attorneys, staff, workload)
├── Resources (budget, hours, tasks)
├── Relationships (matter connections, dependencies)
└── Performance (efficiency, bottlenecks, outcomes)
```

**User Experience Flow**:
1. **Overview** → High-level KPIs (current state)
2. **Timeline** → See concurrent workflows (temporal dimension)
3. **Flow** → Understand department handoffs (process dimension)
4. **Correlation** → Analyze efficiency patterns (resource dimension)
5. **Heatmap** → Scan workload distribution (people dimension)
6. **Network** → Explore relationships (system dimension)

---

## System Architecture

### 1. Data Layer

**Unified Data Model**:
```python
# services/dashboard/domains/multidim_analytics.py

class MultiDimensionalAnalytics:
    """
    Unified data service for multi-view visualizations
    Aggregates data from MatterLifecycle, TaskActivity, and custom queries
    """

    def get_matter_timeline_data(self, start_date, end_date):
        """Multi-lane Gantt: matters as timeline bars"""
        return {
            'matter_id': [...],
            'matter_name': [...],
            'start_date': [...],
            'end_date': [...],
            'stage': [...],  # lane assignment
            'status': [...],  # color coding
            'attorney': [...]
        }

    def get_department_flow_data(self):
        """Sankey: matter flow between departments"""
        return {
            'source': ['Intake', 'Intake', 'Prelitigation', ...],
            'target': ['Prelitigation', 'Litigation', 'Litigation', ...],
            'value': [45, 12, 32, ...],  # matter count
            'stage_duration': [...]
        }

    def get_task_budget_correlation(self):
        """Parallel Coordinates: multi-attribute comparison"""
        return {
            'matter_id': [...],
            'tasks_completed': [...],
            'budget_spent': [...],
            'cycle_time': [...],
            'attorney_hours': [...],
            'outcome': [...]  # resolved/pending
        }

    def get_workload_matrix(self):
        """Heatmap: attorney x practice area workload"""
        return {
            'attorneys': ['J. Doe', 'J. Smith', ...],
            'practice_areas': ['Auto Accident', 'Med Mal', ...],
            'matrix': [[18, 12, 5], [23, 8, 15], ...]  # active matters
        }

    def get_relationship_network(self):
        """Network Graph: matter relationships"""
        return {
            'nodes': [
                {'id': 'M123', 'type': 'matter', 'size': 20, 'color': '...'},
                {'id': 'A456', 'type': 'attorney', 'size': 50, 'color': '...'}
            ],
            'edges': [
                {'source': 'M123', 'target': 'A456', 'weight': 5},
                {'source': 'M123', 'target': 'M789', 'weight': 2}
            ]
        }
```

### 2. Visualization Layer

**Tab Structure** (new tabs to add):
```
Current Tabs:
├── Overview (keep as-is)
├── Lifecycle (keep as-is)
├── Department (keep as-is)
└── Bottlenecks (keep as-is)

New Tabs:
├── Timeline (Multi-lane Gantt)
├── Flow (Sankey)
├── Correlation (Parallel Coordinates)
├── Workload (Matrix Heatmap)
└── Network (Optional - System Map)
```

### 3. Interaction Layer

**Dimension Navigation**:
- **Tab switching**: Smooth transitions between visualizations
- **Cross-filtering**: Click on Timeline → filter Flow view
- **Drill-down**: Click on department → see individual matters
- **Time scrubbing**: Slider to animate changes over time
- **Dimension selector**: Dropdown to switch heatmap dimensions

---

## Visualization Specifications

### 1. Matter Timeline (Multi-Lane Gantt)

**Purpose**: Visualize concurrent matter workflows to identify overlap and resource conflicts

**Plotly Chart Type**: `plotly.figure_factory.create_gantt()` or custom `go.Bar` with horizontal orientation

**Layout**:
```
Y-axis: Matter names (grouped by stage/attorney)
X-axis: Time (date range)
Lanes: Auto Accident | Medical Malpractice | Workers Comp
Color: Status (active=blue, overdue=red, completed=green)
```

**Implementation**:
```python
import plotly.figure_factory as ff
import plotly.graph_objects as go

def create_matter_timeline(data, COLORS):
    """Multi-lane Gantt chart"""

    # Option 1: Built-in Gantt
    fig = ff.create_gantt(
        data,
        colors=COLORS,
        index_col='stage',  # lanes
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True,
        showgrid_y=True
    )

    # Option 2: Custom horizontal bars (more control)
    fig = go.Figure()

    # Group matters by stage (lanes)
    for stage in ['Intake', 'Prelitigation', 'Litigation']:
        stage_matters = data[data['stage'] == stage]

        fig.add_trace(go.Bar(
            x=[end - start for start, end in zip(stage_matters['start_date'], stage_matters['end_date'])],
            y=stage_matters['matter_name'],
            base=stage_matters['start_date'],
            orientation='h',
            name=stage,
            marker=dict(color=COLORS[stage.lower()])
        ))

    fig.update_layout(
        barmode='overlay',
        xaxis=dict(type='date', title='Timeline'),
        yaxis=dict(title='Matters (grouped by stage)'),
        height=600,
        hovermode='closest'
    )

    return fig
```

**Key Features**:
- Click on bar → drill into matter details
- Hover → show matter name, attorney, days in stage
- Zoom/pan to explore timeline
- Toggle lanes on/off

---

### 2. Department Flow (Sankey Diagram)

**Purpose**: Understand how matters flow between departments and identify handoff bottlenecks

**Plotly Chart Type**: `go.Sankey`

**Layout**:
```
Nodes: [Intake] → [Prelitigation] → [Litigation] → [Resolved]
Links: Thickness = matter count
Color: Stage duration (gradient from green=fast to red=slow)
```

**Implementation**:
```python
import plotly.graph_objects as go

def create_department_flow(data, COLORS):
    """Sankey diagram for department flow"""

    # Define nodes
    nodes = ['Intake', 'Prelitigation', 'Litigation', 'Resolved', 'Dismissed']
    node_colors = [COLORS['primary'], COLORS['primary_light'], COLORS['gray_700'], COLORS['success'], COLORS['gray_500']]

    # Define links (source -> target)
    source = [0, 0, 1, 1, 2, 2]  # Intake -> Pre, Intake -> Lit, Pre -> Lit, Pre -> Resolved, etc.
    target = [1, 2, 2, 3, 3, 4]
    values = [45, 12, 32, 8, 15, 5]  # matter count

    # Color links by avg duration
    link_colors = ['rgba(30, 58, 95, 0.3)'] * len(values)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='white', width=0.5),
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=link_colors
        )
    )])

    fig.update_layout(
        title='Matter Flow Across Departments',
        font=dict(size=12, family="'Inter', sans-serif"),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
```

**Key Features**:
- Hover on link → show avg days in transition
- Click on node → filter to see matters in that stage
- Animate over time (slider to show flow by month)

---

### 3. Task & Budget Correlation (Parallel Coordinates)

**Purpose**: Reveal efficiency patterns and bottlenecks by comparing multiple attributes simultaneously

**Plotly Chart Type**: `go.Parcoords`

**Layout**:
```
Dimensions (vertical axes):
├── Tasks Completed (0-100)
├── Budget Spent ($) (0-50k)
├── Cycle Time (days) (0-180)
├── Attorney Hours (0-200)
└── Outcome (categorical: Resolved/Pending)

Each line = one matter
Color = outcome (green=resolved, blue=pending)
```

**Implementation**:
```python
import plotly.graph_objects as go

def create_task_budget_correlation(data, COLORS):
    """Parallel coordinates chart"""

    fig = go.Figure(data=go.Parcoords(
        line=dict(
            color=data['outcome_numeric'],  # 1=resolved, 0=pending
            colorscale=[[0, COLORS['primary']], [1, COLORS['success']]],
            showscale=True,
            cmin=0,
            cmax=1
        ),
        dimensions=[
            dict(
                label='Tasks Completed',
                values=data['tasks_completed'],
                range=[0, 100]
            ),
            dict(
                label='Budget Spent ($K)',
                values=data['budget_spent'] / 1000,
                range=[0, 50]
            ),
            dict(
                label='Cycle Time (days)',
                values=data['cycle_time'],
                range=[0, 180]
            ),
            dict(
                label='Attorney Hours',
                values=data['attorney_hours'],
                range=[0, 200]
            ),
            dict(
                label='Outcome',
                values=data['outcome_numeric'],
                tickvals=[0, 1],
                ticktext=['Pending', 'Resolved']
            )
        ]
    ))

    fig.update_layout(
        title='Task & Budget Correlation Analysis',
        font=dict(size=12, family="'Inter', sans-serif"),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
```

**Key Features**:
- Brush/select on any axis → highlight matching matters
- Identify outliers (high budget, low tasks = inefficiency)
- Find patterns (resolved matters cluster = efficiency pattern)

---

### 4. Overall Workload (Matrix Heatmap)

**Purpose**: Quick visual scanning of workload distribution across attorneys and practice areas

**Plotly Chart Type**: `go.Heatmap`

**Layout**:
```
X-axis: Practice Areas
Y-axis: Attorneys
Cell color: Active matters (gradient from white=0 to navy=30+)
Cell annotation: Number of active matters
```

**Implementation**:
```python
import plotly.graph_objects as go

def create_workload_heatmap(data, COLORS):
    """Matrix heatmap for workload"""

    fig = go.Figure(data=go.Heatmap(
        z=data['matrix'],  # 2D array
        x=data['practice_areas'],
        y=data['attorneys'],
        colorscale=[
            [0, COLORS['white']],
            [0.3, COLORS['gray_100']],
            [0.6, COLORS['primary_light']],
            [1.0, COLORS['primary']]
        ],
        text=data['matrix'],  # annotations
        texttemplate='%{text}',
        textfont=dict(size=11),
        hovertemplate='<b>%{y}</b><br>%{x}<br>%{z} active matters<extra></extra>',
        colorbar=dict(title='Active Matters')
    ))

    fig.update_layout(
        title='Workload Distribution: Attorney × Practice Area',
        xaxis=dict(title='Practice Area', side='bottom'),
        yaxis=dict(title='Attorney'),
        font=dict(size=12, family="'Inter', sans-serif"),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
```

**Key Features**:
- Click on cell → drill into specific attorney/practice area matters
- Dimension selector: Switch to Attorney × Stage or Attorney × Month
- Red highlight for overloaded cells (>25 matters)

---

### 5. Relationship Map (Network Graph)

**Purpose**: Explore matter relationships, attorney collaboration, and case dependencies

**Plotly Chart Type**: `go.Scatter` with custom network layout (or use `plotly-networkx`)

**Layout**:
```
Nodes:
├── Matters (circles, size = budget)
├── Attorneys (squares, size = caseload)
└── Practice Areas (diamonds, size = count)

Edges:
├── Matter → Attorney (assigned to)
├── Matter → Matter (related cases)
└── Attorney → Attorney (collaboration)

Color: Node type
```

**Implementation**:
```python
import plotly.graph_objects as go
import networkx as nx

def create_relationship_network(data, COLORS):
    """Network graph visualization"""

    # Create NetworkX graph
    G = nx.Graph()

    # Add nodes
    for node in data['nodes']:
        G.add_node(node['id'], **node)

    # Add edges
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

    # Compute layout (force-directed)
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    # Create edge traces
    edge_trace = go.Scatter(
        x=[], y=[],
        line=dict(width=0.5, color=COLORS['gray_300']),
        hoverinfo='none',
        mode='lines'
    )

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    # Create node traces
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        text=[G.nodes[node].get('id', '') for node in G.nodes()],
        textposition='top center',
        marker=dict(
            size=[G.nodes[node].get('size', 20) for node in G.nodes()],
            color=[COLORS['primary'] if G.nodes[node].get('type') == 'matter' else COLORS['success'] for node in G.nodes()],
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>%{text}</b><extra></extra>'
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title='Matter Relationship Network',
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
```

**Key Features**:
- Click on node → highlight connected nodes
- Drag nodes to reposition
- Filter by node type (show only matters, only attorneys)
- Cluster detection (identify attorney teams)

---

## Interaction Patterns

### Cross-View Filtering

When user interacts with one view, update related views:

```python
# app.py callback pattern

@app.callback(
    Output('timeline-graph', 'figure'),
    Output('flow-graph', 'figure'),
    Output('heatmap-graph', 'figure'),
    Input('dimension-selector', 'value'),  # e.g., 'practice_area', 'attorney'
    Input('date-range-slider', 'value'),
    Input('timeline-graph', 'clickData'),  # cross-filtering
    Input('flow-graph', 'clickData')
)
def update_all_views(dimension, date_range, timeline_click, flow_click):
    """Sync all visualizations when user interacts"""

    # Determine which view was clicked
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Apply filters
    if timeline_click:
        # User clicked on matter in timeline
        matter_id = timeline_click['points'][0]['customdata']
        # Filter other views to highlight this matter

    if flow_click:
        # User clicked on department node
        department = flow_click['points'][0]['label']
        # Filter timeline to show only matters in this department

    # Rebuild figures with filters
    timeline_fig = create_matter_timeline(filtered_data, COLORS)
    flow_fig = create_department_flow(filtered_data, COLORS)
    heatmap_fig = create_workload_heatmap(filtered_data, COLORS)

    return timeline_fig, flow_fig, heatmap_fig
```

### Smooth Transitions

**CSS Transitions** (already in place):
```css
/* custom.css - already implemented */
[class*="mantine-Paper"] {
    transition: all 0.25s ease;
}

/* Add for new visualizations */
.js-plotly-plot {
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

**Plotly Transitions**:
```python
fig.update_layout(
    transition={'duration': 500, 'easing': 'cubic-in-out'}
)
```

### Dimension Selector

Add interactive controls to switch dimensions:

```python
dmc.SegmentedControl(
    id='dimension-selector',
    data=[
        {'label': 'By Practice Area', 'value': 'practice_area'},
        {'label': 'By Attorney', 'value': 'attorney'},
        {'label': 'By Stage', 'value': 'stage'},
        {'label': 'By Month', 'value': 'month'}
    ],
    value='practice_area',
    size='sm'
)
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [ ] Create `MultiDimensionalAnalytics` data service
- [ ] Set up new tab structure in `app.py`
- [ ] Design mock data for all 5 visualizations

### Phase 2: Core Visualizations (Week 2-3)
- [ ] Implement Timeline (Gantt) - highest priority
- [ ] Implement Flow (Sankey) - highest priority
- [ ] Implement Correlation (Parallel Coordinates)
- [ ] Implement Workload (Heatmap)

### Phase 3: Advanced Features (Week 4)
- [ ] Implement Network Graph (optional)
- [ ] Add cross-view filtering
- [ ] Add dimension selectors
- [ ] Add time range slider

### Phase 4: Polish (Week 5)
- [ ] Smooth transitions
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] User testing and refinement

---

## Technical Considerations

### Performance
- **Large datasets**: Use Plotly Dash DataTable pagination for >1000 matters
- **Network graph**: Limit to 200 nodes, cluster large networks
- **Heatmap**: Use downsampling for >50x50 matrices
- **Caching**: Use `@cache.memoize()` for expensive computations

### Responsive Design
- Timeline: Horizontal scroll on mobile
- Sankey: Stack vertically on mobile
- Parallel Coordinates: Reduce dimensions to 3 on mobile
- Heatmap: Scrollable on mobile
- Network: Touch-friendly on mobile

### Accessibility
- Alt text for all visualizations
- Keyboard navigation for filters
- ARIA labels for interactive elements
- High contrast mode support

---

## Data Requirements

To implement these visualizations, we need:

**From ClioCore**:
```python
# Matter lifecycle data
- matter_id, matter_name, practice_area
- start_date, end_date, current_stage
- status (active/resolved/dismissed)
- assigned_attorney_id, assigned_attorney_name

# Stage transitions
- matter_id, from_stage, to_stage, transition_date
- days_in_stage

# Task data
- task_id, matter_id, task_name
- assigned_to, due_date, completed_date
- estimated_hours, actual_hours

# Financial data
- matter_id, budget_total, budget_spent
- billable_hours, billed_amount

# Relationships
- matter_id, related_matter_id, relationship_type
- matter_id, attorney_id, role
- attorney_id, collaborator_id, project_count
```

**Mock Data Structure** (for initial development):
```python
# dash_clio_dashboard/layouts/mock_multidim_data.py

MOCK_TIMELINE_DATA = [
    {'matter_id': 'M001', 'matter_name': 'Smith v. Jones', 'start': '2025-01-15', 'end': '2025-03-20', 'stage': 'Prelitigation', 'status': 'active'},
    # ... more matters
]

MOCK_FLOW_DATA = {
    'source': ['Intake', 'Intake', 'Prelitigation', 'Prelitigation', 'Litigation'],
    'target': ['Prelitigation', 'Litigation', 'Litigation', 'Resolved', 'Resolved'],
    'value': [45, 12, 32, 8, 15]
}

# ... etc
```

---

## Next Steps

**Decision Points**:

1. **Priority**: Which visualizations to implement first?
   - Recommended: Timeline + Flow (most impactful)

2. **Data Source**: Use mock data or connect to real ClioCore data?
   - Recommended: Start with mock, transition to real data

3. **Tab Structure**: Add new tabs or replace existing tabs?
   - Recommended: Add new tabs, keep existing for backward compatibility

4. **Complexity**: Implement all 5 visualizations or focus on 2-3 core ones?
   - Recommended: Start with Timeline, Flow, Heatmap (80% of value)

**Immediate Next Action**:
- Review this design document
- Decide on implementation priority
- I'll create the first visualization (Timeline or Flow)

---

## Questions for You

1. **Priority**: Which visualization is most critical for your users?
   - Timeline (see concurrent matters)?
   - Flow (understand department handoffs)?
   - Heatmap (scan workload)?

2. **Data**: Do you want to use mock data first, or connect to real ClioCore data?

3. **Scope**: Should I implement all 5 visualizations, or focus on 2-3 core ones?

4. **Timeline**: Is this a multi-week project, or do you want a quick prototype first?

Let me know your preferences and I'll start building!
