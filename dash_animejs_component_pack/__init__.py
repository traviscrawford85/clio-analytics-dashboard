"""
Dash Anime.js Component Pack
Animated React components for Dash using Anime.js
"""

import os
import sys
from dash import Dash, _dash_renderer

# Tell Dash about our component library
_dash_renderer._set_react_version('16.14.0')

# Get the path to our JavaScript bundle
_current_path = os.path.dirname(os.path.abspath(__file__))

# Define resource path for Dash to load our JS
_js_dist = [
    {
        'relative_package_path': 'dash_animejs_component_pack.min.js',
        'namespace': 'dash_animejs_component_pack'
    }
]

# Make components available (for now, just placeholder - full integration requires dash-generate-components)
__version__ = '0.1.0'
__all__ = [
    'AnimatedKPI',
    'StageProgressBar',
    'TaskTracker',
    'WorkloadCard',
    'MatterBudget',
    'TaskTimeline',
    'BottleneckRadar',
    'WorkloadMatrix'
]

# Component placeholders - these would be auto-generated in full build
class AnimatedKPI:
    """Animated KPI card with number count-up effect"""
    pass

class StageProgressBar:
    """Animated progress bar for matter lifecycle stages"""
    pass

class TaskTracker:
    """Task list with staggered animations"""
    pass

class WorkloadCard:
    """Staff workload visualization cards"""
    pass

class MatterBudget:
    """Circular budget progress indicators"""
    pass

class TaskTimeline:
    """Mini Gantt-style timeline"""
    pass

class BottleneckRadar:
    """Radar chart for bottleneck visualization"""
    pass

class WorkloadMatrix:
    """Heatmap showing workload distribution"""
    pass
