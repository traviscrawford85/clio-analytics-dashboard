import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * TaskTimeline - Mini Gantt-style timeline showing task progression
 * Displays tasks with horizontal bars representing duration/progress
 */
const TaskTimeline = ({ id, tasks, showProgress, setProps }) => {
  useEffect(() => {
    // Animate timeline bars growing from left to right
    anime({
      targets: '.timeline-bar',
      width: (el) => el.getAttribute('data-width'),
      duration: 1000,
      easing: 'easeOutCubic',
      delay: anime.stagger(150)
    });

    // Animate item entrance
    anime({
      targets: '.timeline-item',
      opacity: [0, 1],
      translateY: [10, 0],
      duration: 500,
      easing: 'easeOutQuad',
      delay: anime.stagger(80)
    });
  }, [tasks]);

  const getBarColor = (status) => {
    const colors = {
      complete: '#10B981',
      in_progress: '#F59E0B',
      pending: '#6B7280',
      overdue: '#DC2626'
    };
    return colors[status] || colors.pending;
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const calculateDaysUntilDue = (dueDate) => {
    if (!dueDate) return null;
    const today = new Date();
    const due = new Date(dueDate);
    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  return (
    <div id={id} style={{ width: '100%' }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '16px',
        paddingBottom: '8px',
        borderBottom: '2px solid #E5E7EB'
      }}>
        <span style={{ fontSize: '0.875rem', fontWeight: 600, color: '#374151' }}>
          Task
        </span>
        <span style={{ fontSize: '0.875rem', fontWeight: 600, color: '#374151' }}>
          Due Date
        </span>
      </div>

      {/* Timeline items */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {tasks.map((task, idx) => {
          const daysUntil = calculateDaysUntilDue(task.due_date);
          const isOverdue = daysUntil !== null && daysUntil < 0;
          const taskStatus = isOverdue ? 'overdue' : task.status;

          return (
            <div
              key={idx}
              className="timeline-item"
              style={{
                opacity: 0
              }}
            >
              {/* Task name and due date */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '6px'
              }}>
                <div style={{
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  color: '#111827',
                  flex: 1
                }}>
                  {task.name}
                </div>
                <div style={{
                  fontSize: '0.75rem',
                  color: isOverdue ? '#DC2626' : '#6B7280',
                  fontWeight: isOverdue ? 600 : 400,
                  marginLeft: '8px'
                }}>
                  {formatDate(task.due_date)}
                  {daysUntil !== null && (
                    <span style={{ marginLeft: '4px' }}>
                      ({daysUntil < 0 ? `${Math.abs(daysUntil)}d overdue` : `${daysUntil}d left`})
                    </span>
                  )}
                </div>
              </div>

              {/* Progress bar track */}
              <div style={{
                width: '100%',
                height: '20px',
                backgroundColor: '#F3F4F6',
                borderRadius: '10px',
                overflow: 'hidden',
                position: 'relative'
              }}>
                {/* Progress bar */}
                <div
                  className="timeline-bar"
                  data-width={`${showProgress ? task.percent_complete || 0 : 100}%`}
                  style={{
                    width: '0%',
                    height: '100%',
                    background: `linear-gradient(90deg, ${getBarColor(taskStatus)} 0%, ${getBarColor(taskStatus)}dd 100%)`,
                    borderRadius: '10px',
                    transition: 'all 0.3s ease',
                    position: 'relative',
                    overflow: 'hidden'
                  }}
                >
                  {/* Animated shimmer effect */}
                  {task.status === 'in_progress' && (
                    <div style={{
                      position: 'absolute',
                      top: 0,
                      left: '-100%',
                      width: '100%',
                      height: '100%',
                      background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent)',
                      animation: 'shimmer 2s infinite'
                    }} />
                  )}
                </div>

                {/* Percentage label */}
                {showProgress && task.percent_complete > 0 && (
                  <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '8px',
                    transform: 'translateY(-50%)',
                    fontSize: '0.6875rem',
                    fontWeight: 700,
                    color: task.percent_complete > 40 ? '#FFFFFF' : '#374151'
                  }}>
                    {task.percent_complete}%
                  </div>
                )}
              </div>

              {/* Assignee info */}
              {task.assignee && (
                <div style={{
                  fontSize: '0.75rem',
                  color: '#9CA3AF',
                  marginTop: '4px'
                }}>
                  👤 {task.assignee}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {tasks.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '32px',
          color: '#9CA3AF',
          fontSize: '0.875rem'
        }}>
          No tasks in timeline
        </div>
      )}

      <style>
        {`
          @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
          }
        `}
      </style>
    </div>
  );
};

TaskTimeline.defaultProps = {
  showProgress: true
};

TaskTimeline.propTypes = {
  id: PropTypes.string,

  /**
   * Array of timeline tasks
   */
  tasks: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      status: PropTypes.oneOf(['pending', 'in_progress', 'complete']),
      due_date: PropTypes.string,
      assignee: PropTypes.string,
      percent_complete: PropTypes.number
    })
  ).isRequired,

  /**
   * Whether to show progress percentage
   */
  showProgress: PropTypes.bool,

  setProps: PropTypes.func
};

export default TaskTimeline;
