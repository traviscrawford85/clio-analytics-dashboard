import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * WorkloadMatrix - Heatmap showing tasks per staff member per stage
 * Visual representation of workload distribution
 */
const WorkloadMatrix = ({ id, data, stages, users, colorScale, setProps }) => {
  useEffect(() => {
    // Animate cells on mount
    anime({
      targets: '.matrix-cell',
      opacity: [0, 1],
      scale: [0.8, 1],
      delay: anime.stagger(30, { grid: [users.length, stages.length], from: 'center' }),
      duration: 500,
      easing: 'easeOutBack'
    });
  }, [data, users.length, stages.length]);

  const getMaxValue = () => {
    let max = 0;
    data.forEach(row => {
      row.forEach(val => {
        if (val > max) max = val;
      });
    });
    return max || 1;
  };

  const maxValue = getMaxValue();

  const getCellColor = (value) => {
    if (value === 0) return '#F9FAFB';

    const intensity = value / maxValue;

    if (colorScale === 'heat') {
      // Heat scale: blue -> yellow -> red
      if (intensity < 0.33) {
        return `rgba(59, 130, 246, ${0.3 + intensity * 2})`;
      } else if (intensity < 0.66) {
        return `rgba(251, 191, 36, ${0.4 + (intensity - 0.33) * 2})`;
      } else {
        return `rgba(220, 38, 38, ${0.5 + (intensity - 0.66) * 1.5})`;
      }
    } else {
      // Default: blue scale
      return `rgba(0, 112, 224, ${0.2 + intensity * 0.8})`;
    }
  };

  const getCellTextColor = (value) => {
    const intensity = value / maxValue;
    return intensity > 0.5 ? '#FFFFFF' : '#111827';
  };

  return (
    <div id={id} style={{
      width: '100%',
      overflowX: 'auto',
      overflowY: 'auto'
    }}>
      <div style={{
        display: 'inline-block',
        minWidth: '100%'
      }}>
        {/* Header row (stages) */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: `160px repeat(${stages.length}, 100px)`,
          gap: '2px',
          marginBottom: '2px'
        }}>
          <div style={{
            padding: '12px',
            fontWeight: 700,
            fontSize: '0.75rem',
            color: '#6B7280',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Staff / Stage
          </div>
          {stages.map((stage, idx) => (
            <div
              key={idx}
              style={{
                padding: '12px 8px',
                fontWeight: 600,
                fontSize: '0.75rem',
                color: '#374151',
                textAlign: 'center',
                backgroundColor: '#F3F4F6',
                borderRadius: '8px'
              }}
            >
              {stage}
            </div>
          ))}
        </div>

        {/* Data rows */}
        {users.map((user, userIdx) => (
          <div
            key={userIdx}
            style={{
              display: 'grid',
              gridTemplateColumns: `160px repeat(${stages.length}, 100px)`,
              gap: '2px',
              marginBottom: '2px'
            }}
          >
            {/* User name cell */}
            <div style={{
              padding: '12px',
              fontWeight: 600,
              fontSize: '0.875rem',
              color: '#111827',
              backgroundColor: '#F9FAFB',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center'
            }}>
              {user}
            </div>

            {/* Data cells */}
            {data[userIdx].map((value, stageIdx) => {
              const total = data[userIdx].reduce((sum, val) => sum + val, 0);

              return (
                <div
                  key={stageIdx}
                  className="matrix-cell"
                  style={{
                    padding: '12px 8px',
                    backgroundColor: getCellColor(value),
                    color: getCellTextColor(value),
                    fontWeight: 700,
                    fontSize: '1rem',
                    textAlign: 'center',
                    borderRadius: '8px',
                    opacity: 0,
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    position: 'relative'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'scale(1.1)';
                    e.currentTarget.style.zIndex = '10';
                    e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.15)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'scale(1)';
                    e.currentTarget.style.zIndex = '1';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                  title={`${user} - ${stages[stageIdx]}: ${value} tasks`}
                >
                  {value}
                </div>
              );
            })}
          </div>
        ))}

        {/* Total row */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: `160px repeat(${stages.length}, 100px)`,
          gap: '2px',
          marginTop: '8px',
          paddingTop: '8px',
          borderTop: '2px solid #E5E7EB'
        }}>
          <div style={{
            padding: '12px',
            fontWeight: 700,
            fontSize: '0.875rem',
            color: '#374151',
            backgroundColor: '#F3F4F6',
            borderRadius: '8px'
          }}>
            Total
          </div>
          {stages.map((_, stageIdx) => {
            const total = data.reduce((sum, row) => sum + row[stageIdx], 0);
            return (
              <div
                key={stageIdx}
                style={{
                  padding: '12px 8px',
                  fontWeight: 700,
                  fontSize: '1rem',
                  textAlign: 'center',
                  backgroundColor: '#F3F4F6',
                  color: '#111827',
                  borderRadius: '8px'
                }}
              >
                {total}
              </div>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div style={{
        marginTop: '24px',
        padding: '16px',
        backgroundColor: '#F9FAFB',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        fontSize: '0.75rem',
        color: '#6B7280'
      }}>
        <span style={{ fontWeight: 600 }}>Heat Scale:</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <div style={{ width: '40px', height: '16px', background: 'linear-gradient(90deg, rgba(59, 130, 246, 0.3), rgba(220, 38, 38, 0.9))', borderRadius: '4px' }} />
          <span>Low → High</span>
        </div>
        <span style={{ marginLeft: 'auto' }}>
          Max: <strong>{maxValue}</strong> tasks
        </span>
      </div>
    </div>
  );
};

WorkloadMatrix.defaultProps = {
  colorScale: 'heat'
};

WorkloadMatrix.propTypes = {
  id: PropTypes.string,

  /**
   * 2D array of task counts [users][stages]
   */
  data: PropTypes.arrayOf(
    PropTypes.arrayOf(PropTypes.number)
  ).isRequired,

  /**
   * Array of stage names (column headers)
   */
  stages: PropTypes.arrayOf(PropTypes.string).isRequired,

  /**
   * Array of user names (row headers)
   */
  users: PropTypes.arrayOf(PropTypes.string).isRequired,

  /**
   * Color scale type ('heat' or 'blue')
   */
  colorScale: PropTypes.oneOf(['heat', 'blue']),

  setProps: PropTypes.func
};

export default WorkloadMatrix;
