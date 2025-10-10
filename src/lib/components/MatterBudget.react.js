import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * MatterBudget - Circular progress indicator for budget tracking
 * Shows allocated vs spent with animated progress ring
 */
const MatterBudget = ({ id, allocated, spent, matterName, currency, setProps }) => {
  const percentUsed = allocated > 0 ? Math.round((spent / allocated) * 100) : 0;
  const variance = allocated - spent;
  const strokeDashoffset = 440 - (440 * Math.min(percentUsed, 100)) / 100;

  useEffect(() => {
    // Animate progress ring
    anime({
      targets: `#${id} .budget-progress`,
      strokeDashoffset: [440, strokeDashoffset],
      easing: 'easeInOutSine',
      duration: 1200
    });

    // Animate card entrance
    anime({
      targets: `#${id}`,
      opacity: [0, 1],
      scale: [0.9, 1],
      duration: 600,
      easing: 'easeOutQuad'
    });

    // Pulse warning if over budget
    if (percentUsed > 100) {
      anime({
        targets: `#${id} .budget-progress`,
        stroke: ['#DC2626', '#EF4444', '#DC2626'],
        duration: 1000,
        easing: 'easeInOutSine',
        loop: true
      });
    }
  }, [id, percentUsed, strokeDashoffset]);

  const getRingColor = () => {
    if (percentUsed > 100) return '#DC2626'; // Red - over budget
    if (percentUsed > 85) return '#F59E0B'; // Amber - warning
    if (percentUsed > 70) return '#10B981'; // Green
    return '#0070E0'; // Blue - under budget
  };

  const getStatusLabel = () => {
    if (percentUsed > 100) return { text: 'OVER BUDGET', color: '#DC2626' };
    if (percentUsed > 85) return { text: 'Near Limit', color: '#F59E0B' };
    return { text: 'On Track', color: '#10B981' };
  };

  const status = getStatusLabel();

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(amount);
  };

  return (
    <div
      id={id}
      style={{
        background: 'linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%)',
        borderRadius: '16px',
        padding: '24px',
        color: 'white',
        boxShadow: '0 8px 32px rgba(0,0,0,0.12)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        opacity: 0
      }}
    >
      {/* Matter name */}
      {matterName && (
        <div style={{
          fontSize: '0.875rem',
          fontWeight: 600,
          marginBottom: '16px',
          textAlign: 'center',
          opacity: 0.9
        }}>
          {matterName}
        </div>
      )}

      {/* Circular progress */}
      <div style={{ position: 'relative', marginBottom: '16px' }}>
        <svg width="160" height="160" style={{ transform: 'rotate(-90deg)' }}>
          {/* Background circle */}
          <circle
            cx="80"
            cy="80"
            r="70"
            stroke="rgba(255,255,255,0.2)"
            strokeWidth="12"
            fill="none"
          />
          {/* Progress circle */}
          <circle
            className="budget-progress"
            cx="80"
            cy="80"
            r="70"
            stroke={getRingColor()}
            strokeWidth="12"
            fill="none"
            strokeDasharray="440"
            strokeDashoffset="440"
            strokeLinecap="round"
          />
        </svg>

        {/* Center text */}
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '2.5rem', fontWeight: 700, lineHeight: 1 }}>
            {percentUsed}%
          </div>
          <div style={{ fontSize: '0.75rem', opacity: 0.8, marginTop: '4px' }}>
            Budget Used
          </div>
        </div>
      </div>

      {/* Status label */}
      <div style={{
        backgroundColor: status.color,
        padding: '6px 16px',
        borderRadius: '12px',
        fontSize: '0.75rem',
        fontWeight: 700,
        marginBottom: '16px',
        textTransform: 'uppercase',
        letterSpacing: '0.5px'
      }}>
        {status.text}
      </div>

      {/* Budget details */}
      <div style={{ width: '100%', borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ fontSize: '0.875rem', opacity: 0.8 }}>Allocated:</span>
          <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>
            {formatCurrency(allocated)}
          </span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
          <span style={{ fontSize: '0.875rem', opacity: 0.8 }}>Spent:</span>
          <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>
            {formatCurrency(spent)}
          </span>
        </div>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          paddingTop: '8px',
          borderTop: '1px solid rgba(255,255,255,0.2)'
        }}>
          <span style={{ fontSize: '0.875rem', fontWeight: 600 }}>
            {variance >= 0 ? 'Remaining:' : 'Over By:'}
          </span>
          <span style={{
            fontSize: '0.875rem',
            fontWeight: 700,
            color: variance >= 0 ? '#CBEA00' : '#FF6B6B'
          }}>
            {formatCurrency(Math.abs(variance))}
          </span>
        </div>
      </div>
    </div>
  );
};

MatterBudget.defaultProps = {
  currency: 'USD',
  matterName: null
};

MatterBudget.propTypes = {
  id: PropTypes.string,

  /**
   * Total budget allocated
   */
  allocated: PropTypes.number.isRequired,

  /**
   * Amount spent so far
   */
  spent: PropTypes.number.isRequired,

  /**
   * Optional matter name/description
   */
  matterName: PropTypes.string,

  /**
   * Currency code (ISO 4217)
   */
  currency: PropTypes.string,

  setProps: PropTypes.func
};

export default MatterBudget;
