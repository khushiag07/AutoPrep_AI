import { useState } from "react";
import {
  Upload,
  FileSpreadsheet,
  Database,
  CheckCircle,
  Loader2,
  ArrowRight,
  X,
} from "lucide-react";

import "./App.css";
import PipelineSidebar from "./components/PipelineSidebar";


function App() {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [stage, setStage] = useState("upload");
  const [result, setResult] = useState(null);
  const [activeStage, setActiveStage] =
  useState("upload");
  const completedStages = [];

if (result) {
  completedStages.push(
    "upload",
    "profiler",
    "intelligence",
    "cleaning",
    "validation"
  );
}


  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    const validExtensions = [
      "csv",
      "xlsx",
      "xls",
    ];

    const extension =
      selectedFile.name
        .split(".")
        .pop()
        .toLowerCase();

    if (!validExtensions.includes(extension)) {
      alert("Please upload a CSV or Excel file.");
      return;
    }

    setFile(selectedFile);
    setStage("upload");
  };


  const handleDrop = (event) => {
    event.preventDefault();

    setDragging(false);

    const droppedFile =
      event.dataTransfer.files[0];

    handleFile(droppedFile);
  };


  const removeFile = () => {
    setFile(null);
    setStage("upload");
  };


const processFile = async () => {
  if (!file) return;

  setProcessing(true);
  setStage("profiling");

  try {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
      "http://127.0.0.1:8000/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error(
        `Server error: ${response.status}`
      );
    }

    const data = await response.json();

    console.log(
      "Backend response:",
      data
    );


    if (!data.success) {
      throw new Error(
        data.error || "Processing failed"
      );
    }


   setResult(data);

setStage("cleaning");
setActiveStage("cleaning");

setTimeout(() => {

  setStage("validation");
  setActiveStage("validation");

  setTimeout(() => {

    setStage("complete");
    setActiveStage("profiler");

    setProcessing(false);

  }, 800);

}, 800);


  } catch (error) {

    console.error(
      "Upload failed:",
      error
    );

    alert(
      `Upload failed: ${error.message}`
    );

    setProcessing(false);
    setStage("upload");
  }
};


   return (
  <div className="app">

    <PipelineSidebar
      activeStage={activeStage}
      setActiveStage={setActiveStage}
      completedStages={completedStages}
    />

    <div className="app-main">

      <header className="header">
    


        <div className="brand">

          <div className="brand-icon">
            <Database size={22} />
          </div>

          <div>
            <h1>AutoPrep AI</h1>

            <p>
              Intelligent Data Preparation
            </p>
          </div>

        </div>


        <div className="system-status">

          <span className="status-dot"></span>

          Pipeline Ready

        </div>

      </header>


      {/* ================= MAIN ================= */}
      
      <main className="container">


        {/* HERO */}

        <section className="hero">

          <div className="eyebrow">
            AI DATA PREPARATION PLATFORM
          </div>

          <h2>
            Turn messy data into
            <span>ML-ready data.</span>
          </h2>

          <p className="hero-description">

            Upload your dataset and AutoPrep AI
            will profile, clean and validate
            your data before it reaches your
            machine-learning pipeline.

          </p>

        </section>


        {/* ================= UPLOAD ================= */}

        {!file && (

          <section
            className={`upload-container ${
              dragging ? "dragging" : ""
            }`}

            onDragOver={(event) => {
              event.preventDefault();
              setDragging(true);
            }}

            onDragLeave={() => {
              setDragging(false);
            }}

            onDrop={handleDrop}
          >

            <div className="upload-icon">
              <Upload size={30} />
            </div>

            <h3>
              Upload your dataset
            </h3>

            <p>
              Drag & drop your CSV or Excel file
              here
            </p>


            <label className="browse-button">

              Browse files

              <input
                type="file"
                hidden
                accept=".csv,.xlsx,.xls"
                onChange={(event) =>
                  handleFile(
                    event.target.files[0]
                  )
                }
              />

            </label>


            <div className="supported">
              CSV · XLSX · XLS
            </div>

          </section>

        )}


        {/* ================= FILE ================= */}

        {file && (

          <section className="file-card">

            <div className="file-left">

              <div className="file-icon">
                <FileSpreadsheet size={26} />
              </div>

              <div>

                <h3>
                  {file.name}
                </h3>

                <p>
                  {(file.size / 1024 / 1024)
                    .toFixed(2)} MB
                </p>

              </div>

            </div>


            <button
              className="remove-button"
              onClick={removeFile}
              disabled={processing}
            >
              <X size={18} />
            </button>

          </section>

        )}


        {/* ================= PROCESS BUTTON ================= */}

        {file && stage === "upload" && (

          <button
            className="process-button"
            onClick={processFile}
          >

            Analyze Dataset

            <ArrowRight size={19} />

          </button>

        )}


        {/* ================= PIPELINE ================= */}

        {(processing || stage === "complete") && (

          <section className="pipeline-card">

            <div className="pipeline-header">

              <div>
                <h3>
                  Data Preparation Pipeline
                </h3>

                <p>
                  Processing your dataset
                </p>
              </div>

            </div>


            <PipelineStage
              title="Data Profiling"
              description="Analyzing structure and quality"
              active={stage === "profiling"}
              complete={[
                "cleaning",
                "validation",
                "complete",
              ].includes(stage)}
            />


            <PipelineStage
              title="Data Cleaning"
              description="Handling data quality issues"
              active={stage === "cleaning"}
              complete={[
                "validation",
                "complete",
              ].includes(stage)}
            />


            <PipelineStage
              title="Validation"
              description="Verifying the cleaned dataset"
              active={stage === "validation"}
              complete={
                stage === "complete"
              }
            />

          </section>

        )}


        {/* ================= SUCCESS ================= */}

        {stage === "complete" && (

          <section className="success-card">

            <div className="success-icon">
              <CheckCircle size={28} />
            </div>

            <div>

              <h3>
                Dataset successfully processed
              </h3>

              <p>
                Your dataset passed the
                preparation pipeline.
              </p>

            </div>

          </section>

        )}
       {stage === "complete" && result && (

  <div className="dashboard-content">

    {activeStage === "profiler" && (
      <ProfileDashboard result={result} />
    )}

    {activeStage === "intelligence" && (
      <IntelligenceDashboard result={result} />
    )}

    {activeStage === "cleaning" && (
      <CleaningDashboard result={result} />
    )}

    {activeStage === "validation" && (
      <ValidationDashboard result={result} />
    )}

    {activeStage === "upload" && (
      <section className="stage-placeholder">

        <h2>Upload Dataset</h2>

        <p>
          Upload your dataset to begin the
          data preparation pipeline.
        </p>

      </section>
    )}

    {activeStage === "readiness" && (
      <section className="stage-placeholder">

        <h2>ML Readiness</h2>

        <p>
          Coming next...
        </p>

      </section>
    )}

    {activeStage === "models" && (
      <section className="stage-placeholder">

        <h2>Model Selection</h2>

        <p>
          Coming next...
        </p>

      </section>
    )}

    {activeStage === "report" && (
      <section className="stage-placeholder">

        <h2>Final Report</h2>

        <p>
          Coming next...
        </p>

      </section>
    )}

  </div>
)}
      </main>

    </div>
    </div>
  );
}



/* ================================================= */
/* PIPELINE STAGE                                   */
/* ================================================= */

function PipelineStage({
  title,
  description,
  active,
  complete,
}) {

  return (

    <div className="pipeline-stage">

      <div
        className={`stage-icon ${
          complete
            ? "complete"
            : active
            ? "active"
            : ""
        }`}
      >

        {complete ? (

          <CheckCircle size={20} />

        ) : active ? (

          <Loader2
            size={20}
            className="spinner"
          />

        ) : (

          <Database size={20} />

        )}

      </div>


      <div className="stage-content">

        <h4>
          {title}
        </h4>

        <p>
          {description}
        </p>

      </div>

    </div>

  );
}
function CleaningDashboard({ result }) {

  if (!result?.cleaning) {
    return null;
  }

  const cleaning = result.cleaning;

  const auditLog = cleaning.audit_log || [];

  return (
    <section className="cleaning-dashboard">

      <div className="cleaning-header">

        <div>
          <span className="dashboard-label">
            DATA CLEANING
          </span>

          <h3>
            Cleaning Results
          </h3>

          <p>
            Safe cleaning operations applied to
            your dataset.
          </p>
        </div>

      </div>


      {/* BEFORE / AFTER */}

      <div className="cleaning-stats">

        <div className="cleaning-stat">

          <span>Rows Before</span>

          <strong>
            {cleaning.original_rows}
          </strong>

        </div>


        <div className="cleaning-arrow">
          →
        </div>


        <div className="cleaning-stat">

          <span>Rows After</span>

          <strong>
            {cleaning.cleaned_rows}
          </strong>

        </div>


        <div className="cleaning-stat">

          <span>Columns</span>

          <strong>
            {cleaning.cleaned_columns}
          </strong>

        </div>

      </div>


      {/* AUDIT LOG */}

      <div className="audit-section">

        <div className="audit-title">
          Cleaning Audit Log
        </div>


        {auditLog.length === 0 ? (

          <div className="no-cleaning">

            ✓ No cleaning operations were required.

          </div>

        ) : (

          auditLog.map((item, index) => (

            <div
              className="audit-card"
              key={index}
            >

              <div>

                <strong>
                  {formatCleaningOperation(
                    item.operation
                  )}
                </strong>

                {item.column && (

                  <span className="audit-column">
                    {item.column}
                  </span>

                )}

              </div>


              <div className="audit-details">

                {item.values_filled !== undefined && (

                  <span>
                    {item.values_filled} values filled
                  </span>

                )}

                {item.rows_removed !== undefined && (

                  <span>
                    {item.rows_removed} rows removed
                  </span>

                )}

                {item.rows_changed !== undefined && (

                  <span>
                    {item.rows_changed} rows changed
                  </span>

                )}

                {item.outliers_modified !== undefined && (

                  <span>
                    {item.outliers_modified} outliers modified
                  </span>

                )}

              </div>

            </div>

          ))

        )}

      </div>

    </section>
  );
}
function ValidationDashboard({ result }) {

  if (!result?.validation) {
    return null;
  }

  const validation = result.validation;

  const checks = validation.checks || [];

  return (
    <section className="validation-dashboard">

      {/* HEADER */}

      <div className="validation-header">

        <div>

          <span className="dashboard-label">
            DATA VALIDATION
          </span>

          <h3>
            Validation Report
          </h3>

          <p>
            Verifying that cleaning improved the
            dataset without damaging its structure.
          </p>

        </div>


        {/* SCORE */}

        <div className="validation-score">

          <strong>
            {validation.validation_score}
          </strong>

          <span>
            / 100
          </span>

        </div>

      </div>


      {/* STATUS */}

      <div
        className={
          validation.status === "PASSED"
            ? "validation-status passed"
            : "validation-status review"
        }
      >

        {validation.status === "PASSED"
          ? "✓ Dataset passed validation"
          : "⚠ Dataset needs review"
        }

      </div>


      {/* CHECKS */}

      <div className="validation-checks">

        {checks.map((check, index) => (

          <div
            className="validation-check"
            key={index}
          >

            <div className="check-left">

              <div
                className={
                  check.status === "PASS"
                    ? "check-icon pass"
                    : "check-icon fail"
                }
              >

                {check.status === "PASS"
                  ? "✓"
                  : "!"
                }

              </div>


              <div>

                <strong>
                  {check.check}
                </strong>

                {/* BEFORE / AFTER */}

                {check.before !== undefined && (
                  <div className="check-values">

                    Before: {check.before}

                    <span>→</span>

                    After: {check.after}

                  </div>
                )}

              </div>

            </div>


            <span
              className={
                check.status === "PASS"
                  ? "check-status pass-text"
                  : "check-status fail-text"
              }
            >

              {check.status}

            </span>

          </div>

        ))}

      </div>

    </section>
  );
}

function ProfileDashboard({ result }) {

  if (!result?.profile) {
    return null;
  }

  const profile = result.profile;

  const dataset = profile.dataset;
  const quality = profile.quality;
  const columns = profile.columns || [];
  const outliers = profile.outliers || [];

  const issueCount =
    quality.missing_cells +
    quality.duplicate_rows +
    outliers.reduce(
      (total, item) => total + item.count,
      0
    );

  let healthScore = 100;

  if (quality.missing_percentage > 0) {
    healthScore -= Math.min(
      quality.missing_percentage * 2,
      30
    );
  }

  if (quality.duplicate_percentage > 0) {
    healthScore -= Math.min(
      quality.duplicate_percentage * 2,
      20
    );
  }

  if (outliers.length > 0) {
    healthScore -= Math.min(
      outliers.length * 3,
      20
    );
  }

  healthScore = Math.max(
    0,
    Math.round(healthScore)
  );


  return (
    <section className="profile-dashboard">

      <div className="dashboard-header">

        <div>
          <span className="dashboard-label">
            DATASET PROFILE
          </span>

          <h3>
            {result.filename}
          </h3>
        </div>

        <div className="health-score">
          <strong>
            {healthScore}
          </strong>

          <span>/100</span>

          <small>
            Data Health
          </small>
        </div>

      </div>


      {/* SUMMARY */}

      <div className="metric-grid">

        <Metric
          label="Rows"
          value={dataset.rows}
        />

        <Metric
          label="Columns"
          value={dataset.columns}
        />

        <Metric
          label="Missing"
          value={quality.missing_cells}
        />

        <Metric
          label="Duplicates"
          value={quality.duplicate_rows}
        />

        <Metric
          label="Outlier Columns"
          value={outliers.length}
        />

      </div>


      {/* COLUMN TABLE */}

      <div className="table-section">

        <h4>
          Column Analysis
        </h4>

        <div className="table-wrapper">

          <table>

            <thead>

              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Missing</th>
                <th>Unique</th>
                <th>Status</th>
              </tr>

            </thead>


            <tbody>

              {columns.map((column) => {

                const hasMissing =
                  column.missing > 0;

                return (

                  <tr key={column.name}>

                    <td>
                      {column.name}
                    </td>

                    <td>
                      <span className="type-badge">
                        {column.dtype}
                      </span>
                    </td>

                    <td>
                      {column.missing}
                    </td>

                    <td>
                      {column.unique}
                    </td>

                    <td>

                      {hasMissing ? (

                        <span className="warning">
                          ⚠ Needs attention
                        </span>

                      ) : (

                        <span className="healthy">
                          ✓ Healthy
                        </span>

                      )}

                    </td>

                  </tr>

                );

              })}

            </tbody>

          </table>

        </div>

      </div>


      {/* ISSUES */}

      <div className="issues-section">

        <h4>
          Detected Issues
        </h4>


        {quality.missing_cells > 0 && (

          <div className="issue">
            ⚠ {quality.missing_cells} missing
            values detected
          </div>

        )}


        {quality.duplicate_rows > 0 && (

          <div className="issue">
            ⚠ {quality.duplicate_rows} duplicate
            rows detected
          </div>

        )}


        {outliers.length > 0 && (

          <div className="issue">

            ⚠ Potential outliers detected
            in {outliers.length} columns

          </div>

        )}


        {issueCount === 0 && (

          <div className="healthy-message">

            ✓ No major data quality issues
            detected.

          </div>

        )}

      </div>

    </section>
  );
}
function IntelligenceDashboard({ result }) {

  if (!result?.intelligence) {
    return null;
  }

  const intelligence = result.intelligence;

  const recommendations =
    intelligence.recommendations || [];

  const summary =
    intelligence.summary || {};


  return (
    <section className="intelligence-dashboard">

      <div className="intelligence-header">

        <div>

          <span className="dashboard-label">
            AI DATA INTELLIGENCE
          </span>

          <h3>
            Recommended Actions
          </h3>

          <p>
            The system analyzed the profiling
            results and generated these
            recommendations.
          </p>

        </div>

        <div className="issue-count">

          <strong>
            {summary.total_issues || 0}
          </strong>

          <span>
            issues
          </span>

        </div>

      </div>


      {/* SUMMARY */}

      <div className="intelligence-summary">

        <div>
          <span>High</span>
          <strong>
            {summary.high || 0}
          </strong>
        </div>

        <div>
          <span>Medium</span>
          <strong>
            {summary.medium || 0}
          </strong>
        </div>

        <div>
          <span>Low</span>
          <strong>
            {summary.low || 0}
          </strong>
        </div>

      </div>


      {/* RECOMMENDATIONS */}

      <div className="recommendations">

        {recommendations.length === 0 ? (

          <div className="no-issues">

            ✓ No data quality actions
            recommended.

          </div>

        ) : (

          recommendations.map(
            (item, index) => (

              <div
                className="recommendation-card"
                key={index}
              >

                <div className="recommendation-top">

                  <div>

                    <span
                      className={`severity ${item.severity}`}
                    >
                      {item.severity}
                    </span>

                    <h4>
                      {item.issue}
                    </h4>

                  </div>

                  {item.column && (

                    <span className="column-name">
                      {item.column}
                    </span>

                  )}

                </div>


                <div className="recommendation-action">

                  <span>
                    Recommended action
                  </span>

                  <strong>
                    {formatAction(item.action)}
                  </strong>

                </div>


                <div className="recommendation-reason">

                  <span>
                    Why?
                  </span>

                  <p>
                    {item.reason}
                  </p>

                </div>

              </div>

            )
          )

        )}

      </div>

    </section>
  );
}

function Metric({ label, value }) {

  return (
    <div className="metric">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}
function formatCleaningOperation(operation) {

  const names = {

    remove_duplicates:
      "Duplicate rows removed",

    missing_value_imputation:
      "Missing values imputed",

    category_normalization:
      "Categories normalized",

    outlier_capping:
      "Outliers capped",

    outlier_review_required:
      "Outliers flagged for review"
  };

  return names[operation] || operation;
}

function formatAction(action) {

  const actions = {

    impute:
      "Impute missing values",

    remove_duplicates:
      "Remove duplicate rows",

    review_outliers:
      "Review outliers",

    review:
      "Review column",

    review_or_drop:
      "Review or consider removing column"
  };

  return (
    actions[action] ||
    action
  );
}

export default App;