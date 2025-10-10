/**
 * Professional Network Dashboard Component
 * Integrates Cytoscape with Mantine layout and Anime.js animations
 */

import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

const ProfessionalNetworkDashboard = ({ 
  id, 
  networkData, 
  viewMode = 'family_clusters',
  selectedNode = null,
  onNodeSelect,
  corporateColors,
  setProps 
}) => {
  const containerRef = useRef(null);
  const cytoscapeRef = useRef(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (networkData && networkData.elements) {
      initializeCytoscape();
    }
  }, [networkData]);

  useEffect(() => {
    if (cytoscapeRef.current && selectedNode) {
      highlightSelectedNode(selectedNode.id);
    }
  }, [selectedNode]);

  const initializeCytoscape = async () => {
    setIsLoading(true);
    
    // Animate container entrance
    anime({
      targets: containerRef.current,
      opacity: [0, 1],
      translateY: [20, 0],
      duration: 600,
      easing: 'easeOutExpo'
    });

    // Initialize Cytoscape with professional styling
    const cytoscape = window.cytoscape;
    
    if (cytoscapeRef.current) {
      cytoscapeRef.current.destroy();
    }

    cytoscapeRef.current = cytoscape({
      container: document.getElementById(`${id}-cytoscape`),
      elements: networkData.elements,
      layout: getLayoutConfig(viewMode),
      style: getProfessionalStyles(corporateColors),
      userZoomingEnabled: true,
      userPanningEnabled: true,
      boxSelectionEnabled: false,
      selectionType: 'single'
    });

    // Add interaction handlers
    cytoscapeRef.current.on('tap', 'node', (event) => {
      const node = event.target;
      const nodeData = node.data();
      
      if (onNodeSelect) {
        onNodeSelect({
          id: nodeData.id,
          name: nodeData.name,
          type: nodeData.type,
          value: nodeData.value
        });
      }
      
      animateNodeSelection(node);
    });

    // Animate nodes entrance with stagger
    await animateNodesEntrance();
    setIsLoading(false);
  };

  const getLayoutConfig = (mode) => {
    const layouts = {
      'family_clusters': {
        name: 'cose',
        animate: true,
        animationDuration: 1000,
        animationEasing: 'ease-out-expo',
        nodeRepulsion: 8000,
        idealEdgeLength: 100,
        edgeElasticity: 100,
        nestingFactor: 1.2
      },
      'vendor_network': {
        name: 'concentric',
        animate: true,
        animationDuration: 1200,
        concentric: (node) => node.data('value') || 1,
        levelWidth: () => 2,
        spacingFactor: 1.5
      },
      'workflow_analysis': {
        name: 'breadthfirst',
        animate: true,
        animationDuration: 1000,
        directed: true,
        spacingFactor: 1.75,
        avoidOverlap: true
      }
    };

    return layouts[mode] || layouts['family_clusters'];
  };

  const getProfessionalStyles = (colors) => [
    // Client nodes - Primary navy circles
    {
      selector: 'node[type="client"]',
      style: {
        'background-color': colors.primary,
        'color': 'white',
        'label': 'data(name)',
        'font-family': 'Inter, sans-serif',
        'font-size': '11px',
        'font-weight': '500',
        'text-wrap': 'wrap',
        'text-max-width': '80px',
        'text-valign': 'center',
        'text-halign': 'center',
        'width': '60px',
        'height': '60px',
        'border-width': '2px',
        'border-color': 'white',
        'border-opacity': 0.8,
        'opacity': 0.9
      }
    },
    
    // Matter nodes - Rectangular, secondary color
    {
      selector: 'node[type="matter"]',
      style: {
        'background-color': colors.secondary,
        'color': 'white',
        'shape': 'roundrectangle',
        'width': '80px',
        'height': '40px',
        'border-width': '1px',
        'border-color': colors.gray_300,
        'opacity': 0.85
      }
    },
    
    // Vendor nodes - Professional green triangles
    {
      selector: 'node[type="vendor"]',
      style: {
        'background-color': colors.success,
        'color': 'white',
        'shape': 'triangle',
        'width': '50px',
        'height': '50px'
      }
    },
    
    // Staff nodes - Amber pentagons
    {
      selector: 'node[type="staff"]',
      style: {
        'background-color': colors.warning,
        'color': 'white',
        'shape': 'pentagon',
        'width': '45px',
        'height': '45px'
      }
    },
    
    // High-value matters - Special styling
    {
      selector: 'node[type="matter"][value > 100000]',
      style: {
        'border-width': '3px',
        'border-color': colors.success,
        'background-color': colors.primary
      }
    },
    
    // Relationship edges
    {
      selector: 'edge',
      style: {
        'width': '2px',
        'line-color': colors.gray_300,
        'target-arrow-color': colors.gray_300,
        'target-arrow-shape': 'triangle',
        'curve-style': 'bezier',
        'opacity': 0.6,
        'font-family': 'Inter, sans-serif',
        'font-size': '9px',
        'color': colors.gray_700,
        'text-rotation': 'autorotate'
      }
    },
    
    // Family relationship edges - Special styling
    {
      selector: 'edge[relationship="family"]',
      style: {
        'line-color': colors.primary,
        'width': '3px',
        'line-style': 'dashed'
      }
    },
    
    // Selected node styling
    {
      selector: ':selected',
      style: {
        'border-width': '4px',
        'border-color': colors.danger,
        'z-index': 10,
        'overlay-opacity': 0.1,
        'overlay-color': colors.danger
      }
    },
    
    // Hover effects
    {
      selector: 'node:active',
      style: {
        'overlay-opacity': 0.2,
        'overlay-color': colors.primary
      }
    }
  ];

  const animateNodesEntrance = () => {
    return new Promise((resolve) => {
      if (!cytoscapeRef.current) {
        resolve();
        return;
      }

      const nodes = cytoscapeRef.current.nodes();
      
      // Set initial state
      nodes.style('opacity', 0);
      nodes.style('width', '10px');
      nodes.style('height', '10px');

      // Animate nodes in with stagger
      let delay = 0;
      nodes.forEach((node, index) => {
        setTimeout(() => {
          node.animate({
            style: {
              'opacity': node.data('type') === 'matter' ? 0.85 : 0.9,
              'width': getNodeSize(node.data('type')).width,
              'height': getNodeSize(node.data('type')).height
            },
            duration: 600,
            easing: 'ease-out-expo'
          });
        }, delay);
        
        delay += 100; // Stagger delay
      });

      setTimeout(resolve, delay + 600);
    });
  };

  const getNodeSize = (nodeType) => {
    const sizes = {
      'client': { width: '60px', height: '60px' },
      'matter': { width: '80px', height: '40px' },
      'vendor': { width: '50px', height: '50px' },
      'staff': { width: '45px', height: '45px' }
    };
    
    return sizes[nodeType] || sizes['client'];
  };

  const animateNodeSelection = (node) => {
    // Pulse animation for selected node
    node.animate({
      style: {
        'width': '70px',
        'height': '70px'
      },
      duration: 200,
      easing: 'ease-out-quad'
    }).animate({
      style: {
        'width': getNodeSize(node.data('type')).width,
        'height': getNodeSize(node.data('type')).height
      },
      duration: 200,
      easing: 'ease-out-quad'
    });
  };

  const highlightSelectedNode = (nodeId) => {
    if (!cytoscapeRef.current) return;
    
    const node = cytoscapeRef.current.getElementById(nodeId);
    if (node.length > 0) {
      // Clear previous selections
      cytoscapeRef.current.elements().unselect();
      
      // Select and center on node
      node.select();
      cytoscapeRef.current.center(node);
      
      animateNodeSelection(node);
    }
  };

  const getViewModeTitle = () => {
    const titles = {
      'family_clusters': 'Family & Matter Clusters',
      'vendor_network': 'Vendor Relationship Network',
      'workflow_analysis': 'Workflow & Department Analysis'
    };
    
    return titles[viewMode] || 'Network Analysis';
  };

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        position: 'relative',
        opacity: 0
      }}
    >
      {/* Header */}
      <div style={{
        marginBottom: '1rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h3 style={{
          fontFamily: "'Crimson Pro', serif",
          fontSize: '1.25rem',
          fontWeight: 600,
          color: corporateColors.dark,
          margin: 0
        }}>
          {getViewModeTitle()}
        </h3>
        
        {isLoading && (
          <div style={{
            fontSize: '0.875rem',
            color: corporateColors.gray_500,
            fontFamily: "'Inter', sans-serif"
          }}>
            Loading network...
          </div>
        )}
      </div>

      {/* Cytoscape Container */}
      <div
        id={`${id}-cytoscape`}
        style={{
          width: '100%',
          height: '500px',
          border: `1px solid ${corporateColors.gray_300}`,
          borderRadius: '8px',
          backgroundColor: 'white',
          position: 'relative'
        }}
      />

      {/* Network Stats */}
      {networkData && networkData.stats && (
        <div style={{
          marginTop: '1rem',
          display: 'flex',
          gap: '1rem',
          fontSize: '0.75rem',
          color: corporateColors.gray_500,
          fontFamily: "'Inter', sans-serif"
        }}>
          <span>Nodes: {networkData.stats.nodeCount}</span>
          <span>Connections: {networkData.stats.edgeCount}</span>
          <span>Clusters: {networkData.stats.clusterCount}</span>
        </div>
      )}
    </div>
  );
};

ProfessionalNetworkDashboard.propTypes = {
  id: PropTypes.string.isRequired,
  networkData: PropTypes.shape({
    elements: PropTypes.array.isRequired,
    stats: PropTypes.object
  }),
  viewMode: PropTypes.oneOf(['family_clusters', 'vendor_network', 'workflow_analysis']),
  selectedNode: PropTypes.object,
  onNodeSelect: PropTypes.func,
  corporateColors: PropTypes.object.isRequired,
  setProps: PropTypes.func
};

export default ProfessionalNetworkDashboard;