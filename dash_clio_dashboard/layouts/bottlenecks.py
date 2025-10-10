"""
Bottlenecks Dashboard Layout
Identifies process bottlenecks and stuck matters/tasks
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
    from services.dashboard.domains.task_activity import TaskActivity
    CLIOCORE_AVAILABLE = True
except ImportError:
    CLIOCORE_AVAILABLE = False

def get_bottleneck_data():
    """Fetch bottleneck analysis data"""
    if not CLIOCORE_AVAILABLE:
        return {
            'stages': ['Investigation', 'Negotiation', 'Litigation', 'Settlement', 'Documentation', 'Closing'],
            'stuck_counts': [8, 15, 12, 5, 3, 2],
            'avg_stuck_days': [95, 120, 150, 85, 60, 45]
        }

    try:
        matter_lifecycle = MatterLifecycle(backend='sqlite')
        # Would need custom query for "stuck" matters (>90 days in stage)
        # For now, return placeholder
        return {
            'stages': ['Investigation', 'Negotiation', 'Litigation'],
            'stuck_counts': [8, 15, 12],
            'avg_stuck_days': [95, 120, 150]
        }
    except Exception as e:
        print(f"Error fetching bottleneck data: {e}")
        return {'stages': [], 'stuck_counts': [], 'avg_stuck_days': []}

def create_layout(COLORS=None):
    """Create bottlenecks dashboard layout"""
    bottleneck_data = get_bottleneck_data()

    return html.Div([
        # Header
        html.H3("🚦 Bottleneck Analysis", className="mb-4", style={
            'fontWeight': 700,
            'color': '#111827'
        }),

        # Alert Summary
        dbc.Row([
            dbc.Col([
                create_bottleneck_alert_card(
                    "Critical Bottlenecks",
                    len([c for c in bottleneck_data['stuck_counts'] if c > 10]),
                    "#DC2626"
                )
            ], width=12, md=3),
            dbc.Col([
                create_bottleneck_alert_card(
                    "Stuck Matters",
                    sum(bottleneck_data['stuck_counts']) if bottleneck_data['stuck_counts'] else 0,
                    "#F59E0B"
                )
            ], width=12, md=3),
            dbc.Col([
                create_bottleneck_alert_card(
                    "Avg. Stuck Duration",
                    f"{int(sum(bottleneck_data['avg_stuck_days'])/len(bottleneck_data['avg_stuck_days']))}d" if bottleneck_data['avg_stuck_days'] else "0d",
                    "#0070E0",
                    is_duration=True
                )
            ], width=12, md=3),
            dbc.Col([
                create_bottleneck_alert_card(
                    "Overdue Tasks",
                    23,  # Placeholder
                    "#DC2626"
                )
            ], width=12, md=3)
        ], className="mb-4 g-3"),

        # Bottleneck Visualization
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📊 Stuck Matters by Stage", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_bottleneck_bar_chart(bottleneck_data),
                            config={'displayModeBar': False}
                        )
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12, lg=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("🔥 Priority Matrix", className="mb-0")),
                    dbc.CardBody([
                        create_priority_matrix(bottleneck_data)
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12, lg=6)
        ], className="mb-4"),

        # Time in Stage Analysis (Full Width)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⏱️ Average Time Stuck per Stage", className="mb-0")),
                    dbc.CardBody([
                        dcc.Graph(
                            figure=create_duration_chart(bottleneck_data),
                            config={'displayModeBar': False}
                        )
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12)
        ], className="mb-4"),

        # Stuck Matters Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⚠️ Matters Requiring Attention (>90 Days in Stage)", className="mb-0")),
                    dbc.CardBody([
                        create_stuck_matters_table()
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12)
        ], className="mb-4"),

        # Action Items
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("✅ Recommended Actions", className="mb-0")),
                    dbc.CardBody([
                        create_action_items()
                    ])
                ], style={'borderRadius': '12px', 'border': '1px solid #E5E7EB'})
            ], width=12)
        ])
    ])

def create_bottleneck_alert_card(label, value, color, is_duration=False):
    """Create bottleneck alert card"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.P(label, className="text-uppercase mb-2", style={
                    'fontSize': '0.75rem',
                    'fontWeight': 600,
                    'color': '#6B7280',
                    'letterSpacing': '0.5px'
                }),
                html.H3(str(value), className="mb-0", style={
                    'fontSize': '2rem',
                    'fontWeight': 700,
                    'color': color
                })
            ])
        ])
    ], style={
        'borderRadius': '12px',
        'border': f'2px solid {color}',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.04)'
    })

def create_bottleneck_bar_chart(bottleneck_data):
    """Create horizontal bar chart showing stuck matters by stage"""
    if not bottleneck_data['stages']:
        return go.Figure()

    fig = go.Figure()

    # Sort by count descending to show biggest bottlenecks first
    sorted_data = sorted(
        zip(bottleneck_data['stages'], bottleneck_data['stuck_counts'], bottleneck_data['avg_stuck_days']),
        key=lambda x: x[1],
        reverse=True
    )
    stages, counts, days = zip(*sorted_data) if sorted_data else ([], [], [])

    # Color code by severity
    colors = ['#DC2626' if count > 10 else '#F59E0B' if count > 5 else '#10B981'
              for count in counts]

    fig.add_trace(go.Bar(
        y=stages,
        x=counts,
        orientation='h',
        marker_color=colors,
        text=[f"<b>{count}</b> matters" for count in counts],
        textposition='inside',
        textfont=dict(color='white', size=12),
        hovertemplate='<b>%{y}</b><br>%{x} matters stuck<br>Avg: %{customdata} days<extra></extra>',
        customdata=days
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
        xaxis=dict(
            title="Number of Stuck Matters (>90 days)",
            showgrid=True,
            gridcolor='#E5E7EB',
            zeroline=False
        ),
        yaxis=dict(showgrid=False),
        showlegend=False
    )

    return fig

def create_priority_matrix(bottleneck_data):
    """Create visual priority matrix showing urgency"""
    if not bottleneck_data['stages']:
        return html.Div("No data available", className="text-center text-muted py-4")

    # Categorize stages by count and duration
    items = []
    for stage, count, days in zip(
        bottleneck_data['stages'],
        bottleneck_data['stuck_counts'],
        bottleneck_data['avg_stuck_days']
    ):
        # Determine priority
        if count > 10 and days > 120:
            priority = "🔴 Critical"
            bg_color = "#FEE2E2"
            border_color = "#DC2626"
            text_color = "#991B1B"
        elif count > 5 and days > 90:
            priority = "🟠 High"
            bg_color = "#FEF3C7"
            border_color = "#F59E0B"
            text_color = "#92400E"
        elif count > 3:
            priority = "🟡 Medium"
            bg_color = "#FEF9C3"
            border_color = "#EAB308"
            text_color = "#854D0E"
        else:
            priority = "🟢 Low"
            bg_color = "#D1FAE5"
            border_color = "#10B981"
            text_color = "#065F46"

        items.append({
            'stage': stage,
            'count': count,
            'days': days,
            'priority': priority,
            'bg_color': bg_color,
            'border_color': border_color,
            'text_color': text_color
        })

    # Sort by priority (critical first)
    priority_order = {"🔴 Critical": 0, "🟠 High": 1, "🟡 Medium": 2, "🟢 Low": 3}
    items.sort(key=lambda x: priority_order.get(x['priority'], 4))

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Span(item['priority'], style={
                        'fontSize': '0.875rem',
                        'fontWeight': 700,
                        'color': item['text_color']
                    }),
                    html.H6(item['stage'], className="mb-1 mt-2", style={
                        'fontSize': '1rem',
                        'fontWeight': 600,
                        'color': '#111827'
                    }),
                    html.Div([
                        html.Span(f"{item['count']} matters", style={
                            'fontSize': '1.25rem',
                            'fontWeight': 700,
                            'color': item['text_color'],
                            'marginRight': '12px'
                        }),
                        html.Span(f"| {item['days']} days avg", style={
                            'fontSize': '0.875rem',
                            'color': '#6B7280'
                        })
                    ])
                ], style={
                    'padding': '16px',
                    'backgroundColor': item['bg_color'],
                    'borderRadius': '8px',
                    'border': f"2px solid {item['border_color']}",
                    'marginBottom': '12px'
                })
            ]) for item in items
        ], style={'maxHeight': '320px', 'overflowY': 'auto'}),

        # Legend
        html.Div([
            html.Div("Priority Guide:", style={
                'fontSize': '0.75rem',
                'fontWeight': 600,
                'color': '#6B7280',
                'marginBottom': '8px',
                'marginTop': '12px'
            }),
            html.Div([
                html.Span("🔴 Critical: ", style={'fontWeight': 600, 'fontSize': '0.75rem'}),
                html.Span(">10 matters, >120 days | ", style={'fontSize': '0.75rem', 'color': '#6B7280'}),
                html.Span("🟠 High: ", style={'fontWeight': 600, 'fontSize': '0.75rem'}),
                html.Span(">5 matters, >90 days", style={'fontSize': '0.75rem', 'color': '#6B7280'})
            ])
        ], style={
            'padding': '12px',
            'backgroundColor': '#F9FAFB',
            'borderRadius': '6px',
            'borderTop': '1px solid #E5E7EB'
        })
    ])

def create_duration_chart(bottleneck_data):
    """Create bar chart showing average stuck duration"""
    if not bottleneck_data['stages']:
        return go.Figure()

    fig = go.Figure()

    colors = ['#DC2626' if days > 120 else '#F59E0B' if days > 90 else '#10B981'
              for days in bottleneck_data['avg_stuck_days']]

    fig.add_trace(go.Bar(
        x=bottleneck_data['stages'],
        y=bottleneck_data['avg_stuck_days'],
        marker_color=colors,
        text=[f"{d}d" for d in bottleneck_data['avg_stuck_days']],
        textposition='outside'
    ))

    # Add threshold line at 90 days
    fig.add_hline(y=90, line_dash="dash", line_color="#F59E0B",
                  annotation_text="90-day threshold", annotation_position="right")

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=20, b=80),
        height=400,
        xaxis=dict(showgrid=False, tickangle=-45),
        yaxis=dict(title="Average Days Stuck", showgrid=True, gridcolor='#E5E7EB'),
        showlegend=False
    )

    return fig

def create_stuck_matters_table():
    """Create table of matters stuck in stages"""
    if not CLIOCORE_AVAILABLE:
        # Mock data
        matters = [
            {'matter': 'Smith v. Jones Auto Accident', 'stage': 'Litigation', 'days': 156, 'practice_area': 'Auto Accident', 'responsible': 'Jane Doe'},
            {'matter': 'Williams Medical Malpractice', 'stage': 'Negotiation', 'days': 142, 'practice_area': 'Med Mal', 'responsible': 'John Smith'},
            {'matter': 'Brown Workers Comp', 'stage': 'Investigation', 'days': 98, 'practice_area': 'Workers Comp', 'responsible': 'Alice Johnson'},
        ]
    else:
        # Would query actual stuck matters
        matters = []

    if not matters:
        return html.P("No stuck matters detected", className="text-success text-center py-4")

    return dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Matter"),
                html.Th("Current Stage"),
                html.Th("Days in Stage", style={'textAlign': 'center'}),
                html.Th("Practice Area"),
                html.Th("Responsible")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(matter['matter'], style={'fontWeight': 500}),
                html.Td(matter['stage']),
                html.Td(
                    html.Div([
                        html.Span(matter['days'], style={
                            'fontWeight': 700,
                            'color': '#DC2626' if matter['days'] > 120 else '#F59E0B'
                        }),
                        html.Span(' days', style={'fontSize': '0.75rem', 'color': '#6B7280'})
                    ]),
                    style={'textAlign': 'center'}
                ),
                html.Td(matter['practice_area']),
                html.Td(matter['responsible'])
            ], style={
                'backgroundColor': '#FEE2E2' if matter['days'] > 120 else '#FEF3C7'
            }) for matter in matters
        ])
    ], bordered=True, hover=True, responsive=True, style={'fontSize': '0.875rem'})

def create_action_items():
    """Create action items/recommendations list"""
    actions = [
        {
            'priority': 'High',
            'action': 'Review 3 matters stuck in Litigation stage for >150 days',
            'owner': 'Senior Attorney',
            'color': '#DC2626'
        },
        {
            'priority': 'High',
            'action': 'Investigate 15 matters in Negotiation stage (avg 120 days)',
            'owner': 'Case Managers',
            'color': '#DC2626'
        },
        {
            'priority': 'Medium',
            'action': 'Expedite investigation for 8 matters >95 days in Investigation',
            'owner': 'Investigators',
            'color': '#F59E0B'
        },
        {
            'priority': 'Low',
            'action': 'Review Settlement stage process for optimization opportunities',
            'owner': 'Operations Manager',
            'color': '#10B981'
        }
    ]

    return html.Div([
        html.Div([
            html.Div([
                html.Div(
                    action['priority'],
                    style={
                        'padding': '4px 12px',
                        'borderRadius': '12px',
                        'fontSize': '0.75rem',
                        'fontWeight': 700,
                        'color': 'white',
                        'backgroundColor': action['color'],
                        'width': 'fit-content'
                    }
                ),
                html.Div([
                    html.Div(action['action'], style={
                        'fontWeight': 600,
                        'fontSize': '0.9375rem',
                        'color': '#111827',
                        'marginBottom': '4px'
                    }),
                    html.Div(f"Owner: {action['owner']}", style={
                        'fontSize': '0.8125rem',
                        'color': '#6B7280'
                    })
                ], style={'marginTop': '8px'})
            ], style={
                'padding': '16px',
                'backgroundColor': '#F9FAFB',
                'borderRadius': '8px',
                'marginBottom': '12px',
                'border': '1px solid #E5E7EB'
            })
        ]) for action in actions
    ])
