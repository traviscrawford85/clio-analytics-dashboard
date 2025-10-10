/**
 * Professional Dashboard Layout Transition System
 * Smooth view switching with Anime.js and Mantine components
 */

import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import anime from 'animejs';

const ProfessionalViewTransition = ({ 
  id, 
  currentView, 
  views, 
  animationDuration = 600,
  setProps 
}) => {
  const containerRef = useRef(null);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [activeView, setActiveView] = useState(currentView);

  useEffect(() => {
    if (currentView !== activeView && !isTransitioning) {
      transitionToView(currentView);
    }
  }, [currentView]);

  const transitionToView = async (newView) => {
    if (isTransitioning) return;
    
    setIsTransitioning(true);
    
    // Exit animation for current view
    await animateViewExit();
    
    // Switch content
    setActiveView(newView);
    
    // Entry animation for new view
    await animateViewEntry();
    
    setIsTransitioning(false);
  };

  const animateViewExit = () => {
    return new Promise((resolve) => {
      anime({
        targets: `#${id} .view-content`,
        opacity: [1, 0],
        translateX: [0, -30],
        scale: [1, 0.98],
        duration: animationDuration * 0.6,
        easing: 'easeInQuad',
        complete: resolve
      });
    });
  };

  const animateViewEntry = () => {
    return new Promise((resolve) => {
      // Reset position for entry
      anime.set(`#${id} .view-content`, {
        opacity: 0,
        translateX: 30,
        scale: 0.98
      });

      // Animate in
      anime({
        targets: `#${id} .view-content`,
        opacity: [0, 1],
        translateX: [30, 0],
        scale: [0.98, 1],
        duration: animationDuration,
        easing: 'easeOutExpo',
        complete: resolve
      });
    });
  };

  const currentViewData = views.find(view => view.id === activeView);

  return (
    <div
      ref={containerRef}
      id={id}
      style={{
        position: 'relative',
        width: '100%',
        minHeight: '400px',
        overflow: 'hidden'
      }}
    >
      <div 
        className="view-content"
        style={{
          width: '100%',
          opacity: 1
        }}
      >
        {currentViewData && currentViewData.content}
      </div>
    </div>
  );
};

/**
 * Professional Staggered Grid Animation
 * For card grids, KPI displays, etc.
 */
const ProfessionalStaggeredGrid = ({ 
  id, 
  items, 
  columns = 3,
  gap = '1.5rem',
  staggerDelay = 100,
  animateOnMount = true,
  setProps 
}) => {
  const gridRef = useRef(null);

  useEffect(() => {
    if (animateOnMount && items.length > 0) {
      animateGridEntrance();
    }
  }, [items]);

  const animateGridEntrance = () => {
    // Set initial state
    anime.set(`#${id} .grid-item`, {
      opacity: 0,
      translateY: 30,
      scale: 0.9
    });

    // Animate in with stagger
    anime({
      targets: `#${id} .grid-item`,
      opacity: [0, 1],
      translateY: [30, 0],
      scale: [0.9, 1],
      duration: 600,
      delay: anime.stagger(staggerDelay),
      easing: 'easeOutExpo'
    });
  };

  return (
    <div
      ref={gridRef}
      id={id}
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gap: gap,
        width: '100%'
      }}
    >
      {items.map((item, index) => (
        <div
          key={index}
          className="grid-item"
          style={{
            opacity: animateOnMount ? 0 : 1
          }}
        >
          {item}
        </div>
      ))}
    </div>
  );
};

/**
 * Professional Loading State with Skeleton Animation
 */
const ProfessionalLoadingState = ({ 
  id, 
  type = 'cards', 
  count = 3,
  height = '120px',
  setProps 
}) => {
  const skeletonRef = useRef(null);

  useEffect(() => {
    animateSkeletons();
  }, []);

  const animateSkeletons = () => {
    anime({
      targets: `#${id} .skeleton-item`,
      opacity: [0.3, 0.7, 0.3],
      duration: 1500,
      loop: true,
      delay: anime.stagger(200),
      easing: 'easeInOutSine'
    });
  };

  const renderSkeletonCards = () => (
    Array.from({ length: count }, (_, index) => (
      <div
        key={index}
        className="skeleton-item"
        style={{
          backgroundColor: '#E2E8F0',
          borderRadius: '8px',
          height: height,
          opacity: 0.3
        }}
      />
    ))
  );

  const renderSkeletonTable = () => (
    <div style={{ backgroundColor: 'white', borderRadius: '8px', overflow: 'hidden' }}>
      {/* Header */}
      <div
        className="skeleton-item"
        style={{
          backgroundColor: '#EDF2F7',
          height: '48px',
          opacity: 0.3
        }}
      />
      {/* Rows */}
      {Array.from({ length: count }, (_, index) => (
        <div
          key={index}
          className="skeleton-item"
          style={{
            backgroundColor: '#F7FAFC',
            height: '56px',
            margin: '1px 0',
            opacity: 0.3
          }}
        />
      ))}
    </div>
  );

  return (
    <div ref={skeletonRef} id={id}>
      {type === 'cards' && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '1.5rem'
        }}>
          {renderSkeletonCards()}
        </div>
      )}
      {type === 'table' && renderSkeletonTable()}
    </div>
  );
};

ProfessionalViewTransition.propTypes = {
  id: PropTypes.string.isRequired,
  currentView: PropTypes.string.isRequired,
  views: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    content: PropTypes.node.isRequired
  })).isRequired,
  animationDuration: PropTypes.number,
  setProps: PropTypes.func
};

ProfessionalStaggeredGrid.propTypes = {
  id: PropTypes.string.isRequired,
  items: PropTypes.array.isRequired,
  columns: PropTypes.number,
  gap: PropTypes.string,
  staggerDelay: PropTypes.number,
  animateOnMount: PropTypes.bool,
  setProps: PropTypes.func
};

ProfessionalLoadingState.propTypes = {
  id: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['cards', 'table']),
  count: PropTypes.number,
  height: PropTypes.string,
  setProps: PropTypes.func
};

export { 
  ProfessionalViewTransition, 
  ProfessionalStaggeredGrid, 
  ProfessionalLoadingState 
};