/*
  Dash + Anime.js Component Pack (Extended)
  ----------------------------------------
  Added components: TaskTimeline, ExpenseList, MatterTimeline.
  Built for integration with Plotly Dash Component Boilerplate.
*/

import React, { useEffect } from 'react';
import anime from 'animejs';
import Plot from 'react-plotly.js';

/* ==========================
   1️⃣ Animated KPI Component
   ========================== */
export const AnimatedKPI = ({ label, value, suffix = '', duration = 1200 }) => {
  useEffect(() => {
    anime({
      targets: `.kpi-value-${label}`,
      innerHTML: [0, value],
      round: 10,
      easing: 'easeOutExpo',
      duration: duration,
    });
  }, [value]);

  return (
    <div className="kpi-card bg-gradient-to-br from-blue-800 to-blue-600 text-white rounded-2xl p-4 shadow-lg flex flex-col items-center justify-center">
      <div className="text-sm opacity-80">{label}</div>
      <div className={`kpi-value-${label} text-3xl font-bold mt-1`}>{value}{suffix}</div>
    </div>
  );
};

/* ==============================
   2️⃣ Animated Chart Wrapper
   ============================== */
export const AnimatedChartWrapper = ({ data, layout }) => {
  useEffect(() => {
    anime({
      targets: '.plotly-chart',
      opacity: [0, 1],
      translateY: [20, 0],
      duration: 800,
      easing: 'easeOutQuad',
    });
  }, [data]);

  return <div className="plotly-chart"><Plot data={data} layout={layout} /></div>;
};

/* ==============================
   3️⃣ Task Tracker Component
   ============================== */
export const TaskTracker = ({ tasks }) => {
  useEffect(() => {
    anime({
      targets: '.task-row',
      opacity: [0, 1],
      translateX: [-20, 0],
      delay: anime.stagger(100),
      duration: 600,
      easing: 'easeOutQuad',
    });
  }, [tasks]);

  const getColor = (status) => {
    switch (status) {
      case 'complete': return 'text-green-400';
      case 'in_review': return 'text-blue-400';
      case 'in_progress': return 'text-yellow-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="task-tracker grid gap-3">
      {tasks.map((task, i) => (
        <div key={i} className={`task-row bg-white dark:bg-slate-800 p-3 rounded-xl shadow ${getColor(task.status)}`}>
          <div className="flex justify-between">
            <span className="font-medium">{task.name}</span>
            <span className="text-xs opacity-75">{task.status}</span>
          </div>
          <div className="text-xs opacity-70 mt-1">Due: {task.due_date} | {task.assignee}</div>
        </div>
      ))}
    </div>
  );
};

/* ==============================
   4️⃣ Matter Budget Component
   ============================== */
export const MatterBudget = ({ budget }) => {
  const percent = budget.percent_used;
  const strokeOffset = 440 - (440 * percent) / 100;

  useEffect(() => {
    anime({
      targets: '.budget-progress',
      strokeDashoffset: [440, strokeOffset],
      easing: 'easeInOutSine',
      duration: 1200,
    });
  }, [percent]);

  return (
    <div className="budget-card flex flex-col items-center justify-center p-6 bg-gradient-to-br from-blue-900 to-blue-700 text-white rounded-2xl shadow-lg">
      <svg className="w-24 h-24 rotate-[-90deg]">
        <circle cx="38" cy="38" r="35" stroke="#1E3A8A" strokeWidth="6" fill="none" />
        <circle className="budget-progress" cx="38" cy="38" r="35" stroke="#CBEA00" strokeWidth="6" fill="none" strokeDasharray="440" strokeDashoffset="440" />
      </svg>
      <div className="text-3xl font-bold mt-3">{percent}%</div>
      <div className="text-sm opacity-80 mt-1">Budget Used</div>
      <div className="text-xs opacity-70 mt-2">Spent ${budget.spent} / ${budget.allocated}</div>
    </div>
  );
};

/* ==============================
   5️⃣ Task Timeline Component
   ============================== */
export const TaskTimeline = ({ timeline }) => {
  useEffect(() => {
    anime({
      targets: '.timeline-bar',
      width: (el) => el.getAttribute('data-width'),
      duration: 1000,
      easing: 'easeOutCubic',
      delay: anime.stagger(150),
    });
  }, [timeline]);

  return (
    <div className="task-timeline space-y-3">
      {timeline.map((item, i) => (
        <div key={i} className="timeline-item">
          <div className="flex justify-between text-xs opacity-70 mb-1">
            <span>{item.name}</span>
            <span>{item.due_date}</span>
          </div>
          <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
            <div
              className="timeline-bar bg-gradient-to-r from-blue-500 to-blue-300 h-2 rounded-full"
              data-width={`${item.percent_complete}%`}
              style={{ width: '0%' }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
};

/* ==============================
   6️⃣ Expense List Component
   ============================== */
export const ExpenseList = ({ expenses }) => {
  useEffect(() => {
    anime({
      targets: '.expense-row',
      opacity: [0, 1],
      translateY: [20, 0],
      delay: anime.stagger(100),
      easing: 'easeOutQuad',
    });
  }, [expenses]);

  return (
    <div className="expense-list divide-y divide-slate-200 dark:divide-slate-700">
      {expenses.map((exp, i) => (
        <div key={i} className="expense-row py-2 flex justify-between">
          <div>
            <div className="font-medium text-sm">{exp.description}</div>
            <div className="text-xs opacity-70">{exp.date}</div>
          </div>
          <div className="text-sm font-semibold text-green-400">${exp.amount}</div>
        </div>
      ))}
    </div>
  );
};

/* ==============================
   7️⃣ Matter Timeline Component
   ============================== */
export const MatterTimeline = ({ stages }) => {
  useEffect(() => {
    anime({
      targets: '.matter-stage',
      opacity: [0, 1],
      translateY: [30, 0],
      delay: anime.stagger(150),
      easing: 'easeOutExpo',
    });
  }, [stages]);

  return (
    <div className="matter-timeline flex flex-col space-y-4">
      {stages.map((stage, i) => (
        <div key={i} className="matter-stage bg-white dark:bg-slate-800 p-4 rounded-xl shadow">
          <div className="flex justify-between items-center">
            <span className="font-semibold">{stage.name}</span>
            <span className="text-xs opacity-70">{stage.start_date} → {stage.end_date}</span>
          </div>
          <div className="h-2 mt-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
            <div
              className="bg-gradient-to-r from-green-400 to-lime-400 h-2"
              style={{ width: `${stage.percent_complete}%` }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
};

/* ==============================
   8️⃣ Bottleneck Radar & Workload Matrix
   ============================== */
export const BottleneckRadar = ({ data, layout }) => (
  <AnimatedChartWrapper data={data} layout={layout} />
);

export const WorkloadMatrix = ({ data, layout }) => (
  <AnimatedChartWrapper data={data} layout={layout} />
);

/* ==============================
   Export Components
   ============================== */
export default {
  AnimatedKPI,
  AnimatedChartWrapper,
  TaskTracker,
  MatterBudget,
  TaskTimeline,
  ExpenseList,
  MatterTimeline,
  BottleneckRadar,
  WorkloadMatrix,
};
