import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * BottleneckRadar - Radar/spider chart visualization for bottleneck analysis
 * Shows which stages or departments have the most outstanding tasks
 */
const BottleneckRadar = ({ id, data, maxValue, highlightThreshold, setProps }) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !data || data.length === 0) return;

    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(canvas.width, canvas.height) / 2 - 40;
    const angleStep = (2 * Math.PI) / data.length;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw grid circles
    const gridLevels = 5;
    for (let i = 1; i <= gridLevels; i++) {
      const levelRadius = (radius / gridLevels) * i;
      ctx.beginPath();
      ctx.arc(centerX, centerY, levelRadius, 0, 2 * Math.PI);
      ctx.strokeStyle = '#E5E7EB';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // Draw axes
    ctx.strokeStyle = '#D1D5DB';
    ctx.lineWidth = 1;
    data.forEach((_, idx) => {
      const angle = angleStep * idx - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();
    });

    // Animate data polygon
    const animatedValues = data.map(() => 0);

    if (animationRef.current) {
      animationRef.current.pause();
    }

    animationRef.current = anime({
      targets: animatedValues,
      '0': data.map(d => d.value),
      duration: 1200,
      easing: 'easeOutExpo',
      update: () => {
        // Clear previous drawing
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Redraw grid
        for (let i = 1; i <= gridLevels; i++) {
          const levelRadius = (radius / gridLevels) * i;
          ctx.beginPath();
          ctx.arc(centerX, centerY, levelRadius, 0, 2 * Math.PI);
          ctx.strokeStyle = '#E5E7EB';
          ctx.lineWidth = 1;
          ctx.stroke();
        }

        // Redraw axes
        ctx.strokeStyle = '#D1D5DB';
        ctx.lineWidth = 1;
        data.forEach((_, idx) => {
          const angle = angleStep * idx - Math.PI / 2;
          const x = centerX + radius * Math.cos(angle);
          const y = centerY + radius * Math.sin(angle);

          ctx.beginPath();
          ctx.moveTo(centerX, centerY);
          ctx.lineTo(x, y);
          ctx.stroke();
        });

        // Draw data polygon
        ctx.beginPath();
        animatedValues.forEach((value, idx) => {
          const angle = angleStep * idx - Math.PI / 2;
          const valueRadius = (value / maxValue) * radius;
          const x = centerX + valueRadius * Math.cos(angle);
          const y = centerY + valueRadius * Math.sin(angle);

          if (idx === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        });
        ctx.closePath();

        // Fill with gradient
        const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
        gradient.addColorStop(0, 'rgba(0, 112, 224, 0.5)');
        gradient.addColorStop(1, 'rgba(0, 112, 224, 0.1)');
        ctx.fillStyle = gradient;
        ctx.fill();

        ctx.strokeStyle = '#0070E0';
        ctx.lineWidth = 3;
        ctx.stroke();

        // Draw points
        animatedValues.forEach((value, idx) => {
          const angle = angleStep * idx - Math.PI / 2;
          const valueRadius = (value / maxValue) * radius;
          const x = centerX + valueRadius * Math.cos(angle);
          const y = centerY + valueRadius * Math.sin(angle);

          const isHighlighted = value >= highlightThreshold;

          ctx.beginPath();
          ctx.arc(x, y, isHighlighted ? 8 : 6, 0, 2 * Math.PI);
          ctx.fillStyle = isHighlighted ? '#DC2626' : '#0070E0';
          ctx.fill();
          ctx.strokeStyle = '#FFFFFF';
          ctx.lineWidth = 2;
          ctx.stroke();

          // Pulse animation for highlighted points
          if (isHighlighted) {
            ctx.beginPath();
            ctx.arc(x, y, 12, 0, 2 * Math.PI);
            ctx.strokeStyle = 'rgba(220, 38, 38, 0.3)';
            ctx.lineWidth = 2;
            ctx.stroke();
          }
        });
      }
    });

    // Draw labels
    ctx.font = 'bold 12px system-ui, -apple-system, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    data.forEach((item, idx) => {
      const angle = angleStep * idx - Math.PI / 2;
      const labelRadius = radius + 25;
      const x = centerX + labelRadius * Math.cos(angle);
      const y = centerY + labelRadius * Math.sin(angle);

      ctx.fillStyle = '#111827';
      ctx.fillText(item.label, x, y);

      // Draw value
      ctx.font = '10px system-ui, -apple-system, sans-serif';
      ctx.fillStyle = item.value >= highlightThreshold ? '#DC2626' : '#6B7280';
      ctx.fillText(`${item.value}`, x, y + 14);
      ctx.font = 'bold 12px system-ui, -apple-system, sans-serif';
    });

  }, [data, maxValue, highlightThreshold]);

  return (
    <div id={id} style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <canvas
        ref={canvasRef}
        width={400}
        height={400}
        style={{
          maxWidth: '100%',
          height: 'auto'
        }}
      />

      {/* Legend */}
      <div style={{
        marginTop: '16px',
        display: 'flex',
        gap: '24px',
        fontSize: '0.875rem',
        color: '#6B7280'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: '#0070E0'
          }} />
          Normal
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <div style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: '#DC2626'
          }} />
          Bottleneck (≥{highlightThreshold})
        </div>
      </div>
    </div>
  );
};

BottleneckRadar.defaultProps = {
  maxValue: 100,
  highlightThreshold: 10
};

BottleneckRadar.propTypes = {
  id: PropTypes.string,

  /**
   * Array of data points with {label, value}
   */
  data: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string.isRequired,
      value: PropTypes.number.isRequired
    })
  ).isRequired,

  /**
   * Maximum value for scaling
   */
  maxValue: PropTypes.number,

  /**
   * Threshold value to highlight bottlenecks
   */
  highlightThreshold: PropTypes.number,

  setProps: PropTypes.func
};

export default BottleneckRadar;
