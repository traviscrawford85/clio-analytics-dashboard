"""
Clio KPI Dashboard - Main Application
Corporate legal analytics dashboard with professional design
"""
import os
import sys
from pathlib import Path

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# Add current directory to path for local imports
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Add dashboard-neo4j to path for ClioCore access
DASHBOARD_NEO4J_ROOT = Path(__file__).resolve().parent.parent.parent / "dashboard-neo4j"
if str(DASHBOARD_NEO4J_ROOT) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_NEO4J_ROOT))

# Import ClioCore domain services
try:
    from services.dashboard.domains.matter_lifecycle import MatterLifecycle
    from services.dashboard.domains.task_activity import TaskActivity
    CLIOCORE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: ClioCore not available: {e}")
    CLIOCORE_AVAILABLE = False

# Initialize Dash app with professional fonts
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Pro:wght@400;600;700&display=swap"
    ],
    suppress_callback_exceptions=True,
    title="Clio Legal Analytics | CFE Solutions"
)

# Corporate color scheme for legal/professional dashboard
COLORS = {
    # Primary - Professional Navy/Blue
    'primary': '#1E3A5F',        # Deep navy blue for headers
    'primary_light': '#2C5282',  # Lighter navy for accents

    # Neutrals - Sophisticated grays
    'dark': '#1A202C',           # Almost black for text
    'gray_900': '#2D3748',       # Dark gray
    'gray_700': '#4A5568',       # Medium dark gray
    'gray_500': '#718096',       # Medium gray
    'gray_300': '#CBD5E0',       # Light gray
    'gray_100': '#EDF2F7',       # Very light gray
    'white': '#FFFFFF',

    # Accents - Minimal, professional
    'success': '#276749',        # Dark green (subdued)
    'warning': '#975A16',        # Dark amber (professional)
    'danger': '#9B2C2C',         # Dark red (serious)
    'info': '#2C5282',           # Navy blue

    # Backgrounds
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F7FAFC',
    'bg_tertiary': '#EDF2F7'
}

# Helper function to create sidebar navigation items
def create_nav_item(item_id, label, icon, active_tab):
    """Create a sidebar navigation item"""
    is_active = item_id == active_tab

    return html.Div([
        html.Div([
            html.Span(icon, style={
                'fontSize': '1.25rem',
                'marginRight': '0.75rem'
            }),
            html.Span(label, style={
                'fontSize': '0.9375rem',
                'fontWeight': 500 if is_active else 400,
                'fontFamily': "'Inter', sans-serif"
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'padding': '0.875rem 1.5rem',
            'color': COLORS['white'] if is_active else COLORS['gray_700'],
            'backgroundColor': COLORS['primary'] if is_active else 'transparent',
            'borderRadius': '0.5rem',
            'margin': '0.25rem 1rem',
            'transition': 'all 0.2s ease',
            'cursor': 'pointer'
        }, className=f'nav-item {"active" if is_active else ""}')
    ], id=f'nav-{item_id}', n_clicks=0, style={
        'display': 'block'
    })

# App layout with colored header and sidebar navigation
app.layout = dmc.MantineProvider(html.Div([
    # Navy blue header with white text
    html.Div([
        html.Div([
            html.Div([
                html.H1("Clio Legal Analytics", style={
                    'color': COLORS['white'],
                    'fontFamily': "'Crimson Pro', serif",
                    'fontWeight': 600,
                    'fontSize': '1.75rem',
                    'marginBottom': '0.25rem',
                    'letterSpacing': '-0.5px'
                }),
                html.P("Practice Management Intelligence", style={
                    'color': 'rgba(255, 255, 255, 0.8)',
                    'fontSize': '0.8125rem',
                    'fontWeight': 400,
                    'marginBottom': 0,
                    'fontFamily': "'Inter', sans-serif"
                })
            ], style={'flex': 1}),
            html.Div([
                html.Span("CFE SOLUTIONS", style={
                    'color': 'rgba(255, 255, 255, 0.7)',
                    'fontSize': '0.6875rem',
                    'fontWeight': 700,
                    'letterSpacing': '2px'
                })
            ], style={'textAlign': 'right', 'paddingTop': '0.5rem'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'padding': '1.25rem 2rem',
            'maxWidth': '100%'
        })
    ], style={
        'backgroundColor': COLORS['primary'],
        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
        'position': 'sticky',
        'top': 0,
        'zIndex': 1000
    }),

    # Main layout: Sidebar + Content
    html.Div([
        # Left Sidebar Navigation
        html.Div([
            html.Div([
                # Navigation items
                create_nav_item("overview", "Overview", "📊", "overview"),
                create_nav_item("lifecycle", "Lifecycle", "🔄", "overview"),
                create_nav_item("department", "Department", "👥", "overview"),
                create_nav_item("matter3d", "3D Matter View", "🧊", "overview"),
                create_nav_item("matter-bubble", "3D Matter Bubble", "🫧", "overview"),
                create_nav_item("matter-timeline", "Matter Timeline", "⏰", "overview"),
                create_nav_item("bottlenecks", "Bottlenecks", "⚠️", "overview"),
                create_nav_item("analytics", "Analytics", "📈", "overview"),
            ], id='sidebar-nav', style={'padding': '1.5rem 0'}),

            # Sidebar footer
            html.Div([
                html.Div([
                    html.Span("Powered by ", style={'fontSize': '0.6875rem', 'color': COLORS['gray_500']}),
                    html.Span("ClioCore", style={'fontSize': '0.6875rem', 'color': COLORS['primary'], 'fontWeight': 600}),
                ], style={'textAlign': 'center', 'paddingBottom': '1rem'})
            ], style={
                'position': 'absolute',
                'bottom': 0,
                'left': 0,
                'right': 0,
                'borderTop': f"1px solid {COLORS['gray_300']}",
                'backgroundColor': COLORS['white'],
                'padding': '1rem'
            })
        ], id='sidebar', style={
            'width': '240px',
            'height': 'calc(100vh - 80px)',
            'backgroundColor': COLORS['white'],
            'borderRight': f"1px solid {COLORS['gray_300']}",
            'position': 'fixed',
            'left': 0,
            'top': '80px',
            'overflowY': 'auto',
            'boxShadow': '2px 0 8px rgba(0, 0, 0, 0.04)'
        }),

        # Main content area
        html.Div([
            # Auto-refresh interval
            dcc.Interval(
                id='interval-component',
                interval=30*1000,  # Update every 30 seconds
                n_intervals=0
            ),

            # Hidden input to track active tab
            dcc.Store(id='dashboard-tabs', data='overview'),

            # Content placeholder
            html.Div(id='dashboard-content', style={'padding': '2rem'})
        ], style={
            'marginLeft': '240px',
            'backgroundColor': COLORS['bg_secondary'],
            'minHeight': 'calc(100vh - 80px)',
            'transition': 'margin-left 0.3s ease'
        })
    ], style={'position': 'relative'})
], style={
    'fontFamily': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'backgroundColor': COLORS['bg_secondary'],
    'minHeight': '100vh'
}))



# Initialize domain services
def get_domain_services():
    """Get ClioCore domain service instances"""
    if not CLIOCORE_AVAILABLE:
        return None, None
    try:
        matter_lifecycle = MatterLifecycle(backend='sqlite')
        task_activity = TaskActivity(backend='sqlite')
        return matter_lifecycle, task_activity
    except Exception as e:
        print(f"Error initializing domain services: {e}")
        return None, None

# Tab content callback (using dcc.Store for state)
from dash.dependencies import Input, Output, State
from dash import ctx

@app.callback(
    [Output('dashboard-content', 'children'),
     Output('dashboard-tabs', 'data'),
     Output('sidebar-nav', 'children')],
    [Input('nav-overview', 'n_clicks'),
     Input('nav-lifecycle', 'n_clicks'),
     Input('nav-department', 'n_clicks'),
     Input('nav-matter3d', 'n_clicks'),
     Input('nav-matter-bubble', 'n_clicks'),
     Input('nav-matter-timeline', 'n_clicks'),
     Input('nav-bottlenecks', 'n_clicks'),
     Input('nav-analytics', 'n_clicks'),
     Input('interval-component', 'n_intervals')],
    [State('dashboard-tabs', 'data')],
    prevent_initial_call=False
)
def render_tab_content(n1, n2, n3, n4, n5, n6, n7, n8, n_intervals, current_tab):
    """Render content based on active tab and update sidebar"""
    # Determine which nav item was clicked
    triggered_id = ctx.triggered_id if ctx.triggered_id else None

    # Map nav item IDs to tab names
    if triggered_id:
        if 'nav-overview' in str(triggered_id):
            active_tab = 'overview'
        elif 'nav-lifecycle' in str(triggered_id):
            active_tab = 'lifecycle'
        elif 'nav-department' in str(triggered_id):
            active_tab = 'department'
        elif 'nav-matter3d' in str(triggered_id):
            active_tab = 'matter3d'
        elif 'nav-matter-bubble' in str(triggered_id):
            active_tab = 'matter-bubble'
        elif 'nav-matter-timeline' in str(triggered_id):
            active_tab = 'matter-timeline'
        elif 'nav-bottlenecks' in str(triggered_id):
            active_tab = 'bottlenecks'
        elif 'nav-analytics' in str(triggered_id):
            active_tab = 'analytics'
        else:
            active_tab = current_tab if current_tab else 'overview'
    else:
        active_tab = current_tab if current_tab else 'overview'

    # Update sidebar nav items
    sidebar_nav = [
        create_nav_item("overview", "Overview", "📊", active_tab),
        create_nav_item("lifecycle", "Lifecycle", "🔄", active_tab),
        create_nav_item("department", "Department", "👥", active_tab),
        create_nav_item("matter3d", "3D Matter View", "🧊", active_tab),
        create_nav_item("matter-bubble", "3D Matter Bubble", "🫧", active_tab),
        create_nav_item("matter-timeline", "Matter Timeline", "⏰", active_tab),
        create_nav_item("bottlenecks", "Bottlenecks", "⚠️", active_tab),
        create_nav_item("analytics", "Analytics", "📈", active_tab),
    ]

    try:
        if active_tab == "overview":
            from layouts import overview
            return overview.create_layout(COLORS), active_tab, sidebar_nav
        elif active_tab == "lifecycle":
            from layouts import lifecycle
            return lifecycle.create_layout(COLORS), active_tab, sidebar_nav
        elif active_tab == "department":
            from layouts import department
            return department.create_layout(COLORS), active_tab, sidebar_nav
        elif active_tab == "matter3d":
            from layouts import matter_3d
            return matter_3d.create_matter_3d_layout(), active_tab, sidebar_nav
        elif active_tab == "matter-bubble":
            from components.matter_3_d_bubble import layout
            return layout(), active_tab, sidebar_nav
        elif active_tab == "matter-timeline":
            from components.matter_timeline import layout
            return layout(), active_tab, sidebar_nav
        elif active_tab == "bottlenecks":
            from layouts import bottlenecks
            return bottlenecks.create_layout(COLORS), active_tab, sidebar_nav
        elif active_tab == "analytics":
            from layouts import analytics
            return analytics.create_layout(COLORS), active_tab, sidebar_nav
        else:
            return html.Div("Invalid tab selection"), active_tab, sidebar_nav
    except Exception as e:
        return html.Div([
            html.H4("Error Loading Dashboard", style={'color': COLORS['danger']}),
            html.P(f"Error: {str(e)}", style={'fontFamily': 'monospace'}),
            html.P("The dashboard is running in standalone mode. ClioCore integration is not available.",
                   style={'color': COLORS['gray_500']})
        ], style={'padding': '40px', 'textAlign': 'center'}), active_tab, sidebar_nav

# Analytics heatmap dimension selector callback
@app.callback(
    Output('workload-heatmap', 'figure'),
    Input('dimension-selector', 'value'),
    prevent_initial_call=True
)
def update_heatmap_dimension(dimension):
    """Update heatmap when dimension selector changes"""
    try:
        from layouts.analytics import get_workload_data, create_workload_heatmap
        data = get_workload_data(dimension)
        return create_workload_heatmap(data, COLORS)
    except Exception as e:
        print(f"Error updating heatmap: {e}")
        # Return empty figure on error
        import plotly.graph_objects as go
        return go.Figure()

# Health check endpoint
@app.server.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    status = {
        'status': 'healthy',
        'cliocore_available': CLIOCORE_AVAILABLE
    }
    return status, 200

if __name__ == '__main__':
    # Get port from environment or default to 8050
    port = int(os.environ.get('DASH_PORT', 8050))
    debug = os.environ.get('DASH_DEBUG', 'False').lower() == 'true'

    print(f"\n{'='*60}")
    print(f"🏛️  Clio Legal Analytics Dashboard")
    print(f"{'='*60}")
    print(f"📍 URL: http://localhost:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print(f"🔌 ClioCore: {'✅ Connected' if CLIOCORE_AVAILABLE else '❌ Not Available'}")
    print(f"{'='*60}\n")

    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port
    )
