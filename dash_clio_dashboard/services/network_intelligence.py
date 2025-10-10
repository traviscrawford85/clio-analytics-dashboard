# Enhanced Network Intelligence Service
# Integration with your existing ClioCore architecture

import json
import sqlite3
from typing import Dict, List, Optional, Any
from neo4j import GraphDatabase
import pandas as pd
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import dash_cytoscape as cyto
import plotly.express as px

class EnhancedNetworkIntelligenceService:
    """
    Professional network analysis service integrating with your existing ClioCore stack
    Combines Neo4j graph data with SQLite metrics for comprehensive insights
    """
    
    def __init__(self, neo4j_uri="bolt://localhost:7687", sqlite_path="clio-analytics.db"):
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=("neo4j", "password"))
        self.sqlite_conn = sqlite3.connect(sqlite_path)
        
        # Your existing corporate color scheme
        self.colors = {
            'primary': '#1E3A5F',
            'primary_light': '#2C5282',
            'success': '#276749',
            'warning': '#975A16',
            'danger': '#9B2C2C',
            'gray_700': '#4A5568',
            'gray_300': '#CBD5E0',
            'white': '#FFFFFF'
        }
    
    def get_client_family_network(self, limit: int = 100) -> Dict[str, Any]:
        """
        Get family relationship clusters for client analysis
        Combines Neo4j relationships with SQLite matter metrics
        """
        
        # Neo4j query for family relationships
        cypher_query = """
        MATCH (c1:Client)-[:FAMILY_OF]-(c2:Client)
        MATCH (c1)-[:OWNS]->(m1:Matter)
        MATCH (c2)-[:OWNS]->(m2:Matter)
        OPTIONAL MATCH (m1)-[:ASSIGNED_TO]->(s1:Staff)
        OPTIONAL MATCH (m2)-[:ASSIGNED_TO]->(s2:Staff)
        RETURN 
            c1.id as client1_id, c1.name as client1_name,
            c2.id as client2_id, c2.name as client2_name,
            collect(DISTINCT m1.id) as client1_matters,
            collect(DISTINCT m2.id) as client2_matters,
            count(DISTINCT m1) + count(DISTINCT m2) as total_matters
        ORDER BY total_matters DESC
        LIMIT $limit
        """
        
        with self.neo4j_driver.session() as session:
            neo4j_result = session.run(cypher_query, limit=limit)
            
            nodes = []
            edges = []
            seen_clients = set()
            seen_matters = set()
            
            for record in neo4j_result:
                # Add client nodes
                for client_key in ['client1', 'client2']:
                    client_id = record[f'{client_key}_id']
                    client_name = record[f'{client_key}_name']
                    
                    if client_id not in seen_clients:
                        seen_clients.add(client_id)
                        
                        # Enrich with SQLite data
                        client_metrics = self._get_client_metrics(client_id)
                        
                        nodes.append({
                            'data': {
                                'id': f'client_{client_id}',
                                'name': client_name,
                                'type': 'client',
                                'value': client_metrics.get('total_matter_value', 0),
                                'matter_count': client_metrics.get('matter_count', 0)
                            }
                        })
                
                # Add family relationship edge
                edges.append({
                    'data': {
                        'source': f'client_{record["client1_id"]}',
                        'target': f'client_{record["client2_id"]}',
                        'relationship': 'family',
                        'label': 'Family'
                    }
                })
                
                # Add matter nodes and connections
                for matter_list, client_id in [
                    (record['client1_matters'], record['client1_id']),
                    (record['client2_matters'], record['client2_id'])
                ]:
                    for matter_id in matter_list:
                        if matter_id not in seen_matters:
                            seen_matters.add(matter_id)
                            
                            matter_data = self._get_matter_data(matter_id)
                            
                            nodes.append({
                                'data': {
                                    'id': f'matter_{matter_id}',
                                    'name': matter_data.get('description', f'Matter {matter_id}'),
                                    'type': 'matter',
                                    'value': matter_data.get('value', 0),
                                    'status': matter_data.get('status', 'Active')
                                }
                            })
                            
                            # Client owns matter edge
                            edges.append({
                                'data': {
                                    'source': f'client_{client_id}',
                                    'target': f'matter_{matter_id}',
                                    'relationship': 'owns',
                                    'label': 'Owns'
                                }
                            })
        
        return {
            'elements': nodes + edges,
            'stats': {
                'nodeCount': len(nodes),
                'edgeCount': len(edges),
                'clusterCount': len(seen_clients) // 2  # Approximate family clusters
            },
            'layout': 'cose',
            'title': 'Client Family Networks'
        }
    
    def get_vendor_matter_network(self, practice_area: Optional[str] = None, min_value: int = 50000) -> Dict[str, Any]:
        """
        Analyze vendor usage patterns across matters
        Shows which vendors are used most frequently and for what types of cases
        """
        
        where_clause = "WHERE m.value >= $min_value"
        if practice_area:
            where_clause += " AND m.practice_area = $practice_area"
        
        cypher_query = f"""
        MATCH (v:Vendor)-[r:USED_IN]->(m:Matter)
        MATCH (m)-[:OWNED_BY]->(c:Client)
        {where_clause}
        RETURN 
            v.id as vendor_id, v.name as vendor_name, v.specialty as vendor_specialty,
            m.id as matter_id, m.description as matter_desc, m.value as matter_value,
            c.id as client_id, c.name as client_name,
            r.cost as vendor_cost, r.service_type as service_type
        ORDER BY r.cost DESC
        """
        
        params = {'min_value': min_value}
        if practice_area:
            params['practice_area'] = practice_area
        
        with self.neo4j_driver.session() as session:
            result = session.run(cypher_query, **params)
            
            nodes = []
            edges = []
            seen_vendors = set()
            seen_matters = set()
            seen_clients = set()
            
            for record in result:
                # Vendor nodes
                vendor_id = record['vendor_id']
                if vendor_id not in seen_vendors:
                    seen_vendors.add(vendor_id)
                    
                    vendor_metrics = self._get_vendor_metrics(vendor_id)
                    
                    nodes.append({
                        'data': {
                            'id': f'vendor_{vendor_id}',
                            'name': record['vendor_name'],
                            'type': 'vendor',
                            'specialty': record['vendor_specialty'],
                            'total_revenue': vendor_metrics.get('total_revenue', 0),
                            'matter_count': vendor_metrics.get('matter_count', 0)
                        }
                    })
                
                # Matter nodes
                matter_id = record['matter_id']
                if matter_id not in seen_matters:
                    seen_matters.add(matter_id)
                    
                    nodes.append({
                        'data': {
                            'id': f'matter_{matter_id}',
                            'name': record['matter_desc'][:30] + '...' if len(record['matter_desc']) > 30 else record['matter_desc'],
                            'type': 'matter',
                            'value': record['matter_value']
                        }
                    })
                
                # Client nodes (smaller, for context)
                client_id = record['client_id']
                if client_id not in seen_clients:
                    seen_clients.add(client_id)
                    
                    nodes.append({
                        'data': {
                            'id': f'client_{client_id}',
                            'name': record['client_name'],
                            'type': 'client',
                            'value': 0  # Context node
                        }
                    })
                    
                    # Client owns matter
                    edges.append({
                        'data': {
                            'source': f'client_{client_id}',
                            'target': f'matter_{matter_id}',
                            'relationship': 'owns',
                            'label': 'Owns'
                        }
                    })
                
                # Vendor used in matter
                edges.append({
                    'data': {
                        'source': f'vendor_{vendor_id}',
                        'target': f'matter_{matter_id}',
                        'relationship': 'used_in',
                        'label': f'${record["vendor_cost"]:,.0f}',
                        'cost': record['vendor_cost'],
                        'service_type': record['service_type']
                    }
                })
        
        return {
            'elements': nodes + edges,
            'stats': {
                'nodeCount': len(nodes),
                'edgeCount': len(edges),
                'vendorCount': len(seen_vendors)
            },
            'layout': 'concentric',
            'title': f'Vendor Network Analysis{" - " + practice_area if practice_area else ""}'
        }
    
    def get_staff_workload_network(self, department: Optional[str] = None) -> Dict[str, Any]:
        """
        Visualize staff workload distribution and matter assignments
        Shows workflow patterns and potential bottlenecks
        """
        
        where_clause = ""
        if department:
            where_clause = "WHERE d.name = $department"
        
        cypher_query = f"""
        MATCH (m:Matter)-[:ASSIGNED_TO]->(s:Staff)-[:WORKS_IN]->(d:Department)
        MATCH (m)-[:OWNED_BY]->(c:Client)
        {where_clause}
        RETURN 
            s.id as staff_id, s.name as staff_name, s.role as staff_role,
            d.id as dept_id, d.name as dept_name,
            m.id as matter_id, m.description as matter_desc, m.status as matter_status,
            c.id as client_id, c.name as client_name
        ORDER BY s.name
        """
        
        params = {'department': department} if department else {}
        
        with self.neo4j_driver.session() as session:
            result = session.run(cypher_query, **params)
            
            nodes = []
            edges = []
            seen_staff = set()
            seen_departments = set()
            seen_matters = set()
            
            staff_workloads = {}
            
            for record in result:
                # Track staff workload
                staff_id = record['staff_id']
                if staff_id not in staff_workloads:
                    staff_workloads[staff_id] = 0
                staff_workloads[staff_id] += 1
                
                # Staff nodes
                if staff_id not in seen_staff:
                    seen_staff.add(staff_id)
                    
                    staff_metrics = self._get_staff_metrics(staff_id)
                    
                    nodes.append({
                        'data': {
                            'id': f'staff_{staff_id}',
                            'name': record['staff_name'],
                            'type': 'staff',
                            'role': record['staff_role'],
                            'workload': staff_metrics.get('active_matters', 0),
                            'capacity_pct': staff_metrics.get('capacity_percentage', 50)
                        }
                    })
                
                # Department nodes
                dept_id = record['dept_id']
                if dept_id not in seen_departments:
                    seen_departments.add(dept_id)
                    
                    nodes.append({
                        'data': {
                            'id': f'dept_{dept_id}',
                            'name': record['dept_name'],
                            'type': 'department',
                            'staff_count': 0  # Will be calculated
                        }
                    })
                    
                    # Staff works in department
                    edges.append({
                        'data': {
                            'source': f'staff_{staff_id}',
                            'target': f'dept_{dept_id}',
                            'relationship': 'works_in',
                            'label': 'Works in'
                        }
                    })
                
                # Matter nodes (smaller, for context)
                matter_id = record['matter_id']
                if matter_id not in seen_matters:
                    seen_matters.add(matter_id)
                    
                    nodes.append({
                        'data': {
                            'id': f'matter_{matter_id}',
                            'name': record['matter_desc'][:25] + '...' if len(record['matter_desc']) > 25 else record['matter_desc'],
                            'type': 'matter',
                            'status': record['matter_status']
                        }
                    })
                    
                    # Staff assigned to matter
                    edges.append({
                        'data': {
                            'source': f'staff_{staff_id}',
                            'target': f'matter_{matter_id}',
                            'relationship': 'assigned_to',
                            'label': 'Assigned'
                        }
                    })
        
        return {
            'elements': nodes + edges,
            'stats': {
                'nodeCount': len(nodes),
                'edgeCount': len(edges),
                'staffCount': len(seen_staff),
                'avgWorkload': sum(staff_workloads.values()) / len(staff_workloads) if staff_workloads else 0
            },
            'layout': 'breadthfirst',
            'title': f'Staff Workload Analysis{" - " + department if department else ""}'
        }
    
    def _get_client_metrics(self, client_id: str) -> Dict[str, Any]:
        """Get client metrics from SQLite"""
        query = """
        SELECT 
            COUNT(m.id) as matter_count,
            SUM(m.value) as total_matter_value,
            AVG(m.value) as avg_matter_value
        FROM matters m 
        WHERE m.client_id = ?
        """
        
        df = pd.read_sql(query, self.sqlite_conn, params=[client_id])
        return df.iloc[0].to_dict() if not df.empty else {}
    
    def _get_matter_data(self, matter_id: str) -> Dict[str, Any]:
        """Get matter data from SQLite"""
        query = """
        SELECT description, value, status, practice_area, created_date
        FROM matters 
        WHERE id = ?
        """
        
        df = pd.read_sql(query, self.sqlite_conn, params=[matter_id])
        return df.iloc[0].to_dict() if not df.empty else {}
    
    def _get_vendor_metrics(self, vendor_id: str) -> Dict[str, Any]:
        """Get vendor performance metrics"""
        query = """
        SELECT 
            COUNT(DISTINCT m.id) as matter_count,
            SUM(ve.cost) as total_revenue,
            AVG(ve.cost) as avg_cost_per_matter
        FROM vendor_engagements ve
        JOIN matters m ON ve.matter_id = m.id
        WHERE ve.vendor_id = ?
        """
        
        df = pd.read_sql(query, self.sqlite_conn, params=[vendor_id])
        return df.iloc[0].to_dict() if not df.empty else {}
    
    def _get_staff_metrics(self, staff_id: str) -> Dict[str, Any]:
        """Get staff workload and performance metrics"""
        query = """
        SELECT 
            COUNT(CASE WHEN m.status = 'Active' THEN 1 END) as active_matters,
            COUNT(m.id) as total_matters,
            AVG(m.value) as avg_matter_value
        FROM matter_assignments ma
        JOIN matters m ON ma.matter_id = m.id
        WHERE ma.staff_id = ?
        """
        
        df = pd.read_sql(query, self.sqlite_conn, params=[staff_id])
        result = df.iloc[0].to_dict() if not df.empty else {}
        
        # Calculate capacity percentage (assuming 15 active matters = 100% capacity)
        result['capacity_percentage'] = min(100, (result.get('active_matters', 0) / 15) * 100)
        
        return result

def create_network_enhanced_layout(service: EnhancedNetworkIntelligenceService, view_type: str = 'overview'):
    """
    Create a professional layout combining traditional dashboard elements with network views
    Integrates with your existing Mantine + Anime.js architecture
    """
    
    if view_type == 'family_analysis':
        # Family relationship analysis view
        network_data = service.get_client_family_network()
        
        return dmc.Paper([
            dmc.Grid([
                # Traditional KPIs (left column)
                dmc.GridCol([
                    dmc.Title("Family Matter Analysis", order=3, mb="md"),
                    
                    # Animated KPI cards
                    dmc.Grid([
                        dmc.GridCol([
                            create_animated_kpi_card(
                                "Total Families", 
                                network_data['stats']['clusterCount'], 
                                "family networks"
                            )
                        ], span=6),
                        dmc.GridCol([
                            create_animated_kpi_card(
                                "Connected Matters", 
                                network_data['stats']['nodeCount'] - network_data['stats']['clusterCount'] * 2,
                                "matters"
                            )
                        ], span=6)
                    ])
                ], span=4),
                
                # Network visualization (right column)
                dmc.GridCol([
                    dmc.Paper([
                        cyto.Cytoscape(
                            id='family-network',
                            elements=network_data['elements'],
                            layout={'name': network_data['layout'], 'animate': True},
                            style={'width': '100%', 'height': '500px'},
                            stylesheet=get_professional_cytoscape_styles(service.colors)
                        )
                    ], p="md", shadow="sm")
                ], span=8)
            ])
        ], p="lg", shadow="sm")
    
    elif view_type == 'vendor_analysis':
        # Vendor relationship analysis view
        network_data = service.get_vendor_matter_network()
        
        return dmc.Paper([
            dmc.Title("Vendor Network Analysis", order=3, mb="lg"),
            
            # Controls
            dmc.Group([
                dmc.Select(
                    id='practice-area-filter',
                    label="Practice Area",
                    placeholder="All Areas",
                    data=[
                        {'label': 'Personal Injury', 'value': 'personal_injury'},
                        {'label': 'Corporate Law', 'value': 'corporate'},
                        {'label': 'Family Law', 'value': 'family'},
                        {'label': 'Criminal Defense', 'value': 'criminal'}
                    ],
                    w=200
                ),
                dmc.NumberInput(
                    id='min-value-filter',
                    label="Minimum Matter Value",
                    value=50000,
                    step=10000,
                    w=200
                )
            ], mb="lg"),
            
            # Network view
            cyto.Cytoscape(
                id='vendor-network',
                elements=network_data['elements'],
                layout={'name': network_data['layout'], 'animate': True},
                style={'width': '100%', 'height': '600px'},
                stylesheet=get_professional_cytoscape_styles(service.colors)
            ),
            
            # Network statistics
            dmc.Group([
                dmc.Badge(f"{network_data['stats']['vendorCount']} Vendors", color="blue"),
                dmc.Badge(f"{network_data['stats']['nodeCount']} Total Nodes", color="gray"),
                dmc.Badge(f"{network_data['stats']['edgeCount']} Connections", color="green")
            ], mt="md")
        ], p="lg", shadow="sm")
    
    else:  # staff_workload
        # Staff workload visualization
        network_data = service.get_staff_workload_network()
        
        return dmc.Paper([
            dmc.Grid([
                # Workload summary (top)
                dmc.GridCol([
                    dmc.Group([
                        dmc.Paper([
                            dmc.Text("Average Workload", size="sm", c="dimmed"),
                            dmc.Title(f"{network_data['stats']['avgWorkload']:.1f}", order=2, c="blue")
                        ], p="md", ta="center"),
                        dmc.Paper([
                            dmc.Text("Active Staff", size="sm", c="dimmed"),
                            dmc.Title(str(network_data['stats']['staffCount']), order=2, c="green")
                        ], p="md", ta="center"),
                        dmc.Paper([
                            dmc.Text("Total Connections", size="sm", c="dimmed"),
                            dmc.Title(str(network_data['stats']['edgeCount']), order=2, c="orange")
                        ], p="md", ta="center")
                    ], grow=True)
                ], span=12),
                
                # Network visualization
                dmc.GridCol([
                    cyto.Cytoscape(
                        id='staff-workload-network',
                        elements=network_data['elements'],
                        layout={'name': network_data['layout'], 'animate': True},
                        style={'width': '100%', 'height': '500px'},
                        stylesheet=get_professional_cytoscape_styles(service.colors)
                    )
                ], span=12)
            ])
        ], p="lg", shadow="sm")

def create_animated_kpi_card(label: str, value: int, suffix: str = ""):
    """Create animated KPI card matching your existing design system"""
    return dmc.Paper([
        dmc.Text(label.upper(), size="xs", fw=500, c="dimmed", mb="xs"),
        html.Div([
            dmc.Title(str(value), order=2, c="blue"),
            dmc.Text(suffix, size="sm", c="dimmed", ml="xs")
        ], style={'display': 'flex', 'alignItems': 'baseline'})
    ], p="md", shadow="sm", className="animated-kpi-card")

def get_professional_cytoscape_styles(colors: Dict[str, str]) -> List[Dict]:
    """Professional Cytoscape styles matching your Mantine theme"""
    return [
        # Client nodes
        {
            'selector': 'node[type="client"]',
            'style': {
                'background-color': colors['primary'],
                'color': 'white',
                'label': 'data(name)',
                'font-family': 'Inter, sans-serif',
                'font-size': '10px',
                'font-weight': '500',
                'text-wrap': 'wrap',
                'text-max-width': '60px',
                'width': '50px',
                'height': '50px',
                'border-width': '2px',
                'border-color': 'white'
            }
        },
        
        # Matter nodes
        {
            'selector': 'node[type="matter"]',
            'style': {
                'background-color': colors['primary_light'],
                'color': 'white',
                'shape': 'roundrectangle',
                'width': '70px',
                'height': '35px',
                'font-size': '9px'
            }
        },
        
        # Vendor nodes
        {
            'selector': 'node[type="vendor"]',
            'style': {
                'background-color': colors['success'],
                'color': 'white',
                'shape': 'triangle',
                'width': '45px',
                'height': '45px'
            }
        },
        
        # Staff nodes
        {
            'selector': 'node[type="staff"]',
            'style': {
                'background-color': colors['warning'],
                'color': 'white',
                'shape': 'pentagon',
                'width': '40px',
                'height': '40px'
            }
        },
        
        # Department nodes
        {
            'selector': 'node[type="department"]',
            'style': {
                'background-color': colors['gray_700'],
                'color': 'white',
                'shape': 'hexagon',
                'width': '60px',
                'height': '60px'
            }
        },
        
        # Edges
        {
            'selector': 'edge',
            'style': {
                'width': '2px',
                'line-color': colors['gray_300'],
                'target-arrow-color': colors['gray_300'],
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier'
            }
        },
        
        # Family relationship edges
        {
            'selector': 'edge[relationship="family"]',
            'style': {
                'line-color': colors['primary'],
                'width': '3px',
                'line-style': 'dashed'
            }
        },
        
        # High-value matter highlighting
        {
            'selector': 'node[type="matter"][value > 100000]',
            'style': {
                'border-width': '3px',
                'border-color': colors['success']
            }
        },
        
        # Selected state
        {
            'selector': ':selected',
            'style': {
                'border-width': '4px',
                'border-color': colors['danger'],
                'z-index': 10
            }
        }
    ]