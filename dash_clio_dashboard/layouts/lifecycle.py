"""
Lifecycle Dashboard Layout
Visualizes matter progression through workflow stages
"""
import sys
from pathlib import Path

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Add dashboard-neo4j to path
DASHBOARD_NEO4J_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "dashboard-neo4j"
if str(DASHBOARD_NEO4J_ROOT) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_NEO4J_ROOT))

try:
    from services.dashboard.domains.matter_lifecycle import MatterLifecycle
    CLIOCORE_AVAILABLE = True
except ImportError:
    CLIOCORE_AVAILABLE = False

COLORS = ['#0070E0', '#04304C', '#87CEEB', '#018b76', '#D74417', '#F4A540', '#CBEA00', '#6B7280']

def get_stage_data():
    """Fetch stage distribution data"""
    if not CLIOCORE_AVAILABLE:
        return {
            'stages': ['Client Onboarding', 'Investigation', 'Negotiation', 'Litigation', 'Settlement', 'Closed'],
            'counts': [15, 32, 28, 18, 12, 5],
            'avg_days': [7, 45, 62, 120, 30, 0]
        }

    try:
        matter_lifecycle = MatterLifecycle(backend='sqlite')
        stage_dist = matter_lifecycle.get_stage_distribution()

        if not stage_dist.empty:
            stages = stage_dist['stage_name'].tolist()
            counts = stage_dist['matters_count'].tolist()
            # avg_days would need additional computation
            avg_days = [0] * len(stages)

            return {
                'stages': stages,
                'counts': counts,
                'avg_days': avg_days
            }
        else:
            return {'stages': [], 'counts': [], 'avg_days': []}
    except Exception as e:
        print(f"Error fetching stage data: {e}")
        return {'stages': [], 'counts': [], 'avg_days': []}

def create_layout(COLORS=None):
    """Create lifecycle visualization layout"""
    stage_data = get_stage_data()

    return html.Div([
        # Header
        html.H3("🔄 Matter Lifecycle", className="mb-4", style={
            'fontWeight': 700,
            'color': '#111827'
        }),

        # Stage Progress Bar (placeholder for React component)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📊 Matter Distribution by Stage", className="mb-0")),
                    dbc.CardBody([
                        create_stage_progress_bar(stage_data)
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12)
        ], className="mb-4"),

        # Stage Metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⏱️ Average Days per Stage", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_stage_duration_chart(stage_data),
                            config={'displayModeBar': False}
                        )
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12, lg=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📈 Stage Flow Visualization", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_sankey_chart(stage_data),
                            config={'displayModeBar': False}
                        )
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12, lg=6)
        ], className="mb-4"),

        # Practice Area Breakdown
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🧭 Stage Distribution by Practice Area", className="mb-0")),
                    dbc.CardBody([
                        create_practice_area_stage_table()
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12)
        ])
    ])

def create_stage_progress_bar(stage_data):
    """Create horizontal stage progress bar"""
    if not stage_data['stages']:
        return html.P("No stage data available", className="text-muted text-center py-4")

    total = sum(stage_data['counts'])
    if total == 0:
        return html.P("No matters in stages", className="text-muted text-center py-4")

    # Stage labels
    labels = html.Div([
        html.Div([
            html.Div(stage, style={
                'textAlign': 'center',
                'flex': count / total,
                'fontSize': '0.75rem',
                'fontWeight': 600,
                'color': '#374151'
            })
            for stage, count in zip(stage_data['stages'], stage_data['counts'])
        ], style={'display': 'flex', 'marginBottom': '8px'})
    ])

    # Progress bar
    progress_bar = html.Div([
        html.Div([
            html.Div(
                f"{count}",
                style={
                    'width': f"{(count/total)*100}%",
                    'height': '48px',
                    'backgroundColor': COLORS[idx % len(COLORS)],
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'color': 'white',
                    'fontWeight': 600,
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease'
                },
                className="stage-segment"
            )
            for idx, (stage, count) in enumerate(zip(stage_data['stages'], stage_data['counts']))
        ], style={
            'display': 'flex',
            'borderRadius': '12px',
            'overflow': 'hidden',
            'boxShadow': '0 4px 12px rgba(0,0,0,0.08)'
        })
    ])

    return html.Div([labels, progress_bar])

def create_stage_duration_chart(stage_data):
    """Create bar chart showing average days per stage"""
    if not stage_data['stages']:
        return go.Figure()

    # Mock data for avg days (would come from database in production)
    avg_days = [7, 45, 62, 120, 30, 5] if not stage_data['avg_days'] or all(d == 0 for d in stage_data['avg_days']) else stage_data['avg_days']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=stage_data['stages'][:len(avg_days)],
        y=avg_days,
        marker=dict(
            color=avg_days,
            colorscale=[
                [0, '#10B981'],
                [0.5, '#F59E0B'],
                [1, '#DC2626']
            ],
            colorbar=dict(title="Days")
        ),
        text=[f"{d}d" for d in avg_days],
        textposition='outside'
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=20, b=80),
        height=300,
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(title="Average Days", showgrid=True, gridcolor='#E5E7EB'),
        showlegend=False
    )
    return fig

def create_sankey_chart(stage_data):
    """Create Sankey diagram showing matter flow between stages"""
    if not stage_data['stages'] or len(stage_data['stages']) < 2:
        return go.Figure()

    # Build flow data
    source = []
    target = []
    value = []

    for i in range(len(stage_data['stages']) - 1):
        source.append(i)
        target.append(i + 1)
        # Flow decreases as matters progress
        flow_value = max(1, stage_data['counts'][i] - stage_data['counts'][i+1])
        value.append(flow_value)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="white", width=2),
            label=stage_data['stages'],
            color=[COLORS[i % len(COLORS)] for i in range(len(stage_data['stages']))]
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color='rgba(0, 112, 224, 0.3)'
        )
    )])

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_practice_area_stage_table():
    """Create table showing stage breakdown by practice area"""
    if not CLIOCORE_AVAILABLE:
        # Mock data
        data = [
            {'Practice Area': 'Auto Accident', 'Investigation': 12, 'Negotiation': 15, 'Litigation': 8, 'Settlement': 5},
            {'Practice Area': 'Medical Malpractice', 'Investigation': 8, 'Negotiation': 10, 'Litigation': 12, 'Settlement': 3},
            {'Practice Area': 'Workers Comp', 'Investigation': 10, 'Negotiation': 8, 'Litigation': 5, 'Settlement': 4}
        ]
    else:
        # Would query actual data
        data = []

    if not data:
        return html.P("No data available", className="text-muted text-center py-4")

    return dbc.Table([
        html.Thead([
            html.Tr([html.Th("Practice Area")] + [html.Th("Investigation"), html.Th("Negotiation"), html.Th("Litigation"), html.Th("Settlement")])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(row['Practice Area'], style={'fontWeight': 600}),
                html.Td(row['Investigation'], style={'textAlign': 'center'}),
                html.Td(row['Negotiation'], style={'textAlign': 'center'}),
                html.Td(row['Litigation'], style={'textAlign': 'center'}),
                html.Td(row['Settlement'], style={'textAlign': 'center'})
            ]) for row in data
        ])
    ], bordered=True, hover=True, responsive=True, style={'fontSize': '0.875rem'})
