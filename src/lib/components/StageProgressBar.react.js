import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * StageProgressBar - Horizontal progress bar showing matter distribution across stages
 * Supports click interaction to filter by stage
 */
const StageProgressBar = ({ id, stages, onStageClick, colorScheme, setProps }) => {
  const [selectedStage, setSelectedStage] = useState(null);

  useEffect(() => {
    // Animate bars on mount or data change
    anime({
      targets: '.stage-bar-segment',
      width: (el) => el.getAttribute('data-width'),
      opacity: [0, 1],
      delay: anime.stagger(80),
      duration: 800,
      easing: 'easeInOutQuad'
    });
  }, [stages]);

  const total = stages.reduce((sum, stage) => sum + stage.count, 0);

  const handleStageClick = (stageName) => {
    setSelectedStage(stageName);
    if (setProps) {
      setProps({ selectedStage: stageName });
    }
  };

  const getColor = (index) => {
    const colors = colorScheme || [
      '#0070E0', '#04304C', '#87CEEB', '#018b76',
      '#D74417', '#F4A540', '#CBEA00', '#6B7280'
    ];
    return colors[index % colors.length];
  };

  return (
    <div id={id} style={{ width: '100%' }}>
      {/* Stage labels */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.75rem', color: '#6B7280' }}>
        {stages.map((stage, idx) => (
          <div key={idx} style={{ textAlign: 'center', flex: stage.count / total }}>
            <div style={{ fontWeight: 600 }}>{stage.name}</div>
            <div style={{ opacity: 0.7 }}>{stage.count}</div>
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div style={{
        display: 'flex',
        height: '48px',
        borderRadius: '12px',
        overflow: 'hidden',
        boxShadow: '0 4px 12px rgba(0,0,0,0.08)'
      }}>
        {stages.map((stage, idx) => {
          const percentage = (stage.count / total) * 100;
          const isSelected = selectedStage === stage.name;

          return (
            <div
              key={idx}
              className="stage-bar-segment"
              data-width={`${percentage}%`}
              onClick={() => handleStageClick(stage.name)}
              style={{
                width: '0%',
                backgroundColor: getColor(idx),
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                opacity: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                fontWeight: 600,
                fontSize: '0.875rem',
                transform: isSelected ? 'scale(1.05)' : 'scale(1)',
                filter: isSelected ? 'brightness(1.2)' : 'brightness(1)',
                boxShadow: isSelected ? '0 0 0 3px rgba(255,255,255,0.3)' : 'none'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.filter = 'brightness(1.15)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.filter = isSelected ? 'brightness(1.2)' : 'brightness(1)';
              }}
            >
              {percentage > 8 && `${Math.round(percentage)}%`}
            </div>
          );
        })}
      </div>

      {/* Selected stage indicator */}
      {selectedStage && (
        <div style={{
          marginTop: '12px',
          padding: '8px 16px',
          backgroundColor: '#F3F4F6',
          borderRadius: '8px',
          fontSize: '0.875rem',
          color: '#374151'
        }}>
          <strong>Filtering by:</strong> {selectedStage}
          <button
            onClick={() => handleStageClick(null)}
            style={{
              marginLeft: '12px',
              padding: '4px 8px',
              fontSize: '0.75rem',
              backgroundColor: 'white',
              border: '1px solid #D1D5DB',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Clear
          </button>
        </div>
      )}
    </div>
  );
};

StageProgressBar.defaultProps = {
  colorScheme: null,
  onStageClick: null
};

StageProgressBar.propTypes = {
  id: PropTypes.string,

  /**
   * Array of stage objects with {name, count, order}
   */
  stages: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      count: PropTypes.number.isRequired,
      order: PropTypes.number
    })
  ).isRequired,

  /**
   * Callback when a stage is clicked
   */
  onStageClick: PropTypes.func,

  /**
   * Custom color scheme (array of hex colors)
   */
  colorScheme: PropTypes.arrayOf(PropTypes.string),

  /**
   * Currently selected stage (for filtering)
   */
  selectedStage: PropTypes.string,

  setProps: PropTypes.func
};

export default StageProgressBar;
