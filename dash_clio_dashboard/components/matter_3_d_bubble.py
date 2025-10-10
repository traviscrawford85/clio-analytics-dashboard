"""
3D Matter Bubble Component - Professional Implementation
Integrates with the existing matter_3d_analytics.py service
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from dash import dcc, html, Input, Output, callback
import dash_mantine_components as dmc
import plotly.graph_objects as go

try:
    from services.matter_3d_analytics import matter_3d_service
    SERVICE_AVAILABLE = True
except ImportError:
    SERVICE_AVAILABLE = False
    print("Warning: matter_3d_analytics service not available, using fallback data")

# Corporate color scheme matching the dashboard
COLORS = {
    'primary': '#1E3A5F',
    'primary_light': '#2C5282',
    'success': '#276749',
    'warning': '#975A16',
    'danger': '#9B2C2C',
    'gray_700': '#4A5568',
    'gray_300': '#CBD5E0',
    'white': '#FFFFFF'
}

def load_matter_3d_data(department_filter=None, limit=200):
    """Load 3D matter data using the analytics service"""
    if SERVICE_AVAILABLE:
        return matter_3d_service.get_matter_3d_data(limit=limit, department_filter=department_filter)
    else:
        # Fallback mock data
        return generate_fallback_data(limit)

def generate_fallback_data(limit=200):
    """Generate fallback data when service is not available"""
    np.random.seed(42)
    departments = ["Prelitigation", "Litigation", "Discovery", "Settlement", "Trial Prep", "Appeals"]
    
    data = {
        'departments': np.random.choice(departments, limit).tolist(),
        'days_in_stage': np.random.randint(1, 500, limit).tolist(),
        'total_expenses': (np.random.exponential(50000, limit) + 10000).tolist(),
        'active_tasks': np.random.randint(1, 25, limit).tolist(),
        'percent_complete': np.random.uniform(10, 95, limit).tolist(),
        'matter_ids': [f"MTR-2024-{i+1000:04d}" for i in range(limit)],
        'client_names': [f"Client {i+1}" for i in range(limit)],
        'responsible_staff': np.random.choice(
            ["Travis Crawford", "Lisa Litigator", "Amy Assistant", "Paul Prelit", "Nina Assistant", "Omar Ops", "Ivy Intake"], limit
        ).tolist(),
        'hover_text': [f"Matter: MTR-2024-{i+1000:04d}<br>Client: Client {i+1}" for i in range(limit)]
    }
    return data

def build_matter_3d_chart(data, color_by="percent_complete"):
    """Build professional 3D scatter plot for matters"""
    if not data or len(data.get('departments', [])) == 0:
        # Empty state
        fig = go.Figure()
        fig.add_annotation(
            text="No matter data available",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color=COLORS['gray_700'])
        )
        fig.update_layout(
            height=600,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig

    # Professional color scales
    if color_by == "percent_complete":
        colorscale = [
            [0, COLORS['danger']],      # Red for low completion
            [0.5, COLORS['warning']],   # Amber for medium
            [1, COLORS['success']]      # Green for high completion
        ]
        colorbar_title = "Completion %"
        color_data = data['percent_complete']
    elif color_by == "expenses":
        colorscale = "Viridis"
        colorbar_title = "Total Expenses"
        color_data = data['total_expenses']
    else:
        colorscale = "Blues"
        colorbar_title = "Active Tasks"
        color_data = data['active_tasks']

    # Create unique department mapping for x-axis
    unique_depts = list(set(data['departments']))
    dept_mapping = {dept: i for i, dept in enumerate(unique_depts)}
    x_values = [dept_mapping[dept] for dept in data['departments']]

    fig = go.Figure(data=go.Scatter3d(
        x=x_values,
        y=data['days_in_stage'],
        z=data['total_expenses'],
        mode='markers',
        marker=dict(
            size=[max(5, min(20, tasks/2)) for tasks in data['active_tasks']],  # Size by task count
            color=color_data,
            colorscale=colorscale,
            colorbar=dict(
                title=colorbar_title,
                title_font=dict(family="Inter, sans-serif", size=12),
                tickfont=dict(family="Inter, sans-serif", size=10)
            ),
            line=dict(width=0.5, color='rgba(255,255,255,0.8)'),
            opacity=0.8
        ),
        text=data['hover_text'],
        hovertemplate='<b>%{text}</b><br>' +
                     'Days in Stage: %{y}<br>' +
                     'Total Expenses: $%{z:,.0f}<br>' +
                     f'{colorbar_title}: %{{marker.color}}<br>' +
                     '<extra></extra>',
        name='Matters'
    ))

    # Professional layout with corporate styling
    fig.update_layout(
        title=dict(
            text="Matter Performance & Complexity Analysis",
            font=dict(family="Inter, sans-serif", size=20, color=COLORS['primary']),
            x=0.5
        ),
        scene=dict(
            xaxis=dict(
                title="Department",
                title_font=dict(family="Inter, sans-serif", size=14, color=COLORS['gray_700']),
                tickmode='array',
                tickvals=list(range(len(unique_depts))),
                ticktext=unique_depts,
                tickfont=dict(family="Inter, sans-serif", size=10),
                gridcolor='rgba(180,180,180,0.3)'
            ),
            yaxis=dict(
                title="Days in Current Stage",
                title_font=dict(family="Inter, sans-serif", size=14, color=COLORS['gray_700']),
                tickfont=dict(family="Inter, sans-serif", size=10),
                gridcolor='rgba(180,180,180,0.3)'
            ),
            zaxis=dict(
                title="Total Expenses ($)",
                title_font=dict(family="Inter, sans-serif", size=14, color=COLORS['gray_700']),
                tickfont=dict(family="Inter, sans-serif", size=10),
                gridcolor='rgba(180,180,180,0.3)'
            ),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=650,
        margin=dict(l=0, r=0, b=0, t=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif")
    )

    return fig

# Layout with professional styling
def layout():
    return html.Div([
        dmc.Container([
            # Header with consistent styling
            html.Div([
                dmc.Title(
                    "3D Matter Analytics", 
                    order=2, 
                    style={'color': COLORS['primary'], 'fontFamily': 'Inter, sans-serif'}
                ),
                dmc.Text(
                    "Explore matter complexity, progress, and resource allocation in three dimensions",
                    size="sm",
                    style={'color': COLORS['gray_700'], 'marginTop': '0.5rem'}
                )
            ], style={'marginBottom': '1.5rem'}),

            # Controls section
            dmc.Paper([
                dmc.Group([
                    dmc.Select(
                        id="dept-filter-3d",
                        label="Department Filter",
                        placeholder="All Departments",
                        data=[],
                        style={'minWidth': '200px'}
                    ),
                    dmc.Select(
                        id="color-by-3d",
                        label="Color By",
                        value="percent_complete",
                        data=[
                            {"label": "Completion %", "value": "percent_complete"},
                            {"label": "Total Expenses", "value": "expenses"},
                            {"label": "Active Tasks", "value": "tasks"}
                        ],
                        style={'minWidth': '150px'}
                    ),
                    dmc.NumberInput(
                        id="matter-limit-3d",
                        label="Max Matters",
                        value=200,
                        min=50,
                        max=500,
                        step=50,
                        style={'minWidth': '120px'}
                    )
                ], 
                gap="md",
                wrap="wrap"
                )
            ], p="md", shadow="sm", style={'marginBottom': '1rem'}),

            # Chart section
            dmc.Paper([
                dcc.Graph(
                    id="matter-3d-bubble-chart",
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "modeBarButtonsToRemove": ['pan2d', 'lasso2d', 'select2d']
                    },
                    style={"height": "650px"}
                )
            ], p="md", shadow="md", withBorder=True),

            # Info section
            dmc.Paper([
                dmc.Group([
                    dmc.Text("💡 Tip:", fw=600, size="sm"),
                    dmc.Text(
                        "Bubble size represents active task count. Use mouse to rotate and zoom the 3D view.",
                        size="sm",
                        style={'color': COLORS['gray_700']}
                    )
                ])
            ], p="md", style={'marginTop': '1rem', 'backgroundColor': COLORS['gray_300'] + '20'})

        ], size="xl")
    ])

# Callbacks for interactivity
@callback(
    [
        Output("matter-3d-bubble-chart", "figure"),
        Output("dept-filter-3d", "data")
    ],
    [
        Input("dept-filter-3d", "value"),
        Input("color-by-3d", "value"),
        Input("matter-limit-3d", "value")
    ]
)
def update_3d_bubble_chart(department_filter, color_by, limit):
    """Update the 3D bubble chart based on filters"""
    try:
        # Load data with filters
        data = load_matter_3d_data(department_filter=department_filter, limit=limit)
        
        # Get unique departments for filter dropdown
        unique_depts = []
        if data and 'departments' in data:
            unique_depts = [{"label": dept, "value": dept} for dept in sorted(set(data['departments']))]
        
        # Build the chart
        fig = build_matter_3d_chart(data, color_by=color_by)
        
        return fig, unique_depts
        
    except Exception as e:
        print(f"Error updating 3D chart: {e}")
        # Return empty chart on error
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14, color=COLORS['danger'])
        )
        empty_fig.update_layout(height=650, paper_bgcolor="rgba(0,0,0,0)")
        return empty_fig, []
