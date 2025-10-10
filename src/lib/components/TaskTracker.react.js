import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

/**
 * TaskTracker - Display tasks with status indicators and animated entrance
 * Shows task name, due date, assignee, and status with appropriate styling
 */
const TaskTracker = ({ id, tasks, highlightOverdue, setProps }) => {
  useEffect(() => {
    // Stagger animation for task rows
    anime({
      targets: '.task-row',
      opacity: [0, 1],
      translateX: [-20, 0],
      delay: anime.stagger(100),
      duration: 600,
      easing: 'easeOutQuad'
    });

    // Pulse animation for overdue tasks
    if (highlightOverdue) {
      anime({
        targets: '.task-row-overdue',
        backgroundColor: ['#FEE2E2', '#FCA5A5', '#FEE2E2'],
        duration: 1200,
        easing: 'easeInOutSine',
        loop: true
      });
    }
  }, [tasks, highlightOverdue]);

  const getStatusColor = (status) => {
    const statusMap = {
      complete: { bg: '#D1FAE5', text: '#065F46', label: 'Complete' },
      in_review: { bg: '#DBEAFE', text: '#1E40AF', label: 'In Review' },
      in_progress: { bg: '#FEF3C7', text: '#92400E', label: 'In Progress' },
      pending: { bg: '#E5E7EB', text: '#374151', label: 'Pending' }
    };
    return statusMap[status] || statusMap.pending;
  };

  const isOverdue = (dueDate) => {
    if (!dueDate) return false;
    return new Date(dueDate) < new Date();
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'No due date';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div id={id} style={{ display: 'grid', gap: '12px' }}>
      {tasks.map((task, idx) => {
        const status = getStatusColor(task.status);
        const overdue = isOverdue(task.due_date);

        return (
          <div
            key={idx}
            className={`task-row ${overdue && highlightOverdue ? 'task-row-overdue' : ''}`}
            style={{
              backgroundColor: overdue && highlightOverdue ? '#FEE2E2' : '#FFFFFF',
              padding: '16px',
              borderRadius: '12px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
              border: overdue && highlightOverdue ? '2px solid #DC2626' : '1px solid #E5E7EB',
              opacity: 0,
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 16px rgba(0,0,0,0.12)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.06)';
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: '0.9375rem', color: '#111827', marginBottom: '4px' }}>
                  {task.name}
                </div>
                <div style={{ fontSize: '0.8125rem', color: '#6B7280', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                  <span>📅 {formatDate(task.due_date)}</span>
                  {task.assignee && <span>👤 {task.assignee}</span>}
                  {task.matter && <span>⚖️ {task.matter}</span>}
                </div>
              </div>
              <div
                style={{
                  backgroundColor: status.bg,
                  color: status.text,
                  padding: '4px 12px',
                  borderRadius: '12px',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  whiteSpace: 'nowrap'
                }}
              >
                {status.label}
              </div>
            </div>

            {overdue && highlightOverdue && (
              <div style={{
                fontSize: '0.75rem',
                color: '#DC2626',
                fontWeight: 600,
                marginTop: '8px',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                ⚠️ OVERDUE
              </div>
            )}
          </div>
        );
      })}

      {tasks.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '32px',
          color: '#9CA3AF',
          fontSize: '0.875rem'
        }}>
          No tasks to display
        </div>
      )}
    </div>
  );
};

TaskTracker.defaultProps = {
  highlightOverdue: true
};

TaskTracker.propTypes = {
  id: PropTypes.string,

  /**
   * Array of task objects
   */
  tasks: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      status: PropTypes.oneOf(['pending', 'in_progress', 'in_review', 'complete']).isRequired,
      due_date: PropTypes.string,
      assignee: PropTypes.string,
      matter: PropTypes.string
    })
  ).isRequired,

  /**
   * Whether to highlight and pulse overdue tasks
   */
  highlightOverdue: PropTypes.bool,

  setProps: PropTypes.func
};

export default TaskTracker;
