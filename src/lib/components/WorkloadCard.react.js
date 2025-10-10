import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * WorkloadCard - Display staff workload summary with visual indicators
 * Shows active tasks, overdue tasks, completion rate
 */
const WorkloadCard = ({ id, userName, activeTask, overdueTasks, completionRate, totalCompleted, photoUrl, setProps }) => {
  useEffect(() => {
    // Animate card entrance
    anime({
      targets: `#${id}`,
      opacity: [0, 1],
      scale: [0.95, 1],
      duration: 500,
      easing: 'easeOutBack'
    });

    // Animate progress ring
    anime({
      targets: `#${id} .completion-ring`,
      strokeDashoffset: [440, 440 - (440 * completionRate) / 100],
      duration: 1000,
      easing: 'easeInOutSine',
      delay: 200
    });
  }, [id, completionRate]);

  const getRingColor = () => {
    if (completionRate >= 80) return '#10B981'; // Green
    if (completionRate >= 60) return '#F59E0B'; // Amber
    return '#EF4444'; // Red
  };

  const getWorkloadStatus = () => {
    if (overdueTasks > 5) return { label: 'High Pressure', color: '#DC2626' };
    if (activeTask > 15) return { label: 'Busy', color: '#F59E0B' };
    return { label: 'On Track', color: '#10B981' };
  };

  const status = getWorkloadStatus();

  return (
    <div
      id={id}
      style={{
        backgroundColor: '#FFFFFF',
        borderRadius: '16px',
        padding: '20px',
        boxShadow: '0 4px 16px rgba(0,0,0,0.08)',
        border: '1px solid #E5E7EB',
        opacity: 0,
        transition: 'all 0.3s ease'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.12)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.08)';
      }}
    >
      {/* Header with photo and name */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
        <div style={{
          width: '48px',
          height: '48px',
          borderRadius: '50%',
          backgroundColor: '#E5E7EB',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.25rem',
          fontWeight: 600,
          color: '#6B7280',
          overflow: 'hidden'
        }}>
          {photoUrl ? (
            <img src={photoUrl} alt={userName} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          ) : (
            userName.charAt(0).toUpperCase()
          )}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, fontSize: '1rem', color: '#111827' }}>
            {userName}
          </div>
          <div style={{
            fontSize: '0.75rem',
            color: status.color,
            fontWeight: 600,
            marginTop: '2px'
          }}>
            {status.label}
          </div>
        </div>
      </div>

      {/* Workload metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
        <div style={{
          backgroundColor: '#F3F4F6',
          padding: '12px',
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#0070E0' }}>
            {activeTasks}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#6B7280', marginTop: '4px' }}>
            Active
          </div>
        </div>
        <div style={{
          backgroundColor: overdueTasks > 0 ? '#FEE2E2' : '#F3F4F6',
          padding: '12px',
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <div style={{
            fontSize: '1.5rem',
            fontWeight: 700,
            color: overdueTasks > 0 ? '#DC2626' : '#6B7280'
          }}>
            {overdueTasks}
          </div>
          <div style={{ fontSize: '0.75rem', color: '#6B7280', marginTop: '4px' }}>
            Overdue
          </div>
        </div>
      </div>

      {/* Completion rate ring */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div style={{ position: 'relative', width: '100px', height: '100px' }}>
          <svg width="100" height="100" style={{ transform: 'rotate(-90deg)' }}>
            <circle
              cx="50"
              cy="50"
              r="35"
              stroke="#E5E7EB"
              strokeWidth="8"
              fill="none"
            />
            <circle
              className="completion-ring"
              cx="50"
              cy="50"
              r="35"
              stroke={getRingColor()}
              strokeWidth="8"
              fill="none"
              strokeDasharray="440"
              strokeDashoffset="440"
              strokeLinecap="round"
            />
          </svg>
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#111827' }}>
              {completionRate}%
            </div>
            <div style={{ fontSize: '0.625rem', color: '#6B7280' }}>
              On-Time
            </div>
          </div>
        </div>
        <div style={{
          fontSize: '0.75rem',
          color: '#6B7280',
          marginTop: '8px'
        }}>
          {totalCompleted} tasks completed
        </div>
      </div>
    </div>
  );
};

WorkloadCard.defaultProps = {
  activeTasks: 0,
  overdueTasks: 0,
  completionRate: 0,
  totalCompleted: 0,
  photoUrl: null
};

WorkloadCard.propTypes = {
  id: PropTypes.string,

  /**
   * User/staff member name
   */
  userName: PropTypes.string.isRequired,

  /**
   * Number of active tasks
   */
  activeTasks: PropTypes.number,

  /**
   * Number of overdue tasks
   */
  overdueTasks: PropTypes.number,

  /**
   * On-time completion rate (0-100)
   */
  completionRate: PropTypes.number,

  /**
   * Total tasks completed
   */
  totalCompleted: PropTypes.number,

  /**
   * Optional profile photo URL
   */
  photoUrl: PropTypes.string,

  setProps: PropTypes.func
};

export default WorkloadCard;
