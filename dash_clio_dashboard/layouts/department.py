"""
Department Dashboard Layout - Corporate Design
Shows department metrics and staff workload
"""
import sys
from pathlib import Path

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.graph_objects as go

# Add dashboard-neo4j to path
DASHBOARD_NEO4J_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "dashboard-neo4j"
if str(DASHBOARD_NEO4J_ROOT) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_NEO4J_ROOT))

try:
    from services.dashboard.domains.task_activity import TaskActivity
    from services.dashboard.domains.matter_lifecycle import MatterLifecycle
    CLIOCORE_AVAILABLE = True
except ImportError:
    CLIOCORE_AVAILABLE = False

def get_department_metrics():
    """Fetch department-level metrics"""
    if not CLIOCORE_AVAILABLE:
        return {
            'intake': {'active': 42, 'avg_days': 8, 'completed_mtd': 15},
            'prelitigation': {'active': 67, 'avg_days': 35, 'completed_mtd': 12},
            'litigation': {'active': 36, 'avg_days': 120, 'completed_mtd': 5}
        }

    try:
        matter_lifecycle = MatterLifecycle(backend='sqlite')
        # Get matters by department/stage
        # This would need custom queries - using mock for now
        return {
            'intake': {'active': 42, 'avg_days': 8, 'completed_mtd': 15},
            'prelitigation': {'active': 67, 'avg_days': 35, 'completed_mtd': 12},
            'litigation': {'active': 36, 'avg_days': 120, 'completed_mtd': 5}
        }
    except:
        return {
            'intake': {'active': 0, 'avg_days': 0, 'completed_mtd': 0},
            'prelitigation': {'active': 0, 'avg_days': 0, 'completed_mtd': 0},
            'litigation': {'active': 0, 'avg_days': 0, 'completed_mtd': 0}
        }

def get_workload_data():
    """Fetch team workload data"""
    if not CLIOCORE_AVAILABLE:
        return {
            'users': ['Travis Crawford', 'Lisa Litigator', 'Amy Assistant', 'Paul Prelit', 'Nina Assistant'],
            'active_tasks': [18, 23, 15, 20, 12],
            'overdue_tasks': [2, 5, 1, 3, 0],
            'completion_rate': [95, 82, 98, 88, 100],
            'total_completed': [145, 198, 132, 167, 89]
        }

    try:
        task_activity = TaskActivity(backend='sqlite')
        workload_df = task_activity.get_user_workload()

        if not workload_df.empty:
            return {
                'users': workload_df['user_name'].tolist()[:10],
                'active_tasks': workload_df.get('active_tasks', [0]*len(workload_df)).tolist()[:10],
                'overdue_tasks': workload_df.get('overdue_tasks', [0]*len(workload_df)).tolist()[:10],
                'completion_rate': [85] * len(workload_df[:10]),
                'total_completed': workload_df.get('completed_on_time', [0]*len(workload_df)).tolist()[:10]
            }
        else:
            return {'users': [], 'active_tasks': [], 'overdue_tasks': [], 'completion_rate': [], 'total_completed': []}
    except Exception as e:
        print(f"Error fetching workload data: {e}")
        return {'users': [], 'active_tasks': [], 'overdue_tasks': [], 'completion_rate': [], 'total_completed': []}

def create_department_card(name, metrics, color, COLORS):
    """Create a department metrics card"""
    return dmc.Paper([
        html.Div([
            html.Div([
                html.H6(name, style={
                    'fontSize': '0.9375rem',
                    'fontWeight': 600,
                    'color': COLORS['dark'],
                    'marginBottom': '1rem',
                    'fontFamily': "'Inter', sans-serif"
                }),
                # Metrics row
                html.Div([
                    # Active matters
                    html.Div([
                        html.Div("Active", style={
                            'fontSize': '0.75rem',
                            'color': COLORS['gray_500'],
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.3px',
                            'marginBottom': '0.25rem'
                        }),
                        html.Div(str(metrics['active']), style={
                            'fontSize': '1.75rem',
                            'fontWeight': 600,
                            'color': color,
                            'fontFamily': "'Crimson Pro', serif"
                        })
                    ], style={'flex': 1}),

                    # Avg days
                    html.Div([
                        html.Div("Avg Days", style={
                            'fontSize': '0.75rem',
                            'color': COLORS['gray_500'],
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.3px',
                            'marginBottom': '0.25rem'
                        }),
                        html.Div(f"{metrics['avg_days']}d", style={
                            'fontSize': '1.25rem',
                            'fontWeight': 500,
                            'color': COLORS['gray_700']
                        })
                    ], style={'flex': 1}),

                    # Completed MTD
                    html.Div([
                        html.Div("Resolved MTD", style={
                            'fontSize': '0.75rem',
                            'color': COLORS['gray_500'],
                            'textTransform': 'uppercase',
                            'letterSpacing': '0.3px',
                            'marginBottom': '0.25rem'
                        }),
                        html.Div(str(metrics['completed_mtd']), style={
                            'fontSize': '1.25rem',
                            'fontWeight': 500,
                            'color': COLORS['success']
                        })
                    ], style={'flex': 1})
                ], style={'display': 'flex', 'gap': '1.5rem'})
            ])
        ], style={'padding': '1.5rem'})
    ], shadow="xs", radius="md", withBorder=True, style={
        'backgroundColor': COLORS['white'],
        'border': f"1px solid {COLORS['gray_300']}"
    })

def create_layout(COLORS=None):
    """Create department dashboard layout"""
    if COLORS is None:
        # Fallback colors if not provided
        COLORS = {
            'dark': '#1A202C',
            'gray_700': '#4A5568',
            'gray_500': '#718096',
            'gray_300': '#CBD5E0',
            'white': '#FFFFFF',
            'primary': '#1E3A5F',
            'success': '#276749',
            'bg_tertiary': '#EDF2F7'
        }

    dept_metrics = get_department_metrics()
    workload_data = get_workload_data()

    return html.Div([
        # Department Metrics Section
        html.Div([
            html.H6("Department Overview", style={
                'fontSize': '1rem',
                'fontWeight': 600,
                'color': COLORS['dark'],
                'marginBottom': '1.25rem',
                'fontFamily': "'Inter', sans-serif"
            }),

            # Department cards grid
            html.Div([
                create_department_card("Intake", dept_metrics['intake'], COLORS['primary'], COLORS),
                create_department_card("Prelitigation", dept_metrics['prelitigation'], '#2C5282', COLORS),
                create_department_card("Litigation", dept_metrics['litigation'], '#4A5568', COLORS),
            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(3, 1fr)',
                'gap': '1.5rem',
                'marginBottom': '2rem'
            }, className="dept-grid")
        ]),

        # Staff Workload Section
        html.Div([
            html.H6("Staff Workload", style={
                'fontSize': '1rem',
                'fontWeight': 600,
                'color': COLORS['dark'],
                'marginBottom': '1.25rem',
                'fontFamily': "'Inter', sans-serif"
            }),

            dmc.Paper([
                html.Div([
                    create_workload_table(workload_data, COLORS)
                ], style={'padding': '1.5rem'})
            ], shadow="xs", radius="md", withBorder=True, style={
                'backgroundColor': COLORS['white'],
                'border': f"1px solid {COLORS['gray_300']}"
            })
        ])
    ])

def create_workload_table(workload_data, COLORS):
    """Create professional workload table"""
    if not workload_data['users']:
        return html.P("No workload data available", style={
            'color': COLORS['gray_500'],
            'textAlign': 'center',
            'padding': '2rem 0',
            'fontSize': '0.875rem'
        })

    return dmc.Table([
        html.Thead([
            html.Tr([
                html.Th("Attorney", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem'
                }),
                html.Th("Active", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem',
                    'textAlign': 'center'
                }),
                html.Th("Overdue", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem',
                    'textAlign': 'center'
                }),
                html.Th("On-Time %", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem',
                    'textAlign': 'center'
                }),
                html.Th("Completed", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 600,
                    'color': COLORS['gray_700'],
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.5px',
                    'borderBottom': f"2px solid {COLORS['gray_300']}",
                    'padding': '0.75rem',
                    'textAlign': 'center'
                })
            ], style={'backgroundColor': COLORS['bg_tertiary']})
        ]),
        html.Tbody([
            html.Tr([
                html.Td(user, style={
                    'fontWeight': 500,
                    'color': COLORS['dark'],
                    'fontSize': '0.875rem',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                }),
                html.Td(active, style={
                    'textAlign': 'center',
                    'color': COLORS['gray_700'],
                    'fontSize': '0.875rem',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                }),
                html.Td([
                    dmc.Badge(
                        str(overdue),
                        color="red" if overdue > 3 else "yellow" if overdue > 0 else "gray",
                        variant="filled" if overdue > 3 else "light",
                        size="sm"
                    )
                ], style={
                    'textAlign': 'center',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                }),
                html.Td(f"{rate}%", style={
                    'textAlign': 'center',
                    'color': COLORS['success'] if rate >= 90 else COLORS['gray_700'],
                    'fontWeight': 500 if rate >= 90 else 400,
                    'fontSize': '0.875rem',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                }),
                html.Td(completed, style={
                    'textAlign': 'center',
                    'color': COLORS['gray_700'],
                    'fontSize': '0.875rem',
                    'padding': '1rem 0.75rem',
                    'borderBottom': f"1px solid {COLORS['gray_300']}"
                })
            ]) for user, active, overdue, rate, completed in zip(
                workload_data['users'],
                workload_data['active_tasks'],
                workload_data['overdue_tasks'],
                workload_data['completion_rate'],
                workload_data['total_completed']
            )
        ])
    ], striped=False, highlightOnHover=True, withTableBorder=False, withColumnBorders=False, style={
        'width': '100%'
    })
