# Animation Strategy: Anime.js for Multi-Dimensional Visualizations

## Why Anime.js for This Dashboard

**Perfect for**:
- ✅ Animating SVG paths (Sankey links, Network graph edges)
- ✅ Chart transitions (Timeline bars sliding in, Heatmap cells fading)
- ✅ Timeline sequencing (Staggered animations when switching views)
- ✅ Physics-based easing (Smooth, natural motion)
- ✅ Fine-grained control (Coordinate with Plotly updates)

**CSS handles**:
- ✅ Simple hover states (already implemented)
- ✅ Card entrance animations (already implemented)
- ✅ Basic transitions (already implemented)

---

## Animation Architecture

### 1. View Transition Flow

**When user switches tabs**:

```javascript
// Timeline: View transition sequence
anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
})
.add({
  targets: '#old-view',
  opacity: [1, 0],
  translateY: [0, -30],
  duration: 400
})
.add({
  targets: '#new-view',
  opacity: [0, 1],
  translateY: [30, 0],
  duration: 600
}, '-=200');  // Overlap by 200ms
```

**CSS (fast simple transitions)** → **Anime.js (complex sequenced transitions)**

---

## Visualization-Specific Animations

### 1. Matter Timeline (Gantt Chart)

**Entry Animation**:
```javascript
// Stagger bars from left to right
anime({
  targets: '.gantt-bar',
  width: ['0%', anime.stagger(el => el.dataset.width)],
  opacity: [0, 1],
  delay: anime.stagger(100, {start: 200}),  // 100ms delay between bars
  easing: 'easeOutElastic(1, .6)',
  duration: 1200
});
```

**Hover Animation**:
```javascript
// Lift bar on hover (subtle 3D effect)
anime({
  targets: event.target,
  translateY: -5,
  scale: 1.02,
  boxShadow: '0 8px 16px rgba(0,0,0,0.15)',
  duration: 300,
  easing: 'easeOutQuad'
});
```

**Filter Animation** (when user filters by department):
```javascript
// Shrink filtered-out bars, expand matching bars
anime({
  targets: '.gantt-bar.filtered',
  height: [anime.stagger('100%'), '20%'],
  opacity: [1, 0.3],
  duration: 600,
  easing: 'easeInOutQuad'
});
```

---

### 2. Department Flow (Sankey Diagram)

**Entry Animation**:
```javascript
// Animate Sankey links drawing in
anime({
  targets: '.sankey-link path',
  strokeDashoffset: [anime.setDashoffset, 0],
  opacity: [0, 1],
  delay: anime.stagger(150, {start: 300}),
  duration: 1500,
  easing: 'easeInOutSine'
});

// Pulse nodes after links draw
anime({
  targets: '.sankey-node',
  scale: [0.8, 1],
  opacity: [0, 1],
  delay: anime.stagger(100, {start: 1000}),
  duration: 800,
  easing: 'easeOutElastic(1, .5)'
});
```

**Flow Animation** (show matter "flowing" through departments):
```javascript
// Animated particle along Sankey link
anime({
  targets: '.flow-particle',
  translateX: [0, linkLength],
  opacity: [0, 1, 1, 0],
  keyframes: [
    { translateX: 0, opacity: 0 },
    { translateX: linkLength * 0.2, opacity: 1 },
    { translateX: linkLength * 0.8, opacity: 1 },
    { translateX: linkLength, opacity: 0 }
  ],
  duration: 3000,
  loop: true,
  easing: 'linear'
});
```

**Click Animation** (highlight path when clicking node):
```javascript
anime({
  targets: '.connected-links',
  stroke: '#FF6B6B',
  strokeWidth: [3, 6, 3],
  duration: 800,
  easing: 'easeInOutQuad'
});
```

---

### 3. Parallel Coordinates (Correlation)

**Entry Animation**:
```javascript
// Draw lines from left to right
anime({
  targets: '.parcoords-line',
  strokeDashoffset: [anime.setDashoffset, 0],
  opacity: [0, 0.6],
  delay: anime.stagger(20),
  duration: 2000,
  easing: 'easeOutExpo'
});
```

**Highlight Animation** (when user brushes/selects):
```javascript
// Highlight selected lines, fade others
anime({
  targets: '.parcoords-line.selected',
  opacity: [0.6, 1],
  strokeWidth: [1, 2.5],
  duration: 400,
  easing: 'easeOutQuad'
});

anime({
  targets: '.parcoords-line:not(.selected)',
  opacity: [0.6, 0.15],
  duration: 400,
  easing: 'easeOutQuad'
});
```

---

### 4. Workload Heatmap (Matrix)

**Entry Animation**:
```javascript
// Cascade cells from top-left to bottom-right
anime({
  targets: '.heatmap-cell',
  opacity: [0, 1],
  scale: [0.8, 1],
  delay: anime.stagger(50, {grid: [rows, cols], from: 'first'}),
  duration: 600,
  easing: 'easeOutExpo'
});
```

**Dimension Switch Animation** (when changing from Attorney × Practice Area to Attorney × Stage):
```javascript
// Flip cells to reveal new data
anime.timeline()
  .add({
    targets: '.heatmap-cell',
    rotateY: [0, 90],
    opacity: [1, 0],
    duration: 400,
    easing: 'easeInQuad'
  })
  .add({
    // Update data here (React state change)
    duration: 100
  })
  .add({
    targets: '.heatmap-cell',
    rotateY: [90, 0],
    opacity: [0, 1],
    duration: 400,
    easing: 'easeOutQuad'
  });
```

**Hover Animation**:
```javascript
// Lift cell and highlight row/column
anime({
  targets: event.target,
  scale: 1.1,
  zIndex: 10,
  duration: 200,
  easing: 'easeOutQuad'
});

anime({
  targets: '.same-row, .same-col',
  opacity: [0.6, 0.9],
  duration: 200
});
```

---

### 5. Network Graph (Relationship Map)

**Entry Animation**:
```javascript
// Nodes spring into position from center
anime({
  targets: '.network-node',
  translateX: [0, anime.stagger(el => el.dataset.targetX)],
  translateY: [0, anime.stagger(el => el.dataset.targetY)],
  scale: [0, 1],
  opacity: [0, 1],
  delay: anime.stagger(50),
  duration: 1200,
  easing: 'easeOutElastic(1, .6)'
});

// Edges draw in after nodes
anime({
  targets: '.network-edge',
  strokeDashoffset: [anime.setDashoffset, 0],
  opacity: [0, 0.4],
  delay: 1200,
  duration: 800,
  easing: 'easeOutExpo'
});
```

**Click Animation** (expand node to show connections):
```javascript
anime.timeline()
  .add({
    targets: event.target,
    scale: [1, 1.3],
    duration: 300,
    easing: 'easeOutQuad'
  })
  .add({
    targets: '.connected-nodes',
    scale: [1, 1.15],
    opacity: [0.6, 1],
    duration: 400,
    easing: 'easeOutQuad'
  }, '-=150')
  .add({
    targets: '.connected-edges',
    strokeWidth: [1, 3],
    opacity: [0.4, 0.8],
    duration: 400,
    easing: 'easeOutQuad'
  }, '-=400');
```

**Drag Animation** (smooth dragging with physics):
```javascript
// During drag
anime.remove('.dragged-node');  // Cancel ongoing animations

// On drag end (spring to final position)
anime({
  targets: '.dragged-node',
  translateX: finalX,
  translateY: finalY,
  duration: 600,
  easing: 'easeOutElastic(1, .8)'
});
```

---

## Cross-View Transition Animations

### Timeline Sequencing for View Switching

**When user clicks "Timeline" → "Flow" → "Heatmap"**:

```javascript
// Master timeline for coordinated transitions
const viewTransition = anime.timeline({
  easing: 'easeOutExpo'
});

// 1. Fade out current view
viewTransition.add({
  targets: '#current-view',
  opacity: [1, 0],
  translateY: [0, -30],
  duration: 400
});

// 2. Update content (React render)
viewTransition.add({
  complete: () => {
    // Dash callback updates view
  },
  duration: 100
});

// 3. Fade in new view
viewTransition.add({
  targets: '#new-view',
  opacity: [0, 1],
  translateY: [30, 0],
  duration: 600
}, '-=100');

// 4. Animate new view's elements
viewTransition.add({
  targets: '.new-view-element',
  opacity: [0, 1],
  translateX: [-20, 0],
  delay: anime.stagger(100),
  duration: 500
}, '-=300');
```

---

## Integration with Dash/Plotly

### React Component Pattern

**Wrap Plotly charts in Anime.js animations**:

```javascript
// dash_clio_dashboard/assets/chart_animations.js

window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    animate_chart_entrance: function(figure) {
      // Wait for Plotly to render
      setTimeout(() => {
        // Animate SVG elements
        anime({
          targets: '.plotly .scatterlayer .trace',
          opacity: [0, 1],
          delay: anime.stagger(100),
          duration: 800,
          easing: 'easeOutExpo'
        });
      }, 100);

      return figure;
    }
  }
});
```

**Dash callback with clientside animation**:

```python
# app.py

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='animate_chart_entrance'
    ),
    Output('timeline-graph', 'figure'),
    Input('timeline-graph', 'figure')
)
```

---

## Dimension Selector Animation

**When user changes dimension (e.g., "By Practice Area" → "By Attorney")**:

```javascript
// Smooth transition between data views
anime.timeline()
  .add({
    targets: '.dimension-indicator',
    translateX: indicatorPosition,
    duration: 400,
    easing: 'easeInOutQuad'
  })
  .add({
    targets: '.chart-container',
    opacity: [1, 0.3],
    duration: 200
  }, '-=400')
  .add({
    // Update data (React state)
    complete: updateData,
    duration: 100
  })
  .add({
    targets: '.chart-container',
    opacity: [0.3, 1],
    duration: 300
  });
```

---

## Performance Considerations

### Optimization Strategies

1. **Use `willChange` CSS property** for frequently animated elements:
```css
.gantt-bar, .heatmap-cell, .network-node {
  will-change: transform, opacity;
}
```

2. **Limit concurrent animations**:
```javascript
// Cancel previous animations before starting new ones
anime.remove('.chart-element');

anime({
  targets: '.chart-element',
  // ... new animation
});
```

3. **Use `requestAnimationFrame` for smooth updates**:
```javascript
anime({
  targets: '.custom-element',
  update: function(anim) {
    requestAnimationFrame(() => {
      // Update DOM here
    });
  }
});
```

4. **Reduce complexity on mobile**:
```javascript
const isMobile = window.innerWidth < 768;

anime({
  targets: '.element',
  delay: isMobile ? 0 : anime.stagger(100),  // No stagger on mobile
  duration: isMobile ? 400 : 800  // Faster on mobile
});
```

---

## Animation Configuration

### Global Easing Presets

```javascript
// dash_clio_dashboard/assets/animation_config.js

const ANIMATION_PRESETS = {
  // Quick UI feedback
  fast: {
    duration: 200,
    easing: 'easeOutQuad'
  },

  // Standard transitions
  standard: {
    duration: 400,
    easing: 'easeOutExpo'
  },

  // Dramatic entrances
  entrance: {
    duration: 800,
    easing: 'easeOutElastic(1, .6)'
  },

  // Smooth exits
  exit: {
    duration: 600,
    easing: 'easeInExpo'
  },

  // Data transitions
  data: {
    duration: 500,
    easing: 'easeInOutQuad'
  }
};
```

### Corporate Animation Timing

**Principles**:
- **Fast**: <200ms (hover feedback)
- **Standard**: 300-500ms (view transitions)
- **Slow**: 600-1000ms (complex sequences)
- **Never**: >1500ms (users perceive as lag)

**Easing for corporate feel**:
- `easeOutExpo` - Confident, decisive
- `easeInOutQuad` - Smooth, professional
- `easeOutElastic(1, .6)` - Playful but controlled
- Avoid: `easeInOutBack` (too bouncy for corporate)

---

## Implementation Plan

### Phase 1: Setup (Day 1)
- [x] Anime.js already installed
- [ ] Create `chart_animations.js` in assets/
- [ ] Set up clientside callbacks for animations
- [ ] Test basic fade-in animation

### Phase 2: Core Animations (Day 2-3)
- [ ] Implement Timeline (Gantt) animations
- [ ] Implement Flow (Sankey) animations
- [ ] Implement Heatmap animations

### Phase 3: Transitions (Day 4)
- [ ] Cross-view transition system
- [ ] Dimension selector animations
- [ ] Filter animations

### Phase 4: Polish (Day 5)
- [ ] Hover states
- [ ] Click feedback
- [ ] Loading states
- [ ] Performance testing

---

## Code Template

**Complete example for Timeline (Gantt) with Anime.js**:

```python
# layouts/timeline.py

from dash import html, dcc
import dash_mantine_components as dmc

def create_layout(COLORS):
    return html.Div([
        html.Div(id='timeline-container', children=[
            dcc.Graph(
                id='timeline-graph',
                config={'displayModeBar': False},
                className='animated-chart'
            )
        ])
    ])
```

```javascript
// assets/timeline_animations.js

// Animate chart entrance
function animateTimelineEntrance() {
  anime({
    targets: '.gantt-bar',
    width: ['0%', anime.stagger((el) => el.dataset.width)],
    opacity: [0, 1],
    delay: anime.stagger(100, {start: 200}),
    easing: 'easeOutElastic(1, .6)',
    duration: 1200
  });
}

// Hook into Plotly render
document.addEventListener('DOMContentLoaded', () => {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.addedNodes.length) {
        const chart = document.querySelector('#timeline-graph');
        if (chart && chart.querySelectorAll('.gantt-bar').length > 0) {
          animateTimelineEntrance();
          observer.disconnect();
        }
      }
    });
  });

  observer.observe(document.getElementById('timeline-container'), {
    childList: true,
    subtree: true
  });
});
```

---

## Next Steps

1. **Create base animation utilities** in `assets/chart_animations.js`
2. **Implement Timeline view** with Gantt chart + Anime.js animations
3. **Test transition smoothness** on different devices
4. **Add remaining visualizations** one by one

**Ready to start building?** Let me know which visualization to implement first!
