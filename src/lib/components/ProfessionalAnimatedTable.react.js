/**
 * Professional Mantine Table with Anime.js Animations
 * Staggered row reveals, hover effects, and data update animations
 */

import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

const ProfessionalAnimatedTable = ({ 
  id, 
  data, 
  columns, 
  animateOnLoad = true,
  staggerDelay = 80,
  hoverEffects = true,
  setProps 
}) => {
  const tableRef = useRef(null);
  const [animatedRows, setAnimatedRows] = useState(new Set());

  useEffect(() => {
    if (animateOnLoad && tableRef.current) {
      animateTableEntrance();
    }
  }, []);

  useEffect(() => {
    if (data && data.length > 0) {
      animateNewRows();
    }
  }, [data]);

  const animateTableEntrance = () => {
    // Animate header first
    anime({
      targets: `#${id} thead`,
      opacity: [0, 1],
      translateY: [-20, 0],
      duration: 400,
      easing: 'easeOutQuad'
    });

    // Then animate rows with stagger
    anime({
      targets: `#${id} tbody tr`,
      opacity: [0, 1],
      translateX: [-30, 0],
      duration: 600,
      delay: anime.stagger(staggerDelay, { start: 200 }),
      easing: 'easeOutExpo',
      complete: () => {
        // Mark all initial rows as animated
        const rowSet = new Set();
        data.forEach((_, index) => rowSet.add(index));
        setAnimatedRows(rowSet);
      }
    });
  };

  const animateNewRows = () => {
    data.forEach((row, index) => {
      if (!animatedRows.has(index)) {
        anime({
          targets: `#${id} .table-row-${index}`,
          opacity: [0, 1],
          translateX: [-30, 0],
          scale: [0.95, 1],
          duration: 500,
          easing: 'easeOutBack',
          complete: () => {
            setAnimatedRows(prev => new Set([...prev, index]));
          }
        });
      }
    });
  };

  const handleRowHover = (index, isEntering) => {
    if (!hoverEffects) return;

    anime({
      targets: `#${id} .table-row-${index}`,
      backgroundColor: isEntering ? '#F7FAFC' : '#FFFFFF',
      scale: isEntering ? 1.01 : 1,
      duration: 200,
      easing: 'easeOutQuad'
    });
  };

  const getStatusBadgeStyle = (status) => {
    const statusStyles = {
      'Active': { background: '#276749', color: 'white' },
      'Pending': { background: '#975A16', color: 'white' },
      'Completed': { background: '#1E3A5F', color: 'white' },
      'Urgent': { background: '#9B2C2C', color: 'white' },
      'Draft': { background: '#718096', color: 'white' }
    };
    
    return {
      padding: '0.25rem 0.5rem',
      borderRadius: '4px',
      fontSize: '0.75rem',
      fontWeight: 600,
      textAlign: 'center',
      display: 'inline-block',
      minWidth: '60px',
      ...statusStyles[status] || statusStyles['Draft']
    };
  };

  return (
    <div style={{ overflow: 'hidden', borderRadius: '8px' }}>
      <table
        ref={tableRef}
        id={id}
        style={{
          width: '100%',
          borderCollapse: 'separate',
          borderSpacing: '0',
          backgroundColor: 'white',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}
      >
        <thead>
          <tr style={{
            backgroundColor: '#EDF2F7',
            opacity: animateOnLoad ? 0 : 1
          }}>
            {columns.map((column, index) => (
              <th
                key={index}
                style={{
                  padding: '1rem 0.75rem',
                  fontFamily: "'Inter', sans-serif",
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                  color: '#4A5568',
                  textAlign: 'left',
                  borderBottom: '2px solid #CBD5E0'
                }}
              >
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr
              key={rowIndex}
              className={`table-row-${rowIndex}`}
              style={{
                opacity: animateOnLoad ? 0 : 1,
                cursor: 'pointer',
                transition: 'background-color 0.2s ease'
              }}
              onMouseEnter={() => handleRowHover(rowIndex, true)}
              onMouseLeave={() => handleRowHover(rowIndex, false)}
            >
              {columns.map((column, colIndex) => {
                const cellValue = row[column.accessor];
                
                return (
                  <td
                    key={colIndex}
                    style={{
                      padding: '1rem 0.75rem',
                      borderBottom: '1px solid #E2E8F0',
                      fontFamily: "'Inter', sans-serif",
                      fontSize: '0.875rem',
                      color: '#2D3748',
                      verticalAlign: 'middle'
                    }}
                  >
                    {column.accessor === 'status' ? (
                      <span style={getStatusBadgeStyle(cellValue)}>
                        {cellValue}
                      </span>
                    ) : column.accessor === 'progress' ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{
                          width: '60px',
                          height: '6px',
                          backgroundColor: '#E2E8F0',
                          borderRadius: '3px',
                          overflow: 'hidden'
                        }}>
                          <div
                            style={{
                              width: `${cellValue}%`,
                              height: '100%',
                              backgroundColor: '#1E3A5F',
                              borderRadius: '3px',
                              transition: 'width 0.8s ease-out'
                            }}
                          />
                        </div>
                        <span style={{ fontSize: '0.75rem', color: '#718096' }}>
                          {cellValue}%
                        </span>
                      </div>
                    ) : (
                      cellValue
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

ProfessionalAnimatedTable.propTypes = {
  id: PropTypes.string.isRequired,
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
  columns: PropTypes.arrayOf(PropTypes.shape({
    accessor: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired
  })).isRequired,
  animateOnLoad: PropTypes.bool,
  staggerDelay: PropTypes.number,
  hoverEffects: PropTypes.bool,
  setProps: PropTypes.func
};

export default ProfessionalAnimatedTable;