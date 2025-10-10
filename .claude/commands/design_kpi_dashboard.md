🧩 Step 1: Clarify the Business Model (Domain Breakdown)

You’re essentially tracking the lifecycle of legal matters, which are your units of work.
Each matter moves through workflow stages across departments and practice areas.

Key Entities

| Entity                       | Example                                                   | Notes                         |
| ---------------------------- | --------------------------------------------------------- | ----------------------------- |
| **Matter**                   | “Smith v. Jones Auto Accident”                            | Central record                |
| **Practice Area**            | Auto Accident, Med Mal, etc.                              | 6 total                       |
| **Department**               | Intake, Prelit Front, Prelit Back, Litigation, Operations | Based on responsible_staff    |
| **Workflow Stage**           | Client Onboarding → Post-Settlement                       | Represents actual work stage  |
| **Responsible Staff / Team** | e.g., Jane Doe (Prelit Front)                             | Defines department indirectly |
| **Task Activity**            | Investigation tasks, negotiation steps                    | Time or count-based metrics   |

```
📊 Dashboard Section Design (Revised)

| Section                 | Components                                                   | Focus                               |
| ----------------------- | ------------------------------------------------------------ | ----------------------------------- |
| **Overview KPIs**       | `<AnimatedKPI />`                                            | Totals, throughput, completion rate |
| **Lifecycle View**      | `<StageProgressBar />`, `<AnimatedChartWrapper />`           | Workflow visualization              |
| **Department View**     | `<WorkloadCard />`, `<WorkloadMatrix />`                     | Staff efficiency                    |
| **Tasks & Bottlenecks** | `<TaskTracker />`, `<TaskTimeline />`, `<BottleneckRadar />` | Process control                     |
| **Financials**          | `<MatterBudget />`                                           | Budget vs. spend tracking           |


🧠 Strategic Insights (Operations-Focused KPIs)

| Metric                        | Formula                                        | Purpose                   |
| ----------------------------- | ---------------------------------------------- | ------------------------- |
| **Avg. Days per Stage**       | Σ(days_in_stage)/#matters                      | Bottleneck identification |
| **% Outstanding Tasks**       | outstanding_tasks / total_tasks                | Workload pressure         |
| **Overdue Tasks**             | due_date < today                               | Alert trigger             |
| **Budget Utilization**        | spent / allocated                              | Financial performance     |
| **Cross-Department Velocity** | stage_duration[next] - stage_duration[current] | Transition health         |


🧱 Recommended Data Pipeline

```
Clio API (matters, tasks, activities)
   ↓
Python ETL Layer (aggregate, compute KPIs)
   ↓
Dash Backend (callbacks, endpoints)
   ↓
React Frontend (Anime.js-enhanced components)
   ↓
User (smooth, actionable insights)
```
 
⚙️ Step 2: Data Tracking Design

To build insights into bottlenecks and KPIs, we need to aggregate and visualize data by:

Volume Metrics

Matters per stage

Matters per department

Matters per practice area

Velocity Metrics

Average time in stage

Average time per department

Average total lifecycle duration

Performance Metrics

Task completion rates

Staff workload distribution (open matters per staff)

Settlement-to-demand ratios (for Prelit Back)

Operational Health

Matters stuck in stage > X days

Matters with missing data or unassigned staff

Financial reconciliation completion rates (Operations)

📊 Step 3: Dashboard Architecture

We’ll split your dashboard into 4 interactive zones, each driven by a combination of Dash (Python backend) and React (frontend):

1️⃣ KPI Overview Panel

Top-level tiles for quick insights:

Total Active Matters

Avg. Days in Stage

Matters Settled (This Month)

Bottleneck % (Stage Stagnation)

Avg. Workload per Staff

💡 Anime.js Enhancement:
Each KPI tile subtly animates its number count, with fade-in and scale effects on data refresh.

2️⃣ Lifecycle Visualization (By Workflow Stage)

Interactive progress visualization:

Horizontal bar chart or Sankey flow showing # of matters per workflow stage

Clicking a stage filters data below (department breakdown, practice area mix)

💡 Anime.js Enhancement:
Stages animate smoothly on transitions — when new data loads, bars grow or shrink with easing.

3️⃣ Department & Practice Area Breakdown

Stacked bar or pie chart:

Matters grouped by practice area

Filtered by department or stage

💡 Anime.js Enhancement:
Subtle chart animations when switching filters or time ranges.
React component animates Plotly chart wrapper opacity/position.

4️⃣ Performance & Bottlenecks Section

Table + chart hybrid:

Top 10 matters “stuck” in a stage longest

Average duration per staff or per practice area

Timeline animation showing lifecycle velocity

💡 Anime.js Enhancement:
Rows fade-in sequentially; bottleneck bars pulse using accent color (#CBEA00 or #FF8C42).

🧱 Step 4: Component System (Dash + React + Anime.js)

Using your Dash Component Boilerplate:

You’ll build a reusable component library under src/lib/components/.

Each will be a React front-end component rendered in Dash as a custom Dash component.

Anime.js hooks into lifecycle methods (useEffect) for smooth transitions.

Example: Animated KPI Card

```
import React, { useEffect } from 'react';
import anime from 'animejs';

export default function KPI({ label, value }) {
  useEffect(() => {
    anime({
      targets: '.kpi-value',
      innerHTML: [0, value],
      round: 10,
      duration: 1200,
      easing: 'easeOutExpo'
    });
  }, [value]);

  return (
    <div className="kpi-card">
      <h4>{label}</h4>
      <div className="kpi-value">{value}</div>
    </div>
  );
}

```
Then use it in Dash as:

```
import dash
from dash import html
import dash_kpi  # Your custom React component package

app = dash.Dash(__name__)
app.layout = html.Div([
    dash_kpi.KPI(label="Active Matters", value=120),
])

```
🧭 Step 5: Data Design for Analytics

In your backend (Python or SQL), pre-compute metrics:

matters_per_stage

avg_days_per_stage

staff_workload_summary

bottleneck_flags

Each dataset feeds a Dash callback → React props update → Anime.js animates the transition.

🧠 Step 6: Strategic Animation Use

Keep it clean and modern:

| Animation Type | Where                    | Timing    | Easing          |
| -------------- | ------------------------ | --------- | --------------- |
| Fade + Slide   | Chart refresh / KPI load | 600ms     | `easeOutQuad`   |
| Number Count   | KPI values               | 1s        | `easeOutExpo`   |
| Color Pulse    | Bottleneck indicators    | 1.2s loop | `easeInOutSine` |
| Opacity Wave   | Scroll / section entry   | 800ms     | `easeOutCubic`  |



1️⃣ Matters

The main “parent” entity — every other element (tasks, expenses, staff, etc.) rolls up to a Matter.

2️⃣ Workflow Stages (Matter Lifecycle)

Each Matter belongs to a Workflow Stage (Client Onboarding → Post Settlement).

Each stage has a responsible department, determined by responsible_staff.

3️⃣ Tasks

Each Matter has multiple Tasks.

Tasks track operational progress and readiness to move to the next stage.

Task Fields (Clio API):

id

matter_id

name

assignee (maps to responsible_staff → department)

status ∈ {pending, in_progress, in_review, complete}

due_date

created_at, completed_at

4️⃣ Expenses / Activities (Budget Tracking)

Each Matter may have one or more activities (Clio API term for time/expenses).

These roll up into a Budget Summary:

budget_allocated

budget_spent (sum of activities with cost)

variance = budget_allocated - budget_spent

percent_used

⚙️ Data Architecture

| Data Type      | Purpose            | Frequency      | Visualization          |
| -------------- | ------------------ | -------------- | ---------------------- |
| **Matters**    | Core dataset       | Hourly sync    | Bar/Sankey             |
| **Tasks**      | Progress tracking  | Near real-time | Gantt, list, pie       |
| **Activities** | Financial tracking | Daily sync     | Progress circle, table |
| **Staff**      | Workload           | Daily sync     | KPI & distribution     |



🧠 1. <TaskTracker />

Purpose: Show all tasks for a Matter, with progress by status and animated stage transitions.

Data Props Example:
```
tasks = [
  { name: "Request police report", status: "in_progress", due_date: "2025-10-12", assignee: "Jane Doe" },
  { name: "Contact insurance", status: "pending", due_date: "2025-10-10", assignee: "Jane Doe" },
  { name: "Obtain medical bills", status: "in_review", due_date: "2025-10-14", assignee: "John Smith" }
]
```

Behavior:

Progress bar showing % complete (based on task statuses).

Pending/In Progress/In Review tasks animate in on scroll or load.

Tasks overdue pulse with accent color (lime/orange).

Smooth transitions when task status changes.

Anime.js Animation Example:
```
anime({
  targets: '.task-row.pending',
  opacity: [0, 1],
  translateX: [-20, 0],
  delay: anime.stagger(100),
  duration: 600,
  easing: 'easeOutQuad'
});

```
Dash Integration Example:

```
dash_tasktracker.TaskTracker(tasks=task_list)


```
💰 2. <MatterBudget />

Purpose: Track and visualize matter-specific budget, expenses, and remaining funds.

Data Props Example:

```
budget = {
  allocated: 5000,
  spent: 3200,
  variance: 1800,
  percent_used: 64
}


```
Behavior:

Circular progress animation for budget usage.

Subtle color shift from blue → lime/orange as usage increases.

Line animation when new expenses are added.

Tooltip hover: show latest expense entries.

Anime.js Animation Example:

```
anime({
  targets: '.budget-circle path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 1200
});

```
🗓️ 3. <TaskTimeline />

Purpose: Visualize task flow over time (like a mini-Gantt chart per Matter).

Behavior:

Each bar grows left → right as task moves from pending → complete.

Animations show task progress dynamically (based on timestamps).

Could integrate with Plotly for precise scaling, or pure SVG with Anime.js for smoothness.

🔍 4. <BottleneckRadar />

Purpose: Radar chart or circular visualization showing which stages or departments have the most “outstanding tasks” or slowest progression.

Anime.js Enhancement:

Bars grow or pulse based on % outstanding.

Accent colors highlight departments approaching critical thresholds.

💬 5. <WorkloadMatrix />

Purpose: Visual matrix showing how many tasks per staff member per stage.

Behavior:

Heatmap or grid style.

Animated fade/scale transitions as data updates.

Click to filter to that staff member’s matters/tasks.

