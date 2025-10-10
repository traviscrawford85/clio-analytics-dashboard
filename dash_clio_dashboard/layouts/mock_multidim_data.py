"""
Mock Multi-Dimensional Data for Advanced Visualizations
This will be replaced with Clio API data using clio_automation_toolkit
"""
import pandas as pd
import numpy as np

# ============================================
# WORKLOAD HEATMAP DATA
# ============================================

def get_mock_workload_heatmap():
    """
    Attorney × Practice Area workload matrix
    Returns: dict with attorneys, practice_areas, matrix (2D array)
    """
    attorneys = [
        'Travis Crawford',
        'Lisa Litigator',
        'Amy Assistant',
        'Paul Prelit',
        'Nina Assistant',
        'Omar Ops',
        'Ivy Intake'
    ]

    practice_areas = [
        'Auto Accident',
        'Medical Malpractice',
        'Workers Comp',
        'Premises Liability',
        'Product Liability',
        'Wrongful Death'
    ]

    # Generate realistic workload matrix (active matters per attorney/practice area)
    np.random.seed(42)  # Reproducible
    matrix = [
        [18, 12, 5, 8, 3, 2],   # Travis Crawford
        [23, 8, 15, 6, 4, 1],   # Lisa Litigator
        [15, 20, 3, 12, 6, 4],  # Amy Assistant
        [20, 5, 18, 9, 2, 3],   # Paul Prelit
        [12, 15, 8, 5, 8, 5],   # Nina Assistant
        [8, 18, 12, 15, 3, 6],  # Omar Ops
        [16, 10, 6, 8, 12, 8]   # Ivy Intake
    ]

    return {
        'attorneys': attorneys,
        'practice_areas': practice_areas,
        'matrix': matrix,
        'dimension': 'Attorney × Practice Area'
    }


def get_mock_workload_by_stage():
    """
    Attorney × Stage workload matrix
    Returns: dict with attorneys, stages, matrix (2D array)
    """
    attorneys = [
        'Travis Crawford',
        'Lisa Litigator',
        'Amy Assistant',
        'Paul Prelit',
        'Nina Assistant',
        'Omar Ops',
        'Ivy Intake'
    ]

    stages = [
        'Intake',
        'Investigation',
        'Prelitigation',
        'Litigation',
        'Settlement',
        'Closed'
    ]

    # Workload by stage
    matrix = [
        [8, 12, 15, 8, 5, 0],    # Travis Crawford
        [12, 18, 10, 8, 9, 0],   # Lisa Litigator
        [5, 10, 20, 15, 10, 0],  # Amy Assistant
        [10, 15, 12, 10, 10, 0], # Paul Prelit
        [6, 8, 15, 12, 12, 0],   # Nina Assistant
        [15, 12, 10, 8, 17, 0],  # Omar Ops
        [8, 10, 18, 12, 12, 0]   # Ivy Intake
    ]

    return {
        'attorneys': attorneys,
        'practice_areas': stages,  # Reuse same key for consistency
        'matrix': matrix,
        'dimension': 'Attorney × Stage'
    }


def get_mock_workload_by_month():
    """
    Attorney × Month workload matrix (trailing 6 months)
    Returns: dict with attorneys, months, matrix (2D array)
    """
    attorneys = [
        'Travis Crawford',
        'Lisa Litigator',
        'Amy Assistant',
        'Paul Prelit',
        'Nina Assistant',
        'Omar Ops',
        'Ivy Intake'
    ]

    months = [
        'Sep 2025',
        'Aug 2025',
        'Jul 2025',
        'Jun 2025',
        'May 2025',
        'Apr 2025'
    ]

    # Workload trend over time
    matrix = [
        [48, 50, 52, 48, 45, 42],  # Travis Crawford
        [57, 55, 58, 60, 62, 55],  # Lisa Litigator
        [60, 62, 58, 55, 53, 50],  # Amy Assistant
        [57, 55, 57, 59, 57, 55],  # Paul Prelit
        [53, 55, 52, 50, 48, 45],  # Nina Assistant
        [62, 60, 62, 65, 63, 60],  # Omar Ops
        [60, 58, 60, 62, 60, 58]   # Ivy Intake
    ]

    return {
        'attorneys': attorneys,
        'practice_areas': months,  # Reuse same key for consistency
        'matrix': matrix,
        'dimension': 'Attorney × Month'
    }


# ============================================
# TIMELINE (GANTT) DATA
# ============================================

def get_mock_timeline_data():
    """
    Matter timeline data for Gantt chart
    Returns: list of dicts with matter details
    """
    import datetime

    base_date = datetime.date(2025, 1, 1)

    matters = [
        {
            'matter_id': 'M001',
            'matter_name': 'Smith v. Jones Auto Accident',
            'start': '2025-01-15',
            'end': '2025-03-20',
            'stage': 'Prelitigation',
            'status': 'active',
            'attorney': 'Paul Prelit',
            'practice_area': 'Auto Accident'
        },
        {
            'matter_id': 'M002',
            'matter_name': 'Williams Medical Malpractice',
            'start': '2024-12-01',
            'end': '2025-05-15',
            'stage': 'Litigation',
            'status': 'active',
            'attorney': 'Lisa Litigator',
            'practice_area': 'Medical Malpractice'
        },
        {
            'matter_id': 'M003',
            'matter_name': 'Brown Workers Comp',
            'start': '2025-02-10',
            'end': '2025-04-30',
            'stage': 'Prelitigation',
            'status': 'active',
            'attorney': 'Paul Prelit',
            'practice_area': 'Workers Comp'
        },
        {
            'matter_id': 'M004',
            'matter_name': 'Davis v. Corporation',
            'start': '2025-01-05',
            'end': '2025-06-20',
            'stage': 'Litigation',
            'status': 'overdue',
            'attorney': 'Lisa Litigator',
            'practice_area': 'Premises Liability'
        },
        {
            'matter_id': 'M005',
            'matter_name': 'Martinez Product Liability',
            'start': '2024-11-20',
            'end': '2025-02-28',
            'stage': 'Settlement',
            'status': 'active',
            'attorney': 'Travis Crawford',
            'practice_area': 'Product Liability'
        },
        # Add more matters...
    ]

    return matters


# ============================================
# SANKEY (FLOW) DATA
# ============================================

def get_mock_sankey_flow():
    """
    Department flow data for Sankey diagram
    Returns: dict with source, target, value, labels
    """
    return {
        'labels': ['Intake', 'Investigation', 'Prelitigation', 'Litigation', 'Settlement', 'Trial', 'Resolved', 'Dismissed'],
        'source': [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5],  # Indices of source nodes
        'target': [1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 6],  # Indices of target nodes
        'value': [120, 25, 95, 30, 80, 45, 35, 10, 55, 20, 8],  # Matter count
        'colors': [
            'rgba(30, 58, 95, 0.3)',  # Intake -> Investigation
            'rgba(30, 58, 95, 0.3)',  # Intake -> Prelitigation
            'rgba(44, 82, 130, 0.3)', # Investigation -> Prelitigation
            'rgba(44, 82, 130, 0.3)', # Investigation -> Litigation
            'rgba(74, 85, 104, 0.3)', # Prelitigation -> Litigation
            'rgba(74, 85, 104, 0.3)', # Prelitigation -> Settlement
            'rgba(113, 128, 150, 0.3)', # Litigation -> Settlement
            'rgba(113, 128, 150, 0.3)', # Litigation -> Trial
            'rgba(39, 103, 73, 0.4)',  # Settlement -> Resolved
            'rgba(203, 213, 224, 0.4)', # Settlement -> Dismissed
            'rgba(39, 103, 73, 0.4)',  # Trial -> Resolved
        ]
    }


# ============================================
# PARALLEL COORDINATES DATA
# ============================================

def get_mock_parallel_coords():
    """
    Task & Budget correlation data for Parallel Coordinates
    Returns: dict with matter attributes
    """
    np.random.seed(42)
    n_matters = 100

    # Generate correlated data (matters with more tasks tend to have higher budgets)
    tasks_completed = np.random.randint(5, 95, n_matters)
    budget_spent = tasks_completed * 300 + np.random.normal(0, 5000, n_matters)
    budget_spent = np.clip(budget_spent, 1000, 50000)

    cycle_time = 180 - (tasks_completed * 1.2) + np.random.normal(0, 20, n_matters)
    cycle_time = np.clip(cycle_time, 10, 180)

    attorney_hours = tasks_completed * 1.5 + np.random.normal(0, 20, n_matters)
    attorney_hours = np.clip(attorney_hours, 5, 200)

    # Outcome: resolved if tasks > 70 and cycle_time < 100
    outcome = ((tasks_completed > 70) & (cycle_time < 100)).astype(int)

    return {
        'matter_ids': [f'M{i:03d}' for i in range(1, n_matters + 1)],
        'tasks_completed': tasks_completed.tolist(),
        'budget_spent': budget_spent.tolist(),
        'cycle_time': cycle_time.tolist(),
        'attorney_hours': attorney_hours.tolist(),
        'outcome': outcome.tolist(),
        'outcome_numeric': outcome.tolist()
    }


# ============================================
# NETWORK GRAPH DATA
# ============================================

def get_mock_network_graph():
    """
    Relationship network data for Network Graph
    Returns: dict with nodes and edges
    """
    nodes = [
        # Matters
        {'id': 'M001', 'label': 'Smith v. Jones', 'type': 'matter', 'size': 30, 'practice_area': 'Auto Accident'},
        {'id': 'M002', 'label': 'Williams Med Mal', 'type': 'matter', 'size': 40, 'practice_area': 'Medical Malpractice'},
        {'id': 'M003', 'label': 'Brown Workers Comp', 'type': 'matter', 'size': 25, 'practice_area': 'Workers Comp'},
        {'id': 'M004', 'label': 'Davis v. Corp', 'type': 'matter', 'size': 35, 'practice_area': 'Premises Liability'},
        {'id': 'M005', 'label': 'Martinez Product', 'type': 'matter', 'size': 30, 'practice_area': 'Product Liability'},

        # Attorneys
        {'id': 'A001', 'label': 'Travis Crawford', 'type': 'attorney', 'size': 50, 'caseload': 48},
        {'id': 'A002', 'label': 'Lisa Litigator', 'type': 'attorney', 'size': 60, 'caseload': 57},
        {'id': 'A003', 'label': 'Paul Prelit', 'type': 'attorney', 'size': 55, 'caseload': 60},

        # Practice Areas
        {'id': 'PA001', 'label': 'Auto Accident', 'type': 'practice_area', 'size': 45, 'count': 45},
        {'id': 'PA002', 'label': 'Med Mal', 'type': 'practice_area', 'size': 35, 'count': 32},
    ]

    edges = [
        # Matter -> Attorney assignments
        {'source': 'M001', 'target': 'A001', 'weight': 3, 'type': 'assigned_to'},
        {'source': 'M002', 'target': 'A002', 'weight': 5, 'type': 'assigned_to'},
        {'source': 'M003', 'target': 'A003', 'weight': 2, 'type': 'assigned_to'},
        {'source': 'M004', 'target': 'A001', 'weight': 4, 'type': 'assigned_to'},
        {'source': 'M005', 'target': 'A002', 'weight': 3, 'type': 'assigned_to'},

        # Matter -> Practice Area
        {'source': 'M001', 'target': 'PA001', 'weight': 1, 'type': 'belongs_to'},
        {'source': 'M002', 'target': 'PA002', 'weight': 1, 'type': 'belongs_to'},

        # Related matters
        {'source': 'M001', 'target': 'M004', 'weight': 2, 'type': 'related'},

        # Attorney collaboration
        {'source': 'A001', 'target': 'A002', 'weight': 5, 'type': 'collaborates'},
        {'source': 'A002', 'target': 'A003', 'weight': 3, 'type': 'collaborates'},
    ]

    return {
        'nodes': nodes,
        'edges': edges
    }
