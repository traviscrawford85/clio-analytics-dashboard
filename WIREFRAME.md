🧭 Dashboard Wireframe Plan

Type: Responsive Modular Grid Layout
Style: Light/Dark theme toggle
Motion: Enhanced micro-interactions (Anime.js)
Framework: Dash + React + Anime.js

🧱 1️⃣ Header + Navigation Bar

Contents:

Logo + Firm Name (with small wave animation)

Date range selector (global filter)

Department / Practice Area dropdown filters

Theme toggle (Light 🌞 / Dark 🌚)

Animation Ideas:

Header fades in from top with slight slide (easeOutCubic)

Theme toggle glows softly on hover (accent color pulse)

💡 2️⃣ KPI Overview (Hero Row)

3–5 modular tiles across top, dynamically resizing on smaller screens.


| KPI                          | Metric | Example  | Animation                            |
| ---------------------------- | ------ | -------- | ------------------------------------ |
| Total Active Matters         | Count  | 124      | Count-up animation                   |
| Avg. Days per Stage          | Time   | 9.4 days | Count-up + background gradient shift |
| % Outstanding Tasks          | Ratio  | 31%      | Radial fill animation                |
| Matters Settled (This Month) | Count  | 18       | Fade/scale-in on refresh             |
| Avg. Workload per Staff      | Number | 22       | Count + subtle pulse                 |


Layout Note:
Each KPI card = <AnimatedKPI />
Has subtle hover tilt (3D depth, smooth reset)

🔄 3️⃣ Workflow Lifecycle Visualization

Component: <StageProgressBar /> or <LifecycleFlowChart />
Goal: Show matter count & velocity per workflow stage (1–9 stages).

Bars grow horizontally per stage count

Each stage labeled (Client Onboarding → Post Settlement)

Clicking a stage filters the rest of the dashboard

Animation:

Stage bars grow from 0% width → final count

Smooth color gradient flow (navy → soft blue → accent on hover)

🧍‍♀️ 4️⃣ Department & Practice Area Breakdown

Components:

<WorkloadMatrix /> → grid of staff vs workload

<AnimatedChartWrapper /> → stacked bar of matters per department or practice area

Filters:

Dropdowns for department / date range

Click to focus on staff or practice area

Animation:

Bars animate to new heights on data update

On-hover accent highlight with easeInOutSine color glow

📋 5️⃣ Task Tracker + Timeline

Components:

<TaskTracker /> → grouped by status (Pending, In Progress, In Review, Complete)

<TaskTimeline /> → horizontal timeline showing task progress by due date

Animation:

New tasks fade + slide in from left

Completed tasks fade out with soft color wash

Overdue tasks pulse accent color (lime/orange)

Timeline bars grow to completion %

Layout Note:
Placed below workflow section; scrollable horizontally on smaller screens

💰 6️⃣ Matter Budget & Expense Tracker

Components:

<MatterBudget /> → circular progress (budget usage)

<ExpenseList /> → latest expenses / activities

Data:

budget_allocated, spent, variance, percent_used

Linked to Clio Activities API

Animation:

Circular progress stroke animation

Color transition navy → lime as usage increases

Expenses fade-in from bottom (staggered)

⚠️ 7️⃣ Bottleneck & Health Insights

Components:

<BottleneckRadar /> → visualize stages/departments with high outstanding tasks

<AlertList /> → matters or tasks exceeding SLA / overdue

Animation:

Bars/segments grow smoothly on load

Critical areas pulse with accent color

Alert rows fade in sequentially

🧩 8️⃣ Footer / Meta Section

Contents:

Data refresh indicator (animated pulse)

API status light

Version info

Animation:

Live sync indicator using Anime timeline loop


| Area         | Primary Color    | Accent      | Motion           |
| ------------ | ---------------- | ----------- | ---------------- |
| Header / Nav | Navy             | Lime        | Fade + Slide     |
| KPI Cards    | Navy / Soft Blue | Orange      | Count + Tilt     |
| Charts       | Soft Blue        | Lime        | Bar Grow / Morph |
| Tasks        | Light Gray       | Lime        | Slide + Pulse    |
| Budget       | Navy             | Lime/Orange | Circular Sweep   |
| Bottlenecks  | Dark Blue        | Orange      | Pulse            |


🧠 Interaction Flow

User lands → Header + KPIs animate in.

Lifecycle chart animates in, displaying matter flow.

User clicks a stage → dashboard filters below (tasks, workload, budgets update).

Tasks animate (in/out), KPIs re-count.

On hover, subtle glows guide focus (accent motion).

⚙️ Technical Layout
Layer	Tech	Notes

| Layer      | Tech                                   | Notes                                        |
| ---------- | -------------------------------------- | -------------------------------------------- |
| UI         | React + Tailwind (in Dash boilerplate) | Modular grid with responsive breakpoints     |
| Animations | Anime.js                               | Controlled by data updates + scroll triggers |
| Charts     | Plotly.js / Plotly React               | Inside `<AnimatedChartWrapper />`            |
| Data       | Dash callbacks / Clio API              | JSON endpoints feeding props                 |
| Theme      | Light/Dark via Tailwind + CSS vars     | `useTheme()` toggle hook                     |
