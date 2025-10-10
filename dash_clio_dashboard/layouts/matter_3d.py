"""
Matter 3D Analytics Layout

Professional 3D matter visualization layout with sophisticated controls and insights.
Integrates with the CFE Solutions dashboard architecture.
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

# Import our services
from ..services.matter_3d_analytics import matter_3d_service

def create_matter_3d_layout():
    """Create the comprehensive 3D matter analytics layout."""
    
    return dmc.Container([
        # Header Section
        dmc.SimpleGrid([
            html.Div([
                dmc.Title(
                    "Matter Complexity & Progress Landscape",
                    order=2,
                    style={
                        "color": "#1E3A5F",
                        "fontFamily": "Inter, sans-serif",
                        "fontWeight": 600,
                        "marginBottom": "8px"
                    }
                ),
                dmc.Text(
                    "Interactive 3D visualization of matter progression, complexity, and resource allocation",
                    size="sm",
                    c="dimmed",
                    style={"fontFamily": "Inter, sans-serif"}
                )
            ]),
            dmc.Group([
                dmc.Button(
                    "Refresh Data",
                    id="refresh-3d-data",
                    variant="light",
                    color="blue",
                    size="sm"
                ),
                dmc.Button(
                    "Export View",
                    id="export-3d-view",
                    variant="outline",
                    color="gray",
                    size="sm"
                )
            ], justify="flex-end")
        ], cols=2, style={"marginBottom": "24px"}),
        
        # Control Panel
        dmc.Paper([
            dmc.SimpleGrid([
                dmc.Select(
                    id="department-filter-3d",
                    label="Department Filter",
                    placeholder="All Departments",
                    data=[
                        {"value": "all", "label": "All Departments"},
                        {"value": "Prelitigation", "label": "Prelitigation"},
                        {"value": "Litigation", "label": "Litigation"},
                        {"value": "Discovery", "label": "Discovery"},
                        {"value": "Settlement", "label": "Settlement"},
                        {"value": "Trial Prep", "label": "Trial Preparation"},
                        {"value": "Appeals", "label": "Appeals"},
                        {"value": "Post-Settlement", "label": "Post-Settlement"}
                    ],
                    value="all",
                    style={"fontFamily": "Inter, sans-serif"}
                ),
                dmc.NumberInput(
                    id="matter-limit-3d",
                    label="Matter Limit",
                    description="Max matters to display",
                    value=200,
                    min=50,
                    max=1000,
                    step=50,
                    style={"fontFamily": "Inter, sans-serif"}
                ),
                dmc.Select(
                    id="time-range-3d",
                    label="Time Range",
                    placeholder="Last 12 months",
                    data=[
                        {"value": "30", "label": "Last 30 days"},
                        {"value": "90", "label": "Last 3 months"},
                        {"value": "180", "label": "Last 6 months"},
                        {"value": "365", "label": "Last 12 months"},
                        {"value": "730", "label": "Last 24 months"}
                    ],
                    value="365",
                    style={"fontFamily": "Inter, sans-serif"}
                ),
                html.Div([
                    dmc.Switch(
                        id="animation-enabled-3d",
                        label="Enable Animations",
                        checked=True,
                        size="sm",
                        color="blue"
                    )
                ], style={"paddingTop": "25px"})
            ], cols=4)
        ], shadow="xs", radius="md", p="md", withBorder=True, style={"marginBottom": "24px"}),
        
        # Main 3D Visualization and Insights
        dmc.SimpleGrid([
            # 3D Chart Column
            html.Div([
                dmc.Paper([
                    dmc.LoadingOverlay([
                        dcc.Graph(
                            id="matter-3d-bubble-chart",
                            config={
                                "displayModeBar": True,
                                "displaylogo": False,
                                "modeBarButtonsToRemove": [
                                    "pan2d", "select2d", "lasso2d", "resetCameraDefault3d",
                                    "resetCameraLastSave3d", "hoverClosestCartesian"
                                ],
                                "toImageButtonOptions": {
                                    "format": "png",
                                    "filename": "matter_3d_landscape",
                                    "height": 650,
                                    "width": 900,
                                    "scale": 2
                                }
                            },
                            style={"height": "650px"}
                        )
                    ],
                        visible=False,
                        overlayProps={"opacity": 0.1},
                        loaderProps={"color": "#1E3A5F", "size": "lg"}
                    )
                ], shadow="sm", radius="md", withBorder=True)
            ]),
            
            # Insights Panel
            html.Div([
                dmc.Stack([
                    # Key Metrics Card
                    dmc.Paper([
                        dmc.Title("Key Insights", order=4, style={"color": "#1E3A5F", "marginBottom": "12px"}),
                        dmc.Stack([
                            dmc.Group([
                                dmc.Text("Total Matters", size="sm", c="dimmed"),
                                dmc.Text("0", id="total-matters-3d", fw=600, c="#1E3A5F")
                            ], justify="space-between"),
                            dmc.Group([
                                dmc.Text("Avg Days/Stage", size="sm", c="dimmed"),
                                dmc.Text("0", id="avg-days-3d", fw=600, c="#1E3A5F")
                            ], justify="space-between"),
                            dmc.Group([
                                dmc.Text("Total Expenses", size="sm", c="dimmed"),
                                dmc.Text("$0", id="total-expenses-3d", fw=600, c="#1E3A5F")
                            ], justify="space-between"),
                            dmc.Group([
                                dmc.Text("Avg Completion", size="sm", c="dimmed"),
                                dmc.Text("0%", id="avg-completion-3d", fw=600, c="#1E3A5F")
                            ], justify="space-between")
                        ], gap="xs")
                    ], shadow="xs", radius="md", p="md", withBorder=True),
                    
                    # Selected Matter Details
                    dmc.Paper([
                        dmc.Title("Selected Matter", order=4, style={"color": "#1E3A5F", "marginBottom": "12px"}),
                        html.Div(
                            dmc.Text(
                                "Click on a bubble to view matter details",
                                size="sm",
                                c="dimmed",
                                style={"textAlign": "center", "padding": "20px"}
                            ),
                            id="selected-matter-details-3d"
                        )
                    ], shadow="xs", radius="md", p="md", withBorder=True),
                    
                    # Department Performance
                    dmc.Paper([
                        dmc.Title("Department Overview", order=4, style={"color": "#1E3A5F", "marginBottom": "12px"}),
                        html.Div(id="department-performance-3d")
                    ], shadow="xs", radius="md", p="md", withBorder=True),
                    
                    # Legend/Help
                    dmc.Paper([
                        dmc.Title("Visualization Guide", order=4, style={"color": "#1E3A5F", "marginBottom": "12px"}),
                        dmc.Stack([
                            dmc.Group([
                                html.Div(style={"width": "12px", "height": "12px", "backgroundColor": "#E53E3E", "borderRadius": "50%"}),
                                dmc.Text("Low completion", size="xs")
                            ], gap="xs"),
                            dmc.Group([
                                html.Div(style={"width": "12px", "height": "12px", "backgroundColor": "#FD8100", "borderRadius": "50%"}),
                                dmc.Text("Moderate progress", size="xs")
                            ], gap="xs"),
                            dmc.Group([
                                html.Div(style={"width": "12px", "height": "12px", "backgroundColor": "#F6E05E", "borderRadius": "50%"}),
                                dmc.Text("Halfway complete", size="xs")
                            ], gap="xs"),
                            dmc.Group([
                                html.Div(style={"width": "12px", "height": "12px", "backgroundColor": "#38B2AC", "borderRadius": "50%"}),
                                dmc.Text("Good progress", size="xs")
                            ], gap="xs"),
                            dmc.Group([
                                html.Div(style={"width": "12px", "height": "12px", "backgroundColor": "#276749", "borderRadius": "50%"}),
                                dmc.Text("Near completion", size="xs")
                            ], gap="xs"),
                            dmc.Divider(size="xs", style={"margin": "8px 0"}),
                            dmc.Text("• Bubble size = Active tasks", size="xs", c="dimmed"),
                            dmc.Text("• X-axis = Department", size="xs", c="dimmed"),
                            dmc.Text("• Y-axis = Days in stage", size="xs", c="dimmed"),
                            dmc.Text("• Z-axis = Total expenses", size="xs", c="dimmed")
                        ], gap="xs")
                    ], shadow="xs", radius="md", p="md", withBorder=True)
                ], gap="md")
            ])
        ], cols={"base": 1, "md": 2}, spacing="md"),
        
        # Data stores for state management
        dcc.Store(id="3d-chart-data", data={}),
        dcc.Store(id="3d-selected-matter", data={}),
        
    ], fluid=True, style={"padding": "24px"})

# Callback to update the 3D chart data
@callback(
    Output("3d-chart-data", "data"),
    Output("matter-3d-bubble-chart", "figure"),
    [
        Input("department-filter-3d", "value"),
        Input("matter-limit-3d", "value"),
        Input("time-range-3d", "value"),
        Input("refresh-3d-data", "n_clicks")
    ],
    [State("animation-enabled-3d", "checked")]
)
def update_3d_chart(department_filter, matter_limit, time_range, refresh_clicks, animation_enabled):
    """Update the 3D bubble chart based on filters."""
    try:
        # Prepare parameters
        dept_filter = None if department_filter == "all" else department_filter
        limit = matter_limit or 200
        days_range = int(time_range) if time_range else 365
        
        # Get data from service
        data = matter_3d_service.get_matter_3d_data(
            limit=limit,
            department_filter=dept_filter,
            date_range_days=days_range
        )
        
        if not data or len(data.get('departments', [])) == 0:
            # Return empty chart
            fig = go.Figure()
            fig.update_layout(
                title="No data available for selected filters",
                height=650,
                font={"family": "Inter, sans-serif", "color": "#1E3A5F"}
            )
            return {}, fig
        
        # Create the 3D scatter plot
        fig = go.Figure(data=go.Scatter3d(
            x=data['departments'],
            y=data['days_in_stage'],
            z=data['total_expenses'],
            text=data['hover_text'],
            hovertemplate='%{text}<extra></extra>',
            mode='markers',
            marker=dict(
                size=data['active_tasks'],
                sizemode='diameter',
                sizeref=max(data['active_tasks']) / 100 if data['active_tasks'] else 1,
                color=data['percent_complete'],
                colorscale=[
                    [0, '#E53E3E'],      # Red for low completion
                    [0.25, '#FD8100'],   # Orange for moderate
                    [0.5, '#F6E05E'],    # Yellow for halfway
                    [0.75, '#38B2AC'],   # Teal for good progress
                    [1, '#276749']       # Success green for completion
                ],
                colorbar=dict(
                    title=dict(
                        text='Completion %',
                        font=dict(family='Inter, sans-serif', size=14, color='#1E3A5F')
                    ),
                    thickness=15,
                    len=0.7,
                    x=1.02,
                    tickfont=dict(family='Inter, sans-serif', size=12, color='#1E3A5F')
                ),
                line=dict(color='#1E3A5F', width=1),
                opacity=0.85
            ),
            name='Matters'
        ))
        
        # Professional layout
        fig.update_layout(
            title=dict(
                text='Matter Complexity & Progress Landscape',
                font=dict(family='Inter, sans-serif', size=20, color='#1E3A5F'),
                x=0.05,
                y=0.95
            ),
            scene=dict(
                xaxis=dict(
                    title=dict(text='Department', font=dict(family='Inter, sans-serif', size=14, color='#1E3A5F')),
                    showgrid=True,
                    gridcolor='#E2E8F0',
                    zeroline=False,
                    tickfont=dict(family='Inter, sans-serif', size=11, color='#4A5568')
                ),
                yaxis=dict(
                    title=dict(text='Days in Current Stage', font=dict(family='Inter, sans-serif', size=14, color='#1E3A5F')),
                    showgrid=True,
                    gridcolor='#E2E8F0',
                    zeroline=False,
                    tickfont=dict(family='Inter, sans-serif', size=11, color='#4A5568')
                ),
                zaxis=dict(
                    title=dict(text='Total Expenses ($)', font=dict(family='Inter, sans-serif', size=14, color='#1E3A5F')),
                    type='log',
                    showgrid=True,
                    gridcolor='#E2E8F0',
                    zeroline=False,
                    tickfont=dict(family='Inter, sans-serif', size=11, color='#4A5568')
                ),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.2),
                    center=dict(x=0, y=0, z=0)
                ),
                bgcolor='rgba(255,255,255,0.95)',
                aspectmode='cube'
            ),
            margin=dict(l=0, r=80, b=0, t=60),
            height=650,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter, sans-serif', color='#1E3A5F'),
            hoverlabel=dict(
                bgcolor='#1E3A5F',
                bordercolor='#2C5282',
                font=dict(family='Inter, sans-serif', size=13, color='white')
            )
        )
        
        return data, fig
        
    except Exception as e:
        print(f"Error updating 3D chart: {e}")
        fig = go.Figure()
        fig.update_layout(
            title="Error loading data",
            height=650,
            font={"family": "Inter, sans-serif", "color": "#1E3A5F"}
        )
        return {}, fig

# Callback to update key metrics
@callback(
    [
        Output("total-matters-3d", "children"),
        Output("avg-days-3d", "children"),
        Output("total-expenses-3d", "children"),
        Output("avg-completion-3d", "children")
    ],
    Input("3d-chart-data", "data")
)
def update_key_metrics(chart_data):
    """Update the key metrics display."""
    if not chart_data or not chart_data.get('departments'):
        return "0", "0", "$0", "0%"
    
    try:
        total_matters = len(chart_data['departments'])
        avg_days = int(np.mean(chart_data['days_in_stage']))
        total_expenses = sum(chart_data['total_expenses'])
        avg_completion = int(np.mean(chart_data['percent_complete']))
        
        return (
            f"{total_matters:,}",
            f"{avg_days}",
            f"${total_expenses:,.0f}",
            f"{avg_completion}%"
        )
    except:
        return "0", "0", "$0", "0%"

# Callback to handle matter selection
@callback(
    Output("selected-matter-details-3d", "children"),
    Input("matter-3d-bubble-chart", "clickData"),
    State("3d-chart-data", "data")
)
def update_selected_matter(click_data, chart_data):
    """Update selected matter details panel."""
    if not click_data or not chart_data:
        return dmc.Text(
            "Click on a bubble to view matter details",
            size="sm",
            c="dimmed",
            style={"textAlign": "center", "padding": "20px"}
        )
    
    try:
        point_index = click_data['points'][0]['pointNumber']
        
        return dmc.Stack([
            dmc.Group([
                dmc.Text("Matter ID:", size="sm", fw=600),
                dmc.Text(chart_data['matter_ids'][point_index], size="sm")
            ], justify="space-between"),
            dmc.Group([
                dmc.Text("Client:", size="sm", fw=600),
                dmc.Text(chart_data['client_names'][point_index], size="sm")
            ], justify="space-between"),
            dmc.Group([
                dmc.Text("Staff:", size="sm", fw=600),
                dmc.Text(chart_data['responsible_staff'][point_index], size="sm")
            ], justify="space-between"),
            dmc.Group([
                dmc.Text("Department:", size="sm", fw=600),
                dmc.Text(chart_data['departments'][point_index], size="sm")
            ], justify="space-between"),
            dmc.Group([
                dmc.Text("Days in Stage:", size="sm", fw=600),
                dmc.Text(f"{chart_data['days_in_stage'][point_index]}", size="sm")
            ], justify="space-between"),
            dmc.Group([
                dmc.Text("Total Expenses:", size="sm", fw=600),
                dmc.Text(f"${chart_data['total_expenses'][point_index]:,.0f}", size="sm")
            ], justify="space-between"),
            dmc.Group([
                dmc.Text("Active Tasks:", size="sm", fw=600),
                dmc.Text(f"{chart_data['active_tasks'][point_index]}", size="sm")
            ], justify="space-between"),
            dmc.Group([
                dmc.Text("Completion:", size="sm", fw=600),
                dmc.Text(f"{chart_data['percent_complete'][point_index]:.1f}%", size="sm")
            ], justify="space-between")
        ], gap="xs")
        
    except Exception as e:
        return dmc.Text(
            "Error loading matter details",
            size="sm",
            c="red",
            style={"textAlign": "center", "padding": "20px"}
        )

# Callback for department performance overview
@callback(
    Output("department-performance-3d", "children"),
    Input("3d-chart-data", "data")
)
def update_department_performance(chart_data):
    """Update department performance overview."""
    if not chart_data or not chart_data.get('departments'):
        return dmc.Text("No data available", size="sm", c="dimmed")
    
    try:
        # Calculate department statistics
        df = pd.DataFrame(chart_data)
        dept_stats = df.groupby('departments').agg({
            'total_expenses': 'sum',
            'days_in_stage': 'mean',
            'percent_complete': 'mean',
            'active_tasks': 'sum'
        }).round(1)
        
        dept_components = []
        for dept, stats in dept_stats.iterrows():
            dept_components.append(
                dmc.Group([
                    dmc.Text(dept, size="xs", fw=600),
                    dmc.Text(f"{stats['percent_complete']:.0f}%", size="xs", c="dimmed")
                ], justify="space-between")
            )
        
        return dmc.Stack(dept_components, gap="xs")
        
    except Exception as e:
        return dmc.Text("Error calculating statistics", size="sm", c="red")