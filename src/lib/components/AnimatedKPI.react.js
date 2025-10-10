import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * AnimatedKPI - A sleek KPI card with animated number count-up
 * Ideal for dashboard overview metrics
 */
const AnimatedKPI = ({ id, label, value, suffix, prefix, duration, color, setProps }) => {
  const valueRef = useRef(null);

  useEffect(() => {
    if (valueRef.current) {
      // Animate number count
      anime({
        targets: valueRef.current,
        innerHTML: [0, value],
        round: value >= 100 ? 1 : 10,
        easing: 'easeOutExpo',
        duration: duration,
        update: function(anim) {
          const val = Math.round(anim.animations[0].currentValue);
          valueRef.current.innerHTML = `${prefix}${val}${suffix}`;
        }
      });

      // Animate card entrance
      anime({
        targets: `#${id}`,
        opacity: [0, 1],
        translateY: [20, 0],
        duration: 600,
        easing: 'easeOutQuad'
      });
    }
  }, [value, duration, suffix, prefix, id]);

  return (
    <div
      id={id}
      className="kpi-card"
      style={{
        background: `linear-gradient(135deg, ${color}dd 0%, ${color}99 100%)`,
        borderRadius: '16px',
        padding: '24px',
        color: 'white',
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '140px',
        opacity: 0
      }}
    >
      <div
        style={{
          fontSize: '0.875rem',
          opacity: 0.85,
          fontWeight: 500,
          letterSpacing: '0.5px',
          textTransform: 'uppercase',
          marginBottom: '8px'
        }}
      >
        {label}
      </div>
      <div
        ref={valueRef}
        style={{
          fontSize: '2.5rem',
          fontWeight: 700,
          lineHeight: 1
        }}
      >
        {prefix}{value}{suffix}
      </div>
    </div>
  );
};

AnimatedKPI.defaultProps = {
  suffix: '',
  prefix: '',
  duration: 1200,
  color: '#0070E0'
};

AnimatedKPI.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks.
   */
  id: PropTypes.string,

  /**
   * The label displayed above the value
   */
  label: PropTypes.string.isRequired,

  /**
   * The numeric value to display
   */
  value: PropTypes.number.isRequired,

  /**
   * Optional suffix (e.g., '%', 'M')
   */
  suffix: PropTypes.string,

  /**
   * Optional prefix (e.g., '$', '€')
   */
  prefix: PropTypes.string,

  /**
   * Animation duration in milliseconds
   */
  duration: PropTypes.number,

  /**
   * Primary color (hex)
   */
  color: PropTypes.string,

  /**
   * Dash-assigned callback that should be called to report property changes
   * to Dash, to make them available for callbacks.
   */
  setProps: PropTypes.func
};

export default AnimatedKPI;
