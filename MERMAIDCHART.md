flowchart TD

%% === LAYOUT STRUCTURE ===
A[Header / Navbar]:::nav --> B[KPI Overview Row]:::kpi
B --> C[Workflow Lifecycle Visualization]:::flow
C --> D[Department & Practice Area Breakdown]:::dept
D --> E[Task Tracking + Timeline]:::tasks
E --> F[Matter Budget & Expenses]:::budget
F --> G[Bottleneck & Health Insights]:::bottle
G --> H[Footer / Meta Section]:::footer

%% === HEADER ===
subgraph A1[Header / Navbar]
A1a[Logo + Firm Name (Animated Wave)]
A1b[Date Range Selector]
A1c[Department / Practice Area Filters]
A1d[Theme Toggle (Light/Dark)]
end

A --> A1

%% === KPI OVERVIEW ===
subgraph B1[KPI Overview]
B1a[<AnimatedKPI> Total Active Matters]
B1b[<AnimatedKPI> Avg. Days per Stage]
B1c[<AnimatedKPI> % Outstanding Tasks]
B1d[<AnimatedKPI> Matters Settled (Month)]
B1e[<AnimatedKPI> Avg. Workload per Staff]
end

B --> B1

%% === WORKFLOW LIFECYCLE ===
subgraph C1[Workflow Lifecycle Visualization]
C1a[<StageProgressBar> by Stage]
C1b[<LifecycleFlowChart>]
C1 --> C1a
C1 --> C1b
end

C --> C1

%% === DEPARTMENT + PRACTICE AREA ===
subgraph D1[Department & Practice Area Breakdown]
D1a[<WorkloadMatrix> Staff vs Workload]
D1b[<AnimatedChartWrapper> Matters per Department / Area]
end

D --> D1

%% === TASK TRACKER + TIMELINE ===
subgraph E1[Task Management]
E1a[<TaskTracker> Task List by Status]
E1b[<TaskTimeline> Task Progress Over Time]
end

E --> E1

%% === MATTER BUDGET ===
subgraph F1[Matter Budget & Expenses]
F1a[<MatterBudget> Budget Usage Gauge]
F1b[<ExpenseList> Latest Expenses / Activities]
end

F --> F1

%% === BOTTLENECKS + HEALTH ===
subgraph G1[Bottleneck & Health Insights]
G1a[<BottleneckRadar> Stage/Dept Bottlenecks]
G1b[<AlertList> Overdue Matters / Tasks]
end

G --> G1

%% === FOOTER ===
subgraph H1[Footer / Meta]
H1a[Data Refresh Indicator (Anime Loop)]
H1b[API Status Light]
H1c[Version Info]
end

H --> H1

%% === ANIMATION & STYLE NOTES ===
classDef nav fill:#032059,stroke:#CBEA00,color:#fff,stroke-width:2px;
classDef kpi fill:#3A558C,stroke:#FF8C42,color:#fff,stroke-width:2px;
classDef flow fill:#96B9FF,stroke:#032059,color:#000,stroke-width:2px;
classDef dept fill:#C4D4F2,stroke:#032059,color:#000,stroke-width:2px;
classDef tasks fill:#EBEFF2,stroke:#FF8C42,color:#000,stroke-width:2px;
classDef budget fill:#032059,stroke:#CBEA00,color:#fff,stroke-width:2px;
classDef bottle fill:#3A558C,stroke:#FF8C42,color:#fff,stroke-width:2px;
classDef footer fill:#0E1626,stroke:#96B9FF,color:#fff,stroke-width:2px;
