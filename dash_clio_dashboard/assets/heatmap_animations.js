/**
 * Heatmap Animations with Anime.js
 * Professional cascade and dimension-switching animations
 */

// Animation configuration
const HEATMAP_ANIMATION = {
    cascade: {
        duration: 600,
        easing: 'easeOutExpo',
        delay: anime.stagger(50, {grid: 'auto', from: 'first'})
    },
    flip: {
        duration: 400,
        easing: 'easeInOutQuad'
    },
    hover: {
        duration: 200,
        easing: 'easeOutQuad'
    }
};

/**
 * Animate heatmap entrance with cascade effect
 */
function animateHeatmapEntrance() {
    // Wait for Plotly to render
    setTimeout(() => {
        const heatmapCells = document.querySelectorAll('.animated-heatmap .heatmaplayer rect');

        if (heatmapCells.length > 0) {
            // Set initial state
            anime.set(heatmapCells, {
                opacity: 0,
                scale: 0.8
            });

            // Cascade animation
            anime({
                targets: heatmapCells,
                opacity: [0, 1],
                scale: [0.8, 1],
                delay: anime.stagger(50, {
                    grid: 'auto',
                    from: 'first'
                }),
                duration: 600,
                easing: 'easeOutExpo'
            });

            console.log('✨ Heatmap cascade animation triggered');
        }
    }, 200);  // Wait for Plotly rendering
}

/**
 * Animate dimension switch with flip effect
 */
function animateDimensionSwitch() {
    const chartContainer = document.querySelector('.animated-heatmap');

    if (!chartContainer) return;

    // Timeline for smooth transition
    anime.timeline()
        .add({
            targets: chartContainer,
            opacity: [1, 0.3],
            duration: 200,
            easing: 'easeOutQuad'
        })
        .add({
            // Data updates here (handled by Dash callback)
            duration: 100,
            complete: function() {
                console.log('🔄 Dimension switch in progress...');
            }
        })
        .add({
            targets: chartContainer,
            opacity: [0.3, 1],
            duration: 300,
            easing: 'easeOutQuad',
            complete: function() {
                // Trigger entrance animation for new cells
                animateHeatmapEntrance();
            }
        });
}

/**
 * Initialize heatmap animations
 */
function initHeatmapAnimations() {
    // Animate on initial load
    animateHeatmapEntrance();

    // Watch for dimension selector changes
    const dimensionSelector = document.querySelector('#dimension-selector');
    if (dimensionSelector) {
        // Listen for clicks on dimension buttons
        const dimensionButtons = dimensionSelector.querySelectorAll('[role="radio"]');
        dimensionButtons.forEach(button => {
            button.addEventListener('click', function() {
                console.log('📊 Dimension changed - animating transition');
                animateDimensionSwitch();
            });
        });
    }

    // Watch for chart updates (when Dash re-renders)
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                const heatmap = document.querySelector('.animated-heatmap');
                if (heatmap && heatmap.querySelectorAll('.heatmaplayer rect').length > 0) {
                    console.log('🔄 Heatmap updated - re-animating');
                    // Don't re-animate on every mutation, just on significant changes
                    // This prevents animation loops
                }
            }
        });
    });

    const contentArea = document.getElementById('dashboard-content');
    if (contentArea) {
        observer.observe(contentArea, {
            childList: true,
            subtree: true
        });
    }
}

/**
 * Add hover effects to heatmap cells (optional enhancement)
 */
function addHeatmapHoverEffects() {
    setTimeout(() => {
        const heatmapCells = document.querySelectorAll('.animated-heatmap .heatmaplayer rect');

        heatmapCells.forEach(cell => {
            cell.addEventListener('mouseenter', function() {
                anime({
                    targets: this,
                    scale: 1.1,
                    duration: 200,
                    easing: 'easeOutQuad'
                });
            });

            cell.addEventListener('mouseleave', function() {
                anime({
                    targets: this,
                    scale: 1,
                    duration: 200,
                    easing: 'easeOutQuad'
                });
            });
        });
    }, 300);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 Heatmap animations initialized');

    // Initial setup
    initHeatmapAnimations();

    // Optional: Add hover effects (can be performance-intensive with many cells)
    // addHeatmapHoverEffects();
});

// Also initialize when Dash loads the Analytics tab
window.addEventListener('load', function() {
    setTimeout(() => {
        const heatmap = document.querySelector('.animated-heatmap');
        if (heatmap) {
            console.log('🎨 Heatmap detected on page load - initializing animations');
            initHeatmapAnimations();
        }
    }, 500);
});

// Export functions for manual triggering
window.heatmapAnimations = {
    entrance: animateHeatmapEntrance,
    dimensionSwitch: animateDimensionSwitch,
    init: initHeatmapAnimations
};
