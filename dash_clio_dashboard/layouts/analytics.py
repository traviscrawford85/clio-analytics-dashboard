"""
Analytics Dashboard Layout - Multi-Dimensional Visualizations
Workload Heatmap with dimension switching capability
"""
from dash import html, dcc, callback, Input, Output
import dash_mantine_components as dmc
import plotly.graph_objects as go

from layouts.mock_multidim_data import (
    get_mock_workload_heatmap,
    get_mock_workload_by_stage,
    get_mock_workload_by_month
)


def get_workload_data(dimension='practice_area'):
    """
    Fetch workload data based on selected dimension
    Args:
        dimension: 'practice_area', 'stage', or 'month'
    Returns:
        dict with attorneys, practice_areas (or other dimension), matrix
    """
    if dimension == 'practice_area':
        return get_mock_workload_heatmap()
    elif dimension == 'stage':
        return get_mock_workload_by_stage()
    elif dimension == 'month':
        return get_mock_workload_by_month()
    else:
        return get_mock_workload_heatmap()


def create_workload_heatmap(data, COLORS):
    """
    Create professional workload heatmap
    Args:
        data: dict with attorneys, practice_areas, matrix
        COLORS: color scheme dict
    Returns:
        Plotly Figure
    """
    # Determine max value for color scale
    max_value = max(max(row) for row in data['matrix'])

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=data['matrix'],
        x=data['practice_areas'],
        y=data['attorneys'],
        colorscale=[
            [0, COLORS['white']],
            [0.2, COLORS['gray_100']],
            [0.4, COLORS['bg_tertiary']],
            [0.6, COLORS['primary_light']],
            [0.8, COLORS['primary']],
            [1.0, '#163152']  # Darker navy for high values
        ],
        text=data['matrix'],
        texttemplate='%{text}',
        textfont=dict(
            size=11,
            family="'Inter', sans-serif",
            color=COLORS['dark']
        ),
        hovertemplate='<b>%{y}</b><br>%{x}<br><b>%{z} active matters</b><extra></extra>',
        colorbar=dict(
            title=dict(
                text='Active<br>Matters',
                side='right',
                font=dict(size=11, family="'Inter', sans-serif")
            ),
            tickfont=dict(size=10),
            thickness=15,
            len=0.7
        ),
        xgap=3,  # Gap between cells
        ygap=3
    ))

    fig.update_layout(
        title=dict(
            text=f'<b>Workload Distribution</b><br><sub>{data.get("dimension", "")}</sub>',
            font=dict(
                size=16,
                family="'Crimson Pro', serif",
                color=COLORS['dark']
            ),
            x=0.02,
            y=0.98,
            xanchor='left',
            yanchor='top'
        ),
        xaxis=dict(
            title='',
            side='bottom',
            tickangle=-45,
            tickfont=dict(size=11, family="'Inter', sans-serif", color=COLORS['gray_700']),
            showgrid=False
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=11, family="'Inter', sans-serif", color=COLORS['gray_700']),
            showgrid=False
        ),
        font=dict(size=11, family="'Inter', sans-serif"),
        height=550,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=120, r=100, t=80, b=100),
        hoverlabel=dict(
            bgcolor=COLORS['dark'],
            font_size=12,
            font_family="'Inter', sans-serif"
        )
    )

    return fig


def create_layout(COLORS=None):
    """
    Create analytics dashboard layout with workload heatmap
    Args:
        COLORS: color scheme dict
    Returns:
        Dash layout
    """
    if COLORS is None:
        # Fallback colors
        COLORS = {
            'dark': '#1A202C',
            'gray_700': '#4A5568',
            'gray_500': '#718096',
            'gray_300': '#CBD5E0',
            'gray_100': '#EDF2F7',
            'white': '#FFFFFF',
            'primary': '#1E3A5F',
            'primary_light': '#2C5282',
            'success': '#276749',
            'bg_tertiary': '#EDF2F7'
        }

    # Get initial data
    initial_data = get_workload_data('practice_area')

    return html.Div([
        # Section Header with Dimension Selector
        html.Div([
            html.Div([
                html.H6("Workload Analytics", style={
                    'fontSize': '1.125rem',
                    'fontWeight': 600,
                    'color': COLORS['dark'],
                    'marginBottom': '0.5rem',
                    'fontFamily': "'Crimson Pro', serif"
                }),
                html.P("Visual scanning of workload distribution across dimensions", style={
                    'fontSize': '0.875rem',
                    'color': COLORS['gray_500'],
                    'marginBottom': 0,
                    'fontFamily': "'Inter', sans-serif"
                })
            ], style={'flex': 1}),

            # Dimension Selector
            html.Div([
                html.Label("View by:", style={
                    'fontSize': '0.8125rem',
                    'fontWeight': 500,
                    'color': COLORS['gray_700'],
                    'marginRight': '0.75rem',
                    'fontFamily': "'Inter', sans-serif"
                }),
                dmc.SegmentedControl(
                    id='dimension-selector',
                    data=[
                        {'label': 'Practice Area', 'value': 'practice_area'},
                        {'label': 'Stage', 'value': 'stage'},
                        {'label': 'Month', 'value': 'month'}
                    ],
                    value='practice_area',
                    color='dark',
                    size='sm',
                    style={'display': 'inline-block'}
                )
            ], style={'display': 'flex', 'alignItems': 'center'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'flex-start',
            'marginBottom': '1.5rem',
            'flexWrap': 'wrap',
            'gap': '1rem'
        }),

        # Heatmap Card
        dmc.Paper([
            html.Div([
                dcc.Graph(
                    id='workload-heatmap',
                    figure=create_workload_heatmap(initial_data, COLORS),
                    config={'displayModeBar': False},
                    className='animated-heatmap'
                )
            ], style={'padding': '1.5rem'})
        ], shadow="xs", radius="md", withBorder=True, style={
            'backgroundColor': COLORS['white'],
            'border': f"1px solid {COLORS['gray_300']}",
            'marginBottom': '2rem'
        }),

        # Insights Section
        html.Div([
            html.H6("Key Insights", style={
                'fontSize': '1rem',
                'fontWeight': 600,
                'color': COLORS['dark'],
                'marginBottom': '1rem',
                'fontFamily': "'Inter', sans-serif"
            }),

            dmc.Grid([
                dmc.GridCol([
                    create_insight_card(
                        "Highest Workload",
                        "Omar Ops",
                        "62 active matters",
                        COLORS['danger'],
                        COLORS
                    )
                ], span=4),

                dmc.GridCol([
                    create_insight_card(
                        "Lowest Workload",
                        "Nina Assistant",
                        "53 active matters",
                        COLORS['success'],
                        COLORS
                    )
                ], span=4),

                dmc.GridCol([
                    create_insight_card(
                        "Average Caseload",
                        "All Attorneys",
                        "57.1 matters",
                        COLORS['primary'],
                        COLORS
                    )
                ], span=4)
            ], gutter="lg")
        ])
    ])


def create_insight_card(label, primary, secondary, accent_color, COLORS):
    """Create a small insight card"""
    return dmc.Paper([
        html.Div([
            html.P(label, style={
                'fontSize': '0.75rem',
                'color': COLORS['gray_500'],
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px',
                'marginBottom': '0.5rem',
                'fontWeight': 500
            }),
            html.H6(primary, style={
                'fontSize': '1.125rem',
                'fontWeight': 600,
                'color': COLORS['dark'],
                'marginBottom': '0.25rem',
                'fontFamily': "'Crimson Pro', serif"
            }),
            html.P(secondary, style={
                'fontSize': '0.875rem',
                'color': accent_color,
                'fontWeight': 500,
                'marginBottom': 0
            })
        ], style={'padding': '1.25rem'})
    ], shadow="xs", radius="md", withBorder=True, style={
        'backgroundColor': COLORS['white'],
        'border': f"1px solid {COLORS['gray_300']}"
    })


# Note: Callback moved to app.py to avoid registration issues
