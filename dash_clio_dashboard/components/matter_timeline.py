"""
Matter Timeline Component - Professional Implementation
Shows matter lifecycle progression with timeline visualization
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dash import dcc, html, Input, Output, callback
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go

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

def generate_timeline_data(department_filter=None, limit=50):
    """Generate realistic timeline data for matter lifecycle visualization"""
    np.random.seed(42)
    
    # Department and stage definitions
    departments = ["Prelitigation", "Litigation", "Discovery", "Settlement", "Trial Prep", "Appeals"]
    stages = ["Initial Review", "Investigation", "Filing", "Discovery", "Mediation", "Trial Prep", "Settlement", "Closed"]
    staff_names = ["Travis Crawford", "Lisa Litigator", "Amy Assistant", "Paul Prelit", "Nina Assistant", "Omar Ops", "Ivy Intake"]
    
    # Filter departments if specified
    if department_filter:
        departments = [department_filter] if department_filter in departments else departments
    
    matters = []
    base_date = datetime.now() - timedelta(days=365*2)  # Start 2 years ago
    
    for i in range(limit):
        matter_id = f"MTR-{2023 + i//100}-{i+1001:04d}"
        client_name = f"Client {chr(65 + i%26)}{i//26 + 1}"
        department = np.random.choice(departments)
        responsible_staff = np.random.choice(staff_names)
        
        # Generate realistic timeline progression
        start_date = base_date + timedelta(days=np.random.randint(0, 600))
        
        # Create stages with realistic durations
        current_date = start_date
        matter_stages = []
        
        # Determine how many stages this matter will go through
        num_stages = np.random.choice([3, 4, 5, 6, 7], p=[0.1, 0.2, 0.3, 0.3, 0.1])
        selected_stages = stages[:num_stages]
        
        for j, stage in enumerate(selected_stages):
            # Stage duration varies by type
            if stage in ["Initial Review", "Filing"]:
                duration_days = np.random.randint(5, 30)
            elif stage in ["Investigation", "Discovery"]:
                duration_days = np.random.randint(30, 120)
            elif stage in ["Mediation", "Settlement"]:
                duration_days = np.random.randint(15, 60)
            elif stage in ["Trial Prep"]:
                duration_days = np.random.randint(60, 180)
            else:
                duration_days = np.random.randint(10, 45)
            
            stage_end = current_date + timedelta(days=duration_days)
            
            # Calculate completion percentage
            if j == len(selected_stages) - 1:
                # Last stage
                completion = 100 if stage == "Closed" else np.random.randint(60, 95)
            else:
                completion = 100  # Completed stages are 100%
            
            matter_stages.append({
                'matter_id': matter_id,
                'client_name': client_name,
                'department': department,
                'responsible_staff': responsible_staff,
                'stage_name': stage,
                'start_date': current_date,
                'end_date': stage_end,
                'completion_pct': completion,
                'is_current': j == len(selected_stages) - 1 and completion < 100,
                'stage_order': j + 1,
                'total_stages': len(selected_stages)
            })
            
            current_date = stage_end + timedelta(days=np.random.randint(1, 7))  # Small gap between stages
        
        matters.extend(matter_stages)
    
    return pd.DataFrame(matters)

def build_matter_timeline_chart(df, view_type="gantt"):
    """Build professional timeline visualization"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No timeline data available",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color=COLORS['gray_700'])
        )
        fig.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig

    if view_type == "gantt":
        # Create Gantt chart showing matter progression
        fig = px.timeline(
            df,
            x_start="start_date",
            x_end="end_date",
            y="matter_id",
            color="stage_name",
            title="Matter Lifecycle Timeline",
            hover_data={
                "client_name": True,
                "department": True,
                "responsible_staff": True,
                "completion_pct": True,
                "stage_order": True,
                "total_stages": True
            },
            color_discrete_map={
                "Initial Review": COLORS['primary_light'],
                "Investigation": COLORS['warning'],
                "Filing": COLORS['primary'],
                "Discovery": "#8E4EC6",
                "Mediation": COLORS['success'],
                "Trial Prep": "#E03131",
                "Settlement": "#37B24D",
                "Closed": COLORS['gray_700']
            }
        )

        # Update hover template
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>" +
                         "Stage: %{color}<br>" +
                         "Client: %{customdata[0]}<br>" +
                         "Department: %{customdata[1]}<br>" +
                         "Staff: %{customdata[2]}<br>" +
                         "Completion: %{customdata[3]}%<br>" +
                         "Stage %{customdata[4]} of %{customdata[5]}<br>" +
                         "Duration: %{x}<br>" +
                         "<extra></extra>"
        )

        # Professional styling
        fig.update_layout(
            title=dict(
                text="Matter Lifecycle Timeline",
                font=dict(family="Inter, sans-serif", size=20, color=COLORS['primary']),
                x=0.5
            ),
            xaxis_title="Timeline",
            yaxis_title="Matter ID",
            height=600,
            margin=dict(l=100, r=50, t=60, b=50),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif"),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Reverse y-axis to show most recent at top
        fig.update_yaxes(autorange="reversed")

    else:  # stage_distribution
        # Create stage distribution chart
        stage_counts = df.groupby('stage_name').size().reset_index(name='count')
        
        fig = px.bar(
            stage_counts,
            x='stage_name',
            y='count',
            title="Matter Distribution by Stage",
            color='count',
            color_continuous_scale=[[0, COLORS['primary_light']], [1, COLORS['primary']]]
        )
        
        fig.update_layout(
            title=dict(
                text="Matter Distribution by Stage",
                font=dict(family="Inter, sans-serif", size=20, color=COLORS['primary']),
                x=0.5
            ),
            xaxis_title="Stage",
            yaxis_title="Number of Matters",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif"),
            showlegend=False
        )

    return fig

# Professional layout
def layout():
    return html.Div([
        dmc.Container([
            # Header section
            html.Div([
                dmc.Title(
                    "Matter Timeline Analytics", 
                    order=2, 
                    style={'color': COLORS['primary'], 'fontFamily': 'Inter, sans-serif'}
                ),
                dmc.Text(
                    "Track matter progression through lifecycle stages and identify workflow patterns",
                    size="sm",
                    style={'color': COLORS['gray_700'], 'marginTop': '0.5rem'}
                )
            ], style={'marginBottom': '1.5rem'}),

            # Controls section
            dmc.Paper([
                dmc.Group([
                    dmc.Select(
                        id="timeline-dept-filter",
                        label="Department Filter",
                        placeholder="All Departments",
                        data=[],
                        style={'minWidth': '200px'}
                    ),
                    dmc.Select(
                        id="timeline-staff-filter",
                        label="Staff Filter",
                        placeholder="All Staff",
                        data=[],
                        style={'minWidth': '200px'}
                    ),
                    dmc.Select(
                        id="timeline-view-type",
                        label="View Type",
                        value="gantt",
                        data=[
                            {"label": "Timeline (Gantt)", "value": "gantt"},
                            {"label": "Stage Distribution", "value": "stage_distribution"}
                        ],
                        style={'minWidth': '180px'}
                    ),
                    dmc.NumberInput(
                        id="timeline-matter-limit",
                        label="Max Matters",
                        value=50,
                        min=10,
                        max=100,
                        step=10,
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
                    id="matter-timeline-chart",
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "modeBarButtonsToRemove": ['pan2d', 'lasso2d', 'select2d']
                    },
                    style={"height": "600px"}
                )
            ], p="md", shadow="md", withBorder=True),

            # Statistics section
            html.Div(id="timeline-stats", style={'marginTop': '1rem'})

        ], size="xl")
    ])

# Callbacks for interactivity
@callback(
    [
        Output("matter-timeline-chart", "figure"),
        Output("timeline-dept-filter", "data"),
        Output("timeline-staff-filter", "data"),
        Output("timeline-stats", "children")
    ],
    [
        Input("timeline-dept-filter", "value"),
        Input("timeline-staff-filter", "value"),
        Input("timeline-view-type", "value"),
        Input("timeline-matter-limit", "value")
    ]
)
def update_timeline_chart(department_filter, staff_filter, view_type, limit):
    """Update the timeline chart based on filters"""
    try:
        # Generate timeline data
        df = generate_timeline_data(department_filter=department_filter, limit=limit)
        
        # Apply staff filter if specified
        if staff_filter:
            df = df[df['responsible_staff'] == staff_filter]
        
        # Get unique values for filter dropdowns
        unique_depts = [{"label": dept, "value": dept} for dept in sorted(df['department'].unique())]
        unique_staff = [{"label": staff, "value": staff} for staff in sorted(df['responsible_staff'].unique())]
        
        # Build the chart
        fig = build_matter_timeline_chart(df, view_type=view_type)
        
        # Create statistics
        stats = create_timeline_stats(df)
        
        return fig, unique_depts, unique_staff, stats
        
    except Exception as e:
        print(f"Error updating timeline chart: {e}")
        # Return empty chart on error
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text=f"Error loading timeline data: {str(e)}",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14, color=COLORS['danger'])
        )
        empty_fig.update_layout(height=600, paper_bgcolor="rgba(0,0,0,0)")
        return empty_fig, [], [], html.Div()

def create_timeline_stats(df):
    """Create statistics cards for the timeline view"""
    if df.empty:
        return html.Div()
    
    # Calculate key metrics
    total_matters = df['matter_id'].nunique()
    avg_completion = df['completion_pct'].mean()
    current_matters = df[df['is_current'] == True]['matter_id'].nunique()
    closed_matters = len(df[df['stage_name'] == 'Closed'])
    
    return dmc.Group([
        dmc.Paper([
            dmc.Text("Total Matters", size="xs", style={'color': COLORS['gray_700']}),
            dmc.Title(str(total_matters), order=3, style={'color': COLORS['primary']})
        ], p="md", shadow="sm", style={'textAlign': 'center', 'minWidth': '120px'}),
        
        dmc.Paper([
            dmc.Text("Avg Completion", size="xs", style={'color': COLORS['gray_700']}),
            dmc.Title(f"{avg_completion:.1f}%", order=3, style={'color': COLORS['success']})
        ], p="md", shadow="sm", style={'textAlign': 'center', 'minWidth': '120px'}),
        
        dmc.Paper([
            dmc.Text("Active Matters", size="xs", style={'color': COLORS['gray_700']}),
            dmc.Title(str(current_matters), order=3, style={'color': COLORS['warning']})
        ], p="md", shadow="sm", style={'textAlign': 'center', 'minWidth': '120px'}),
        
        dmc.Paper([
            dmc.Text("Closed Matters", size="xs", style={'color': COLORS['gray_700']}),
            dmc.Title(str(closed_matters), order=3, style={'color': COLORS['gray_700']})
        ], p="md", shadow="sm", style={'textAlign': 'center', 'minWidth': '120px'})
    ], gap="md")
