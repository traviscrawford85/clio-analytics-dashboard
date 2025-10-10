"""
Overview Dashboard Layout - Corporate Design
Professional analytics dashboard for legal practice management
"""
import sys
from pathlib import Path

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go

# Add dashboard-neo4j to path for ClioCore access
DASHBOARD_NEO4J_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "dashboard-neo4j"
if str(DASHBOARD_NEO4J_ROOT) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_NEO4J_ROOT))

try:
    from services.dashboard.domains.matter_lifecycle import MatterLifecycle
    from services.dashboard.domains.task_activity import TaskActivity
    CLIOCORE_AVAILABLE = True
except ImportError:
    CLIOCORE_AVAILABLE = False

def get_kpi_data():
    """Fetch KPI data from ClioCore"""
    if not CLIOCORE_AVAILABLE:
        # Return mock data
        return {
            'total_active_matters': 145,
            'avg_days_in_stage': 42,
            'matters_settled_month': 12,
            'bottleneck_percentage': 18,
            'avg_staff_workload': 23
        }

    try:
        matter_lifecycle = MatterLifecycle(backend='sqlite')
        task_activity = TaskActivity(backend='sqlite')

        # Get matters data
        matters_df = matter_lifecycle.get_matters_overview(limit=500)
        total_active = len(matters_df) if not matters_df.empty else 0

        # Calculate metrics
        avg_days = 42  # Placeholder
        matters_settled = 12  # Placeholder
        bottleneck_pct = 18  # Placeholder

        # Avg staff workload
        workload_df = task_activity.get_user_workload()
        if not workload_df.empty and 'active_tasks' in workload_df.columns:
            avg_workload = int(workload_df['active_tasks'].mean())
        else:
            avg_workload = 0

        return {
            'total_active_matters': total_active,
            'avg_days_in_stage': avg_days,
            'matters_settled_month': matters_settled,
            'bottleneck_percentage': bottleneck_pct,
            'avg_staff_workload': avg_workload
        }
    except Exception as e:
        print(f"Error fetching KPI data: {e}")
        return {
            'total_active_matters': 0,
            'avg_days_in_stage': 0,
            'matters_settled_month': 0,
            'bottleneck_percentage': 0,
            'avg_staff_workload': 0
        }

def create_kpi_card(label, value, suffix='', trend=None, COLORS=None):
    """Create a professional KPI card"""
    return dmc.Paper([
        html.Div([
            html.Div([
                html.P(label, style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 500,
                    'color': COLORS['gray_500'],
                    'letterSpacing': '0.3px',
                    'textTransform': 'uppercase',
                    'marginBottom': '0.5rem'
                }),
                html.Div([
                    html.H2(f"{value}", style={
                        'fontSize': '2.25rem',
                        'fontWeight': 600,
                        'color': COLORS['dark'],
                        'marginBottom': 0,
                        'lineHeight': 1,
                        'fontFamily': "'Crimson Pro', serif"
                    }),
                    html.Span(suffix, style={
                        'fontSize': '0.875rem',
                        'color': COLORS['gray_500'],
                        'marginLeft': '0.25rem'
                    }) if suffix else None
                ], style={'display': 'flex', 'alignItems': 'baseline'})
            ])
        ], style={'padding': '1.5rem'})
    ], shadow="xs", radius="md", withBorder=True, style={
        'backgroundColor': COLORS['white'],
        'border': f"1px solid {COLORS['gray_300']}"
    })

def create_layout(COLORS):
    """Create the corporate overview layout"""
    kpi_data = get_kpi_data()

    return html.Div([
        # KPI Cards Grid - Professional spacing with responsive CSS
        html.Div([
            create_kpi_card(
                "Active Matters",
                kpi_data['total_active_matters'],
                COLORS=COLORS
            ),
            create_kpi_card(
                "Avg. Cycle Time",
                kpi_data['avg_days_in_stage'],
                suffix="days",
                COLORS=COLORS
            ),
            create_kpi_card(
                "Resolved (MTD)",
                kpi_data['matters_settled_month'],
                COLORS=COLORS
            ),
            create_kpi_card(
                "Bottleneck Rate",
                kpi_data['bottleneck_percentage'],
                suffix="%",
                COLORS=COLORS
            ),
            create_kpi_card(
                "Avg. Caseload",
                kpi_data['avg_staff_workload'],
                suffix="matters",
                COLORS=COLORS
            ),
        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(5, 1fr)',
            'gap': '1.5rem',
            'marginBottom': '2rem'
        }, className="kpi-grid"),

        # Charts Row - Professional grid
        dmc.Grid([
            dmc.GridCol([
                dmc.Paper([
                    html.Div([
                        html.H6("Practice Area Distribution", style={
                            'fontSize': '0.9375rem',
                            'fontWeight': 600,
                            'color': COLORS['dark'],
                            'marginBottom': '1rem',
                            'fontFamily': "'Inter', sans-serif"
                        }),
                        dcc.Graph(
                            figure=create_practice_area_chart(COLORS),
                            config={'displayModeBar': False},
                            style={'height': '280px'}
                        )
                    ], style={'padding': '1.5rem'})
                ], shadow="xs", radius="md", withBorder=True, style={
                    'backgroundColor': COLORS['white'],
                    'border': f"1px solid {COLORS['gray_300']}"
                })
            ], span=6),

            dmc.GridCol([
                dmc.Paper([
                    html.Div([
                        html.H6("Matter Activity Trend", style={
                            'fontSize': '0.9375rem',
                            'fontWeight': 600,
                            'color': COLORS['dark'],
                            'marginBottom': '1rem',
                            'fontFamily': "'Inter', sans-serif"
                        }),
                        dcc.Graph(
                            figure=create_activity_timeline(COLORS),
                            config={'displayModeBar': False},
                            style={'height': '280px'}
                        )
                    ], style={'padding': '1.5rem'})
                ], shadow="xs", radius="md", withBorder=True, style={
                    'backgroundColor': COLORS['white'],
                    'border': f"1px solid {COLORS['gray_300']}"
                })
            ], span=6)
        ], gutter="lg", style={'marginBottom': '2rem'}),

        # Urgent Tasks Table
        dmc.Paper([
            html.Div([
                html.H6("Priority Actions", style={
                    'fontSize': '0.9375rem',
                    'fontWeight': 600,
                    'color': COLORS['dark'],
                    'marginBottom': '1.25rem',
                    'fontFamily': "'Inter', sans-serif"
                }),
                create_urgent_tasks_table(COLORS)
            ], style={'padding': '1.5rem'})
        ], shadow="xs", radius="md", withBorder=True, style={
            'backgroundColor': COLORS['white'],
            'border': f"1px solid {COLORS['gray_300']}"
        })
    ])

def create_practice_area_chart(COLORS):
    """Create professional practice area distribution chart"""
    if not CLIOCORE_AVAILABLE:
        data = {
            'Practice Area': ['Auto Accident', 'Medical Malpractice', 'Workers Comp', 'Premises Liability'],
            'Count': [45, 32, 28, 40]
        }
    else:
        try:
            matter_lifecycle = MatterLifecycle(backend='sqlite')
            matters_df = matter_lifecycle.get_matters_overview(limit=500)
            if not matters_df.empty and 'practice_area_name' in matters_df.columns:
                pa_counts = matters_df['practice_area_name'].value_counts().reset_index()
                pa_counts.columns = ['Practice Area', 'Count']
                data = pa_counts.head(6).to_dict('list')
            else:
                data = {'Practice Area': [], 'Count': []}
        except:
            data = {'Practice Area': [], 'Count': []}

    fig = go.Figure()

    # Professional bar chart with minimal styling
    fig.add_trace(go.Bar(
        x=data['Practice Area'],
        y=data['Count'],
        marker_color=COLORS['primary'],
        marker_line_color=COLORS['primary_light'],
        marker_line_width=0,
        opacity=0.85,
        hovertemplate='<b>%{x}</b><br>%{y} matters<extra></extra>'
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=60),
        height=280,
        xaxis=dict(
            showgrid=False,
            tickangle=-30,
            tickfont=dict(size=11, color=COLORS['gray_700'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS['gray_300'],
            gridwidth=1,
            tickfont=dict(size=11, color=COLORS['gray_700'])
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor=COLORS['dark'],
            font_size=12,
            font_family="'Inter', sans-serif"
        )
    )
    return fig

def create_activity_timeline(COLORS):
    """Create professional activity timeline"""
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
    values = [20, 25, 22, 28, 30, 27, 25, 23, 26, 29, 31, 28, 27, 30, 32, 29, 27, 26, 28, 30, 31, 29, 27, 28, 30, 32, 31, 29, 28, 30]

    fig = go.Figure()

    # Minimal, professional line chart
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines',
        name='Matters Processed',
        line=dict(color=COLORS['primary'], width=2.5),
        fill='tozeroy',
        fillcolor=f"rgba(30, 58, 95, 0.08)",
        hovertemplate='<b>%{x|%b %d}</b><br>%{y} matters<extra></extra>'
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=10, b=40),
        height=280,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=11, color=COLORS['gray_700'])
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS['gray_300'],
            gridwidth=1,
            tickfont=dict(size=11, color=COLORS['gray_700']),
            zeroline=False
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor=COLORS['dark'],
            font_size=12,
            font_family="'Inter', sans-serif"
        )
    )
    return fig

def create_urgent_tasks_table(COLORS):
    """Create professional urgent tasks table using Mantine DataTable"""
    if not CLIOCORE_AVAILABLE:
        tasks = [
            {'task': 'File motion for summary judgment', 'matter': 'Smith v. Jones Auto Accident', 'due': '2 days', 'assignee': 'Paul Prelit'},
            {'task': 'Client deposition prep', 'matter': 'Williams Medical Malpractice', 'due': '5 days', 'assignee': 'Lisa Litigator'},
            {'task': 'Discovery response deadline', 'matter': 'Brown v. Corporation', 'due': 'OVERDUE', 'assignee': 'Travis Crawford'},
            {'task': 'Settlement negotiation call', 'matter': 'Davis Workers Comp', 'due': '1 day', 'assignee': 'Amy Assistant'},
        ]
    else:
        try:
            task_activity = TaskActivity(backend='sqlite')
            urgency_df = task_activity.get_tasks_by_urgency()
            if not urgency_df.empty:
                tasks = []
                for _, row in urgency_df.head(5).iterrows():
                    tasks.append({
                        'task': row.get('task_name', 'Unknown'),
                        'matter': row.get('matter_description', 'Unknown'),
                        'due': row.get('urgency_category', 'N/A'),
                        'assignee': row.get('assignee_name', 'Unassigned')
                    })
            else:
                tasks = []
        except:
            tasks = []

    if not tasks:
        return html.P("No priority actions at this time", style={
            'color': COLORS['gray_500'],
            'textAlign': 'center',
            'padding': '2rem 0',
            'fontSize': '0.875rem'
        })

    # Professional table with Mantine-style design
    return dmc.Table([
        html.Thead([
            html.Tr([
                html.Th("Task", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem'
                }),
                html.Th("Matter", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem'
                }),
                html.Th("Due", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem',
                    'textAlign': 'center'
                }),
                html.Th("Assignee", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem'
                })
            ], style={'backgroundColor': COLORS['bg_tertiary']})
        ]),
        html.Tbody([
            html.Tr([
                html.Td(task['task'], style={
                    'fontWeight': 500,
                    'color': COLORS['dark'],
                    'fontSize': '0.875rem',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                }),
                html.Td(task['matter'], style={
                    'color': COLORS['gray_700'],
                    'fontSize': '0.875rem',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                }),
                html.Td([
                    dmc.Badge(
                        task['due'],
                        color="red" if 'OVERDUE' in task['due'].upper() else "yellow" if 'day' in task['due'].lower() and int(task['due'].split()[0]) <= 3 else "gray",
                        variant="filled" if 'OVERDUE' in task['due'].upper() else "light",
                        size="sm"
                    )
                ], style={
                    'textAlign': 'center',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                }),
                html.Td(task['assignee'], style={
                    'color': COLORS['gray_700'],
                    'fontSize': '0.875rem',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                })
            ], style={
                'transition': 'background-color 0.15s ease',
                '_hover': {'backgroundColor': COLORS['bg_tertiary']}
            }) for task in tasks
        ])
    ], striped=False, highlightOnHover=True, withTableBorder=False, withColumnBorders=False, style={
        'width': '100%'
    })
