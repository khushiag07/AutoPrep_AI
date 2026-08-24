import {
  Upload,
  BarChart3,
  Brain,
  Sparkles,
  ShieldCheck,
  Cpu,
  GitCompare,
  FileText,
} from "lucide-react";

const stages = [
  {
    id: "upload",
    label: "Upload Dataset",
    icon: Upload,
  },
  {
    id: "profiler",
    label: "Profiler",
    icon: BarChart3,
  },
  {
    id: "intelligence",
    label: "Intelligence",
    icon: Brain,
  },
  {
    id: "cleaning",
    label: "Cleaning",
    icon: Sparkles,
  },
  {
    id: "validation",
    label: "Validation",
    icon: ShieldCheck,
  },
  {
    id: "readiness",
    label: "ML Readiness",
    icon: Cpu,
  },
  {
    id: "models",
    label: "Model Selection",
    icon: GitCompare,
  },
  {
    id: "report",
    label: "Final Report",
    icon: FileText,
  },
];

export default function PipelineSidebar({
  activeStage,
  setActiveStage,
  completedStages = [],
}) {
  return (
    <aside className="pipeline-sidebar">

      <div className="sidebar-title">
        <div className="sidebar-logo">
          AI
        </div>

        <div>
          <h2>DataFlow</h2>
          <span>ML Pipeline</span>
        </div>
      </div>


      <div className="pipeline-label">
        PIPELINE
      </div>


      <nav className="pipeline-nav">

        {stages.map((stage, index) => {

          const Icon = stage.icon;

          const active =
            activeStage === stage.id;

          const completed =
            completedStages.includes(stage.id);

          return (
            <button
              key={stage.id}
              className={`pipeline-item ${
                active ? "active" : ""
              }`}
              onClick={() =>
                setActiveStage(stage.id)
              }
            >

              <div
                className={`stage-number ${
                  active
                    ? "active-number"
                    : completed
                    ? "completed-number"
                    : ""
                }`}
              >
                {completed ? "✓" : index + 1}
              </div>


              <Icon
                size={17}
                strokeWidth={1.8}
              />


              <span>
                {stage.label}
              </span>

            </button>
          );
        })}

      </nav>


      <div className="sidebar-bottom">

        <div className="pipeline-status">
          <span className="status-dot" />

          <div>
            <strong>Pipeline Active</strong>
            <small>Ready for analysis</small>
          </div>
        </div>

      </div>

    </aside>
  );
}