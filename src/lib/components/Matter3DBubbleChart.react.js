import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import Plotly from 'plotly.js-dist-min';

/**
 * Professional 3D Matter Bubble Chart Component
 * 
 * Provides sophisticated 3D visualization of matter complexity, progress, and performance
 * with corporate styling and animations integrated with the legal dashboard.
 */
const Matter3DBubbleChart = (props) => {
    const { id, data, style, className, loading_state, setProps } = props;
    const plotRef = useRef(null);
    const containerRef = useRef(null);

    useEffect(() => {
        if (!data || !containerRef.current) return;

        // Professional color palette matching the dashboard
        const colors = {
            primary: '#1E3A5F',      // Navy primary
            secondary: '#2C5282',    // Secondary blue
            success: '#276749',      // Success green
            background: '#F8FAFC',   // Light background
            accent: '#4A5568'        // Neutral accent
        };

        // Create the 3D scatter plot configuration
        const trace = {
            x: data.departments,
            y: data.days_in_stage,
            z: data.total_expenses,
            text: data.hover_text,
            hovertemplate: 
                '<b>%{text}</b><br>' +
                'Department: %{x}<br>' +
                'Days in Stage: %{y}<br>' +
                'Total Expenses: $%{z:,.0f}<br>' +
                '<extra></extra>',
            type: 'scatter3d',
            mode: 'markers',
            marker: {
                size: data.active_tasks,
                sizemode: 'diameter',
                sizeref: Math.max(...data.active_tasks) / 100, // Normalize size
                color: data.percent_complete,
                colorscale: [
                    [0, '#E53E3E'],      // Red for low completion
                    [0.25, '#FD8100'],   // Orange for moderate
                    [0.5, '#F6E05E'],    // Yellow for halfway
                    [0.75, '#38B2AC'],   // Teal for good progress
                    [1, '#276749']       // Success green for completion
                ],
                colorbar: {
                    title: {
                        text: 'Completion %',
                        font: {
                            family: 'Inter, sans-serif',
                            size: 14,
                            color: colors.primary
                        }
                    },
                    thickness: 15,
                    len: 0.7,
                    x: 1.02,
                    tickfont: {
                        family: 'Inter, sans-serif',
                        size: 12,
                        color: colors.primary
                    }
                },
                line: {
                    color: colors.primary,
                    width: 1
                },
                opacity: 0.85
            },
            name: 'Matters'
        };

        // Professional layout configuration
        const layout = {
            title: {
                text: 'Matter Complexity & Progress Landscape',
                font: {
                    family: 'Inter, sans-serif',
                    size: 20,
                    color: colors.primary,
                    weight: 600
                },
                x: 0.05,
                y: 0.95
            },
            scene: {
                xaxis: {
                    title: {
                        text: 'Department',
                        font: {
                            family: 'Inter, sans-serif',
                            size: 14,
                            color: colors.primary
                        }
                    },
                    showgrid: true,
                    gridcolor: '#E2E8F0',
                    zeroline: false,
                    tickfont: {
                        family: 'Inter, sans-serif',
                        size: 11,
                        color: colors.accent
                    }
                },
                yaxis: {
                    title: {
                        text: 'Days in Current Stage',
                        font: {
                            family: 'Inter, sans-serif',
                            size: 14,
                            color: colors.primary
                        }
                    },
                    showgrid: true,
                    gridcolor: '#E2E8F0',
                    zeroline: false,
                    tickfont: {
                        family: 'Inter, sans-serif',
                        size: 11,
                        color: colors.accent
                    }
                },
                zaxis: {
                    title: {
                        text: 'Total Expenses ($)',
                        font: {
                            family: 'Inter, sans-serif',
                            size: 14,
                            color: colors.primary
                        }
                    },
                    type: 'log',
                    showgrid: true,
                    gridcolor: '#E2E8F0',
                    zeroline: false,
                    tickfont: {
                        family: 'Inter, sans-serif',
                        size: 11,
                        color: colors.accent
                    }
                },
                camera: {
                    eye: { x: 1.5, y: 1.5, z: 1.2 },
                    center: { x: 0, y: 0, z: 0 }
                },
                bgcolor: 'rgba(255,255,255,0.95)',
                aspectmode: 'cube'
            },
            margin: { l: 0, r: 80, b: 0, t: 60 },
            height: 650,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
                family: 'Inter, sans-serif',
                color: colors.primary
            },
            hoverlabel: {
                bgcolor: colors.primary,
                bordercolor: colors.secondary,
                font: {
                    family: 'Inter, sans-serif',
                    size: 13,
                    color: 'white'
                }
            }
        };

        // Professional configuration
        const config = {
            displayModeBar: true,
            modeBarButtonsToRemove: [
                'pan2d', 'select2d', 'lasso2d', 'resetCameraDefault3d',
                'resetCameraLastSave3d', 'hoverClosestCartesian', 'hoverCompareCartesian'
            ],
            modeBarButtonsToAdd: [
                {
                    name: 'Reset View',
                    icon: {
                        'width': 1792,
                        'height': 1792,
                        'path': 'M1664 896q0 156-61 298t-164 245-245 164-298 61-298-61-245-164-164-245-61-298q0-182 80.5-343t226.5-270q43-32 95.5-25t83.5 50q32 42 24.5 94.5t-49.5 84.5q-98 74-151.5 181.5t-53.5 228.5q0 104 40.5 198.5t109.5 163.5 163.5 109.5 198.5 40.5 198.5-40.5 163.5-109.5 109.5-163.5 40.5-198.5q0-121-53.5-228.5t-151.5-181.5q-42-32-49.5-84.5t24.5-94.5q31-43 83.5-50t95.5 25q146 109 226.5 270t80.5 343z'
                    },
                    click: () => {
                        Plotly.relayout(containerRef.current, {
                            'scene.camera.eye': { x: 1.5, y: 1.5, z: 1.2 },
                            'scene.camera.center': { x: 0, y: 0, z: 0 }
                        });
                    }
                }
            ],
            displaylogo: false,
            toImageButtonOptions: {
                format: 'png',
                filename: 'matter_3d_analysis',
                height: 650,
                width: 900,
                scale: 2
            }
        };

        // Create the plot
        Plotly.newPlot(containerRef.current, [trace], layout, config)
            .then(() => {
                // Add professional entrance animation
                Plotly.animate(containerRef.current, {
                    data: [{
                        marker: {
                            ...trace.marker,
                            opacity: 0.85
                        }
                    }]
                }, {
                    transition: {
                        duration: 800,
                        easing: 'cubic-in-out'
                    },
                    frame: {
                        duration: 800
                    }
                });
            });

        // Handle click events for interactivity
        const handleClick = (eventData) => {
            if (eventData.points && eventData.points.length > 0) {
                const point = eventData.points[0];
                const matterData = {
                    pointIndex: point.pointIndex,
                    department: point.x,
                    daysInStage: point.y,
                    totalExpenses: point.z,
                    activeTasksCount: point.marker.size,
                    percentComplete: point.marker.color
                };
                
                if (setProps) {
                    setProps({
                        selectedMatter: matterData
                    });
                }
            }
        };

        // Handle hover events
        const handleHover = (eventData) => {
            if (eventData.points && eventData.points.length > 0) {
                const point = eventData.points[0];
                if (setProps) {
                    setProps({
                        hoveredMatter: {
                            pointIndex: point.pointIndex,
                            department: point.x,
                            daysInStage: point.y,
                            totalExpenses: point.z
                        }
                    });
                }
            }
        };

        // Attach event listeners
        containerRef.current.on('plotly_click', handleClick);
        containerRef.current.on('plotly_hover', handleHover);

        // Cleanup function
        return () => {
            if (containerRef.current) {
                Plotly.purge(containerRef.current);
            }
        };

    }, [data, setProps]);

    // Loading state styling
    const loadingStyle = {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '650px',
        backgroundColor: '#F8FAFC',
        borderRadius: '8px',
        border: '1px solid #E2E8F0',
        color: '#1E3A5F',
        fontSize: '16px',
        fontFamily: 'Inter, sans-serif'
    };

    return (
        <div 
            id={id}
            className={className}
            style={{
                ...style,
                position: 'relative',
                fontFamily: 'Inter, sans-serif'
            }}
        >
            {loading_state && loading_state.is_loading ? (
                <div style={loadingStyle}>
                    <div>
                        <div style={{ 
                            width: '40px', 
                            height: '40px', 
                            border: '3px solid #E2E8F0',
                            borderTop: '3px solid #1E3A5F',
                            borderRadius: '50%',
                            animation: 'spin 1s linear infinite',
                            marginBottom: '16px',
                            margin: '0 auto 16px'
                        }}></div>
                        Loading Matter Analytics...
                    </div>
                </div>
            ) : (
                <div 
                    ref={containerRef}
                    style={{ 
                        width: '100%', 
                        height: '650px',
                        backgroundColor: 'rgba(0,0,0,0)',
                        borderRadius: '8px'
                    }}
                />
            )}
            
            {/* CSS for loading animation */}
            <style jsx>{`
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
};

Matter3DBubbleChart.defaultProps = {
    style: {},
    className: '',
    loading_state: { is_loading: false }
};

Matter3DBubbleChart.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Data for the 3D bubble chart
     */
    data: PropTypes.shape({
        departments: PropTypes.arrayOf(PropTypes.string).isRequired,
        days_in_stage: PropTypes.arrayOf(PropTypes.number).isRequired,
        total_expenses: PropTypes.arrayOf(PropTypes.number).isRequired,
        active_tasks: PropTypes.arrayOf(PropTypes.number).isRequired,
        percent_complete: PropTypes.arrayOf(PropTypes.number).isRequired,
        hover_text: PropTypes.arrayOf(PropTypes.string).isRequired
    }),

    /**
     * CSS style properties
     */
    style: PropTypes.object,

    /**
     * CSS class name
     */
    className: PropTypes.string,

    /**
     * Object that holds the loading state object coming from dash-renderer
     */
    loading_state: PropTypes.shape({
        /**
         * Determines if the component is loading or not
         */
        is_loading: PropTypes.bool,
        /**
         * Holds which property is loading
         */
        prop_name: PropTypes.string,
        /**
         * Holds the name of the component that is loading
         */
        component_name: PropTypes.string
    }),

    /**
     * Data about the selected matter point
     */
    selectedMatter: PropTypes.object,

    /**
     * Data about the currently hovered matter point
     */
    hoveredMatter: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     */
    setProps: PropTypes.func
};

export default Matter3DBubbleChart;