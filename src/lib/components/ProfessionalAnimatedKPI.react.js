// Enhanced Professional AnimatedKPI Component
// Builds on your existing AnimatedKPI with Mantine integration

import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * ProfessionalAnimatedKPI - Enhanced KPI card with sophisticated Mantine-style design
 * Features: Staggered animations, trend indicators, professional typography
 */
const ProfessionalAnimatedKPI = ({ 
  id, 
  label, 
  value, 
  suffix = '', 
  prefix = '', 
  duration = 1200, 
  color = '#1E3A5F', 
  trend = null,
  description = '',
  size = 'md',
  setProps 
}) => {
  const valueRef = useRef(null);
  const cardRef = useRef(null);
  const trendRef = useRef(null);
  const descRef = useRef(null);

  // Professional sizing system
  const sizes = {
    sm: { fontSize: '1.75rem', padding: '1rem' },
    md: { fontSize: '2.25rem', padding: '1.5rem' },
    lg: { fontSize: '3rem', padding: '2rem' }
  };

  useEffect(() => {
    if (!cardRef.current) return;

    // Professional card entrance with sophisticated timing
    anime({
      targets: cardRef.current,
      opacity: [0, 1],
      translateY: [30, 0],
      scale: [0.96, 1],
      duration: 600,
      easing: 'easeOutExpo',
      complete: () => {
        // Animate value after card is visible
        animateValue();
        animateTrend();
        animateDescription();
      }
    });
  }, []);

  useEffect(() => {
    if (valueRef.current && cardRef.current.style.opacity === '1') {
      animateValue();
    }
  }, [value]);

  const animateValue = () => {
    if (!valueRef.current) return;
    
    anime({
      targets: valueRef.current,
      innerHTML: [0, value],
      round: value >= 100 ? 1 : 10,
      easing: 'easeOutExpo',
      duration: duration,
      delay: 150,
      update: function(anim) {
        const val = Math.round(anim.animations[0].currentValue);
        valueRef.current.innerHTML = `${prefix}${val.toLocaleString()}${suffix}`;
      }
    });
  };

  const animateTrend = () => {
    if (!trend || !trendRef.current) return;
    
    anime({
      targets: trendRef.current,
      opacity: [0, 1],
      scale: [0.8, 1],
      translateX: [-10, 0],
      duration: 400,
      delay: 800,
      easing: 'easeOutBack'
    });
  };

  const animateDescription = () => {
    if (!description || !descRef.current) return;
    
    anime({
      targets: descRef.current,
      opacity: [0, 1],
      duration: 500,
      delay: 1000,
      easing: 'easeOutQuad'
    });
  };

  return (
    <div
      ref={cardRef}
      id={id}
      style={{
        background: 'white',
        borderRadius: '12px',
        padding: sizes[size].padding,
        border: '1px solid #E2E8F0',
        position: 'relative',
        overflow: 'hidden',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        opacity: 0
      }}
      onMouseEnter={() => {
        anime({
          targets: cardRef.current,
          scale: 1.02,
          boxShadow: '0 8px 25px rgba(30,58,95,0.15)',
          duration: 200,
          easing: 'easeOutQuad'
        });
      }}
      onMouseLeave={() => {
        anime({
          targets: cardRef.current,
          scale: 1,
          boxShadow: '0 4px 16px rgba(30,58,95,0.1)',
          duration: 200,
          easing: 'easeOutQuad'
        });
      }}
    >
      {/* Professional gradient accent */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '4px',
        background: `linear-gradient(90deg, ${color} 0%, ${color}80 100%)`
      }} />
      
      {/* Label */}
      <div style={{
        fontFamily: "'Inter', sans-serif",
        color: '#4A5568',
        fontSize: '0.875rem',
        fontWeight: 500,
        marginBottom: '0.5rem',
        textTransform: 'uppercase',
        letterSpacing: '0.05em'
      }}>
        {label}
      </div>
      
      {/* Main Value */}
      <div
        ref={valueRef}
        style={{
          fontFamily: "'Crimson Pro', serif",
          fontSize: sizes[size].fontSize,
          fontWeight: 600,
          color: '#1A202C',
          lineHeight: 1.2,
          marginBottom: description || trend ? '0.5rem' : 0
        }}
      >
        {prefix}0{suffix}
      </div>
      
      {/* Trend Indicator */}
      {trend && (
        <div
          ref={trendRef}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            padding: '0.25rem 0.5rem',
            borderRadius: '4px',
            fontSize: '0.75rem',
            fontWeight: 600,
            backgroundColor: trend > 0 ? '#F0FFF4' : '#FED7D7',
            color: trend > 0 ? '#276749' : '#9B2C2C',
            opacity: 0,
            marginBottom: description ? '0.5rem' : 0
          }}
        >
          <span style={{ marginRight: '0.25rem' }}>
            {trend > 0 ? '↗' : '↘'}
          </span>
          {Math.abs(trend)}%
        </div>
      )}
      
      {/* Description */}
      {description && (
        <div
          ref={descRef}
          style={{
            fontFamily: "'Inter', sans-serif",
            fontSize: '0.75rem',
            color: '#718096',
            lineHeight: 1.4,
            opacity: 0
          }}
        >
          {description}
        </div>
      )}
    </div>
  );
};

ProfessionalAnimatedKPI.propTypes = {
  id: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  suffix: PropTypes.string,
  prefix: PropTypes.string,
  duration: PropTypes.number,
  color: PropTypes.string,
  trend: PropTypes.number,
  description: PropTypes.string,
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  setProps: PropTypes.func
};

export default ProfessionalAnimatedKPI;