import { useState } from "react";
import ReactFlow, { Background, Controls, MiniMap } from "reactflow";
import "reactflow/dist/style.css";

const API = "http://127.0.0.1:8001";

function App() {
  const [view, setView] = useState("dashboard");
  const [repoUrl, setRepoUrl] = useState("");
  const [changedFile, setChangedFile] = useState("");
  const [changedFunction, setChangedFunction] = useState("");
  const [change, setChange] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [graph, setGraph] = useState(null);
  const [graphLoading, setGraphLoading] = useState(false);
  const [graphError, setGraphError] = useState("");

  const simulate = async () => {
    setError("");
    setResult(null);

    if (!repoUrl.trim()) {
      return setError("Please enter a GitHub repository URL.");
    }

    if (!changedFile.trim()) {
      return setError("Please enter the file you want to change.");
    }

    if (!change.trim()) {
      return setError("Please describe the proposed change.");
    }

    setLoading(true);

    try {
      const response = await fetch(`${API}/simulate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          repo_url: repoUrl.trim(),
          changed_file: changedFile.trim(),
          change_description: change.trim(),
          changed_function: changedFunction.trim() || null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Simulation failed.");
      }

      setResult(data);
      setView("results");
    } catch (err) {
      setError(
        err.message || "Could not connect to ProjectTwin API."
      );
    } finally {
      setLoading(false);
    }
  };

  const loadGraph = async () => {
    setGraphError("");

    if (!repoUrl.trim()) {
      setGraphError(
        "Enter a GitHub repository URL first."
      );
      setView("graph");
      return;
    }

    setGraphLoading(true);

    try {
      const response = await fetch(`${API}/graph`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          repo_url: repoUrl.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Could not load dependency graph."
        );
      }

      setGraph(data);
      setView("graph");
    } catch (err) {
      setGraphError(
        err.message ||
          "Could not connect to ProjectTwin API."
      );
      setView("graph");
    } finally {
      setGraphLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError("");
    setView("dashboard");
  };

  return (
    <div style={styles.app}>
      <aside style={styles.sidebar}>
        <div style={styles.brand}>
          <div style={styles.logo}>PT</div>

          <div>
            <div style={styles.brandName}>
              ProjectTwin
            </div>

            <div style={styles.brandSub}>
              AI Digital Twin
            </div>
          </div>
        </div>

        <div style={styles.navTitle}>
          WORKSPACE
        </div>

        <Nav
          active={view === "dashboard"}
          onClick={() => setView("dashboard")}
          icon="⌂"
        >
          Dashboard
        </Nav>

        <Nav
          active={
            view === "simulate" ||
            view === "results"
          }
          onClick={() => setView("simulate")}
          icon="◈"
        >
          Change Simulation
        </Nav>

        <Nav
          active={view === "graph"}
          onClick={loadGraph}
          icon="⌘"
        >
          Dependency Graph
        </Nav>

        <div style={styles.sidebarBottom}>
          <div style={styles.statusDot} />

          <div>
            <div style={styles.statusText}>
              SYSTEM READY
            </div>

            <div style={styles.statusSub}>
              Simulation engine online
            </div>
          </div>
        </div>
      </aside>

      <main style={styles.main}>
        <header style={styles.header}>
          <div>
            <div style={styles.eyebrow}>
              SOFTWARE CHANGE INTELLIGENCE
            </div>

            <h1 style={styles.title}>
              {view === "graph"
                ? "Dependency Graph"
                : view === "results"
                ? "Simulation Results"
                : view === "simulate"
                ? "Change Simulation"
                : "Project Overview"}
            </h1>
          </div>

          <div style={styles.headerBadge}>
            DIGITAL TWIN
          </div>
        </header>

        {error && <Alert message={error} />}

        {graphError && view === "graph" && (
          <Alert message={graphError} />
        )}

        {view === "dashboard" && (
          <Dashboard
            onStart={() => setView("simulate")}
            onGraph={loadGraph}
          />
        )}

        {view === "simulate" && (
          <SimulationForm
            repoUrl={repoUrl}
            setRepoUrl={setRepoUrl}
            changedFile={changedFile}
            setChangedFile={setChangedFile}
            changedFunction={changedFunction}
            setChangedFunction={setChangedFunction}
            change={change}
            setChange={setChange}
            loading={loading}
            onSimulate={simulate}
          />
        )}

        {view === "results" && result && (
          <Results
            result={result}
            onBack={() => setView("simulate")}
            onNew={reset}
          />
        )}

        {view === "graph" && (
          <GraphView
            data={graph}
            loading={graphLoading}
          />
        )}
      </main>
    </div>
  );
}

function Nav({
  active,
  onClick,
  icon,
  children,
}) {
  return (
    <button
      onClick={onClick}
      style={{
        ...styles.nav,
        ...(active ? styles.navActive : {}),
      }}
    >
      <span style={styles.navIcon}>
        {icon}
      </span>

      {children}
    </button>
  );
}

function Alert({ message }) {
  return (
    <div style={styles.alert}>
      ⚠ {message}
    </div>
  );
}

function Dashboard({ onStart, onGraph }) {
  return (
    <div>
      <section style={styles.hero}>
        <div>
          <div style={styles.heroKicker}>
            PREDICT BEFORE YOU CHANGE
          </div>

          <h2 style={styles.heroTitle}>
            Understand the impact of a software
            change before touching the real project.
          </h2>

          <p style={styles.heroText}>
            ProjectTwin analyzes repository
            structure, dependencies, functions and
            Git history, then simulates the likely
            consequences of a proposed change.
          </p>

          <div style={styles.heroButtons}>
            <button
              style={styles.primary}
              onClick={onStart}
            >
              Start Change Simulation →
            </button>

            <button
              style={styles.secondary}
              onClick={onGraph}
            >
              Explore Dependency Graph
            </button>
          </div>
        </div>

        <div style={styles.heroOrb}>
          <div style={styles.orbInner}>
            PT
          </div>
        </div>
      </section>

      <div style={styles.cardGrid}>
        <Feature
          title="Change Impact"
          text="Find direct and indirect files affected by a proposed change."
          icon="◈"
        />

        <Feature
          title="Function Relationships"
          text="Trace function-level dependencies across the project."
          icon="ƒ"
        />

        <Feature
          title="Git Intelligence"
          text="Use file history as evidence for the simulation."
          icon="↗"
        />

        <Feature
          title="AI Reasoning"
          text="Turn project evidence into a clear change-impact explanation."
          icon="✦"
        />
      </div>

      <section style={styles.infoCard}>
        <div>
          <div style={styles.cardLabel}>
            CORE PRINCIPLE
          </div>

          <h3 style={styles.cardTitle}>
            The repository is never modified by
            the simulation.
          </h3>

          <p style={styles.cardText}>
            The result is hypothetical. ProjectTwin
            separates evidence from predictions so
            developers can inspect consequences
            before implementing a real change.
          </p>
        </div>

        <div style={styles.flowMini}>
          <span>Repository</span>
          <b>→</b>
          <span>Analysis</span>
          <b>→</b>
          <span>Simulation</span>
          <b>→</b>
          <span>Prediction</span>
        </div>
      </section>
    </div>
  );
}

function Feature({ title, text, icon }) {
  return (
    <div style={styles.feature}>
      <div style={styles.featureIcon}>
        {icon}
      </div>

      <h3 style={styles.featureTitle}>
        {title}
      </h3>

      <p style={styles.featureText}>
        {text}
      </p>
    </div>
  );
}

function SimulationForm({
  repoUrl,
  setRepoUrl,
  changedFile,
  setChangedFile,
  changedFunction,
  setChangedFunction,
  change,
  setChange,
  loading,
  onSimulate,
}) {
  return (
    <section style={styles.panel}>
      <div style={styles.panelHeader}>
        <div>
          <div style={styles.cardLabel}>
            HYPOTHETICAL CHANGE
          </div>

          <h2 style={styles.panelTitle}>
            Simulate a proposed repository change
          </h2>
        </div>

        <div style={styles.stepBadge}>
          01 / INPUT
        </div>
      </div>

      <Field
        label="GitHub Repository"
        hint="Public repository URL"
      >
        <input
          style={styles.input}
          value={repoUrl}
          onChange={(e) =>
            setRepoUrl(e.target.value)
          }
          placeholder="https://github.com/psf/requests"
        />
      </Field>

      <div style={styles.twoCol}>
        <Field
          label="Changed File"
          hint="Project-relative path"
        >
          <input
            style={styles.input}
            value={changedFile}
            onChange={(e) =>
              setChangedFile(e.target.value)
            }
            placeholder="src/requests/utils.py"
          />
        </Field>

        <Field
          label="Changed Function"
          hint="Optional; leave blank for whole file"
        >
          <input
            style={styles.input}
            value={changedFunction}
            onChange={(e) =>
              setChangedFunction(e.target.value)
            }
            placeholder="function_name"
          />
        </Field>
      </div>

      <Field
        label="Proposed Change"
        hint="Describe what you want to happen"
      >
        <textarea
          style={styles.textarea}
          value={change}
          onChange={(e) =>
            setChange(e.target.value)
          }
          placeholder="Remove this file from the project"
        />
      </Field>

      <div style={styles.simulationNote}>
        This is a hypothetical simulation. The
        actual GitHub repository will not be modified.
      </div>

      <button
        style={styles.primaryWide}
        onClick={onSimulate}
        disabled={loading}
      >
        {loading
          ? "Analyzing project..."
          : "Run Change Simulation →"}
      </button>
    </section>
  );
}

function Field({
  label,
  hint,
  children,
}) {
  return (
    <label style={styles.field}>
      <span style={styles.fieldTop}>
        <b>{label}</b>
        <small>{hint}</small>
      </span>

      {children}
    </label>
  );
}

function ImpactList({ title, items, empty }) {
  return (
    <div
      style={{
        marginTop: "18px",
        background: "#15151f",
        border: "1px solid #2a2a3a",
        borderRadius: "14px",
        padding: "20px",
      }}
    >
      <div
        style={{
          fontSize: "13px",
          fontWeight: "800",
          color: "#ffffff",
          marginBottom: "14px",
        }}
      >
        {title}
      </div>

      {!items || items.length === 0 ? (
        <div
          style={{
            color: "#77778f",
            fontSize: "13px",
          }}
        >
          {empty}
        </div>
      ) : (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "8px",
          }}
        >
          {items.map((item, index) => {
            const text =
              typeof item === "string"
                ? item
                : item?.file || item?.path || JSON.stringify(item);

            return (
              <div
                key={index}
                style={{
                  padding: "10px 12px",
                  borderRadius: "8px",
                  background: "#101018",
                  color: "#d8d8e5",
                  fontSize: "13px",
                  wordBreak: "break-word",
                }}
              >
                {text}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
function ImpactEvidence({ dependencyImpact }) {
  if (!dependencyImpact) {
    return null;
  }

  const direct = dependencyImpact.direct_impact || [];
  const indirect = dependencyImpact.indirect_impact_details || [];
  const confidence = dependencyImpact.confidence || {};

  return (
    <section style={styles.subsection}>
      <h3 style={styles.sectionTitle}>
        Impact Evidence
      </h3>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "12px",
          marginBottom: "16px",
        }}
      >
        <div
          style={{
            padding: "12px",
            borderRadius: "9px",
            background: "#0b0c10",
            border: "1px solid rgba(52, 211, 153, 0.2)",
          }}
        >
          <div
            style={{
              color: "#6ee7b7",
              fontSize: "9px",
              fontWeight: 800,
              letterSpacing: "1px",
              marginBottom: "6px",
            }}
          >
            DIRECT CONFIDENCE
          </div>

          <div
            style={{
              color: "#d1fae5",
              fontSize: "13px",
              fontWeight: 700,
            }}
          >
            {confidence.direct || "PROVEN"}
          </div>
        </div>

        <div
          style={{
            padding: "12px",
            borderRadius: "9px",
            background: "#0b0c10",
            border: "1px solid rgba(167, 139, 250, 0.2)",
          }}
        >
          <div
            style={{
              color: "#a78bfa",
              fontSize: "9px",
              fontWeight: 800,
              letterSpacing: "1px",
              marginBottom: "6px",
            }}
          >
            INDIRECT CONFIDENCE
          </div>

          <div
            style={{
              color: "#ddd6fe",
              fontSize: "13px",
              fontWeight: 700,
            }}
          >
            {confidence.indirect || "LIKELY"}
          </div>
        </div>
      </div>

      <div
        style={{
          padding: "15px",
          borderRadius: "10px",
          background: "#0b0c10",
          border: "1px solid #20222a",
          marginBottom: "10px",
        }}
      >
        <div
          style={{
            color: "#6ee7b7",
            fontSize: "10px",
            fontWeight: 800,
            letterSpacing: "1px",
            marginBottom: "10px",
          }}
        >
          DIRECT IMPACT
        </div>

        {direct.length === 0 ? (
          <div style={styles.muted}>
            No direct impact detected.
          </div>
        ) : (
          direct.map((item, index) => (
            <div
              key={index}
              style={{
                padding: "10px",
                marginBottom: "7px",
                borderRadius: "8px",
                background: "#111218",
              }}
            >
              <div
                style={{
                  color: "#e5e7eb",
                  fontSize: "12px",
                  fontWeight: 700,
                }}
              >
                {item.source_file}
              </div>

              {item.source_symbol && (
                <div
                  style={{
                    color: "#a78bfa",
                    fontSize: "11px",
                    marginTop: "4px",
                  }}
                >
                  {item.source_symbol}() →{" "}
                  {item.target_symbol || dependencyImpact.changed_symbol || "changed component"}
                </div>
              )}

              <div
                style={{
                  color: "#777b89",
                  fontSize: "10px",
                  marginTop: "5px",
                }}
              >
                {item.evidence || "Dependency relationship detected."}
              </div>

              <div
                style={{
                  color: "#6ee7b7",
                  fontSize: "9px",
                  fontWeight: 800,
                  marginTop: "6px",
                }}
              >
                ✓ {item.confidence || "PROVEN"}
              </div>
            </div>
          ))
        )}
      </div>

      <div
        style={{
          padding: "15px",
          borderRadius: "10px",
          background: "#0b0c10",
          border: "1px solid #20222a",
        }}
      >
        <div
          style={{
            color: "#a78bfa",
            fontSize: "10px",
            fontWeight: 800,
            letterSpacing: "1px",
            marginBottom: "10px",
          }}
        >
          INDIRECT IMPACT
        </div>

        {indirect.length === 0 ? (
          <div style={styles.muted}>
            No indirect impact detected.
          </div>
        ) : (
          indirect.map((item, index) => (
            <div
              key={index}
              style={{
                padding: "10px",
                marginBottom: "7px",
                borderRadius: "8px",
                background: "#111218",
              }}
            >
              <div
                style={{
                  color: "#e5e7eb",
                  fontSize: "12px",
                  fontWeight: 700,
                }}
              >
                {item.source_file}
              </div>

              <div
                style={{
                  color: "#777b89",
                  fontSize: "10px",
                  marginTop: "5px",
                  lineHeight: 1.5,
                }}
              >
                {item.evidence}
              </div>

              {item.dependency_chain && (
                <div
                  style={{
                    color: "#8b8f9d",
                    fontSize: "10px",
                    marginTop: "6px",
                  }}
                >
                  Chain:{" "}
                  {item.dependency_chain.join(" → ")}
                </div>
              )}

              <div
                style={{
                  color: "#c4b5fd",
                  fontSize: "9px",
                  fontWeight: 800,
                  marginTop: "6px",
                }}
              >
                {item.confidence || "LIKELY"}
              </div>
            </div>
          ))
        )}
      </div>
    </section>
  );
}

function ConsequencePrediction({ consequences }) {
  if (!consequences || consequences.length === 0) {
    return null;
  }

  return (
    <section style={styles.subsection}>
      <h3 style={styles.sectionTitle}>
        Predicted Consequences
      </h3>

      <div
        style={{
          padding: "14px",
          borderRadius: "10px",
          background: "#0b0c10",
          border: "1px solid #20222a",
        }}
      >
        <div
          style={{
            color: "#fbbf24",
            fontSize: "10px",
            fontWeight: 800,
            letterSpacing: "1px",
            marginBottom: "12px",
          }}
        >
          WHAT MAY HAPPEN IF THIS CHANGE IS APPLIED
        </div>

        {consequences.map((item, index) => (
          <div
            key={index}
            style={{
              padding: "12px",
              marginBottom:
                index === consequences.length - 1
                  ? "0"
                  : "8px",
              borderRadius: "8px",
              background: "#111218",
              border: "1px solid #1d2028",
            }}
          >
            {/* TYPE + SEVERITY */}
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: "10px",
                marginBottom: "7px",
              }}
            >
              <div
                style={{
                  color: "#e5e7eb",
                  fontSize: "12px",
                  fontWeight: 800,
                }}
              >
                {item.type || "CONSEQUENCE"}
              </div>

              <div
                style={{
                  color:
                    item.severity === "HIGH"
                      ? "#fca5a5"
                      : "#fcd34d",
                  fontSize: "9px",
                  fontWeight: 800,
                  letterSpacing: "0.8px",
                }}
              >
                {item.severity || "POTENTIAL"}
              </div>
            </div>

            {/* AFFECTED COMPONENT */}
            <div
              style={{
                color: "#9ca3af",
                fontSize: "10px",
                marginBottom: "6px",
              }}
            >
              {item.file}
              {item.function
                ? ` · ${item.function}()`
                : ""}
            </div>

            {/* REASON */}
            <div
              style={{
                color: "#d1d5db",
                fontSize: "11px",
                lineHeight: 1.55,
                marginBottom:
                  item.predicted_effects ||
                  item.recommended_checks
                    ? "12px"
                    : "0",
              }}
            >
              {item.reason}
            </div>

            {/* PREDICTED EFFECTS */}
            {item.predicted_effects &&
              item.predicted_effects.length > 0 && (
                <div
                  style={{
                    marginTop: "10px",
                    padding: "10px",
                    borderRadius: "8px",
                    background: "#0d0f14",
                    border: "1px solid #1d2028",
                  }}
                >
                  <div
                    style={{
                      color: "#fbbf24",
                      fontSize: "9px",
                      fontWeight: 800,
                      letterSpacing: "0.8px",
                      marginBottom: "7px",
                    }}
                  >
                    PREDICTED EFFECTS
                  </div>

                  {item.predicted_effects.map(
                    (effect, effectIndex) => (
                      <div
                        key={effectIndex}
                        style={{
                          color: "#cbd5e1",
                          fontSize: "10px",
                          lineHeight: 1.5,
                          marginBottom:
                            effectIndex ===
                            item.predicted_effects.length - 1
                              ? "0"
                              : "4px",
                        }}
                      >
                        • {effect}
                      </div>
                    )
                  )}
                </div>
              )}

            {/* RECOMMENDED CHECKS */}
            {item.recommended_checks &&
              item.recommended_checks.length > 0 && (
                <div
                  style={{
                    marginTop: "8px",
                    padding: "10px",
                    borderRadius: "8px",
                    background: "#0d0f14",
                    border: "1px solid #1d2028",
                  }}
                >
                  <div
                    style={{
                      color: "#86efac",
                      fontSize: "9px",
                      fontWeight: 800,
                      letterSpacing: "0.8px",
                      marginBottom: "7px",
                    }}
                  >
                    RECOMMENDED CHECKS
                  </div>

                  {item.recommended_checks.map(
                    (check, checkIndex) => (
                      <div
                        key={checkIndex}
                        style={{
                          color: "#cbd5e1",
                          fontSize: "10px",
                          lineHeight: 1.5,
                          marginBottom:
                            checkIndex ===
                            item.recommended_checks.length - 1
                              ? "0"
                              : "4px",
                        }}
                      >
                        ✓ {check}
                      </div>
                    )
                  )}
                </div>
              )}
          </div>
        ))}
      </div>
    </section>
  );
}

function Metric({ label, value }) {
  return (
    <div
      style={{
        background: "#15151f",
        border: "1px solid #2a2a3a",
        borderRadius: "14px",
        padding: "20px",
      }}
    >
      <div
        style={{
          fontSize: "11px",
          fontWeight: "700",
          letterSpacing: "1.5px",
          color: "#8f8fa8",
          marginBottom: "10px",
        }}
      >
        {label}
      </div>

      <div
        style={{
          fontSize: "24px",
          fontWeight: "800",
          color: "#ffffff",
        }}
      >
        {value}
      </div>
    </div>
  );
}

function FeatureImpact({
  featureImpact,
  repositoryFeatureMap,
}) {
  if (!featureImpact || featureImpact.length === 0) {
    return null;
  }

  return (
    <section style={styles.subsection}>
      <h3 style={styles.sectionTitle}>
        Feature Impact
      </h3>

      <div
        style={{
          padding: "14px",
          borderRadius: "10px",
          background: "#0b0c10",
          border: "1px solid #20222a",
        }}
      >
        <div
          style={{
            color: "#60a5fa",
            fontSize: "10px",
            fontWeight: 800,
            letterSpacing: "1px",
            marginBottom: "12px",
          }}
        >
          POTENTIALLY AFFECTED FEATURES
        </div>

        {featureImpact.map((impact, index) => (
          <div
            key={index}
            style={{
              padding: "12px",
              marginBottom:
                index === featureImpact.length - 1
                  ? "0"
                  : "8px",
              borderRadius: "8px",
              background: "#111218",
              border: "1px solid #1d2028",
            }}
          >
            <div
              style={{
                color: "#e5e7eb",
                fontSize: "12px",
                fontWeight: 800,
              }}
            >
              {impact.feature}
            </div>

            <div
              style={{
                display: "flex",
                gap: "8px",
                marginTop: "8px",
                flexWrap: "wrap",
              }}
            >
              <span
                style={{
                  padding: "4px 7px",
                  borderRadius: "5px",
                  background: "#171922",
                  color: "#fbbf24",
                  fontSize: "9px",
                  fontWeight: 800,
                  letterSpacing: "0.5px",
                }}
              >
                {impact.impact_level}
              </span>

              <span
                style={{
                  padding: "4px 7px",
                  borderRadius: "5px",
                  background: "#171922",
                  color: "#a78bfa",
                  fontSize: "9px",
                  fontWeight: 800,
                  letterSpacing: "0.5px",
                }}
              >
                {impact.confidence}
              </span>
            </div>

            <div
              style={{
                color: "#9ca3af",
                fontSize: "10px",
                lineHeight: 1.5,
                marginTop: "10px",
              }}
            >
              {impact.predicted_effect}
            </div>

            <div
              style={{
                color: "#6b7280",
                fontSize: "10px",
                lineHeight: 1.5,
                marginTop: "8px",
              }}
            >
              {impact.relationship}
            </div>

            <div
              style={{
                color: "#6b7280",
                fontSize: "9px",
                lineHeight: 1.5,
                marginTop: "8px",
              }}
            >
              Evidence: {impact.evidence}
            </div>

            {repositoryFeatureMap?.map((mapping, mappingIndex) => (
  <div
    key={mappingIndex}
    style={{
      marginTop: "10px",
      padding: "10px",
      borderRadius: "7px",
      background: "#0d1016",
      border: "1px solid #252a35",
    }}
  >
    <div
      style={{
        color: "#60a5fa",
        fontSize: "9px",
        fontWeight: 800,
        letterSpacing: "0.7px",
        marginBottom: "7px",
      }}
    >
      REPOSITORY-GROUNDED RELATIONSHIP
    </div>

    <div
      style={{
        color: "#d1d5db",
        fontSize: "10px",
        lineHeight: 1.5,
      }}
    >
      {mapping.changed_component?.function}()
      {" → "}
      {mapping.dependent_component?.function}()
    </div>

    <div
      style={{
        color: "#9ca3af",
        fontSize: "9px",
        lineHeight: 1.5,
        marginTop: "6px",
      }}
    >
      {mapping.basis}
    </div>

    <div
      style={{
        color: "#6b7280",
        fontSize: "9px",
        marginTop: "6px",
      }}
    >
      Repository grounded:{" "}
      {mapping.repository_grounded ? "YES" : "NO"}
    </div>
  </div>
))}

            <div
              style={{
                marginTop: "10px",
              }}
            >
              <div
                style={{
                  color: "#d1d5db",
                  fontSize: "9px",
                  fontWeight: 800,
                  letterSpacing: "0.7px",
                  marginBottom: "5px",
                }}
              >
                RECOMMENDED CHECKS
              </div>

              {impact.recommended_checks?.map(
                (check, checkIndex) => (
                  <div
                    key={checkIndex}
                    style={{
                      color: "#9ca3af",
                      fontSize: "9px",
                      lineHeight: 1.5,
                    }}
                  >
                    ✓ {check}
                  </div>
                )
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function TestImpact({ testImpact }) {
  if (!testImpact || testImpact.length === 0) {
    return null;
  }

  return (
    <section style={styles.subsection}>
      <h3 style={styles.sectionTitle}>
        Test Impact
      </h3>

      <div
        style={{
          padding: "14px",
          borderRadius: "10px",
          background: "#0b0c10",
          border: "1px solid #20222a",
        }}
      >
        <div
          style={{
            color: "#fbbf24",
            fontSize: "10px",
            fontWeight: 800,
            letterSpacing: "1px",
            marginBottom: "10px",
          }}
        >
          TESTS THAT SHOULD BE REVIEWED
        </div>

        <div
          style={{
            color: "#9ca3af",
            fontSize: "10px",
            marginBottom: "10px",
          }}
        >
          {testImpact.length} test
          {testImpact.length === 1 ? "" : "s"} potentially affected
          by this change.
        </div>

        {testImpact.map((testFile, index) => (
          <div
            key={index}
            style={{
              padding: "10px",
              marginBottom:
                index === testImpact.length - 1
                  ? "0"
                  : "7px",
              borderRadius: "8px",
              background: "#111218",
              border: "1px solid #1d2028",
            }}
          >
            <div
              style={{
                color: "#e5e7eb",
                fontSize: "11px",
                fontWeight: 800,
              }}
            >
              {testFile}
            </div>

            <div
              style={{
                color: "#9ca3af",
                fontSize: "10px",
                lineHeight: 1.5,
                marginTop: "5px",
              }}
            >
              This test directly depends on the changed
              component and should be reviewed or run after
              applying the proposed change.
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function ChangeImpactSummary({
  simulation,
  semanticChange,
  direct,
  indirect,
  breakage,
}) {
  const changedFunction =
    simulation.changed_function || null;

  const changedFile =
    simulation.changed_file || "Unknown";

  const impactCount =
    simulation.impact_count ?? 0;

  const riskAreas = [];

  if (changedFunction) {
    riskAreas.push(`${changedFunction}()`);
  }

  if (semanticChange?.category === "BEHAVIORAL") {
    riskAreas.push("Changed feature behavior");
  }

  if (
    semanticChange?.category === "RETURN_CONTRACT"
  ) {
    riskAreas.push("Return value compatibility");
  }

  if (
    semanticChange?.category === "INPUT_CONTRACT"
  ) {
    riskAreas.push("Input/parameter compatibility");
  }

  if (
    semanticChange?.category === "API_COMPATIBILITY"
  ) {
    riskAreas.push("API compatibility");
  }

  if (
    semanticChange?.category === "DATA_FLOW"
  ) {
    riskAreas.push("Data flow / data structure");
  }

  if (
    semanticChange?.category === "STRUCTURAL"
  ) {
    riskAreas.push("Project structure / references");
  }

  if (breakage && breakage.length > 0) {
    riskAreas.push("Related tests and dependent code");
  }

  return (
    <section style={styles.subsection}>
      <h3 style={styles.sectionTitle}>
        Change Impact Summary
      </h3>

      <div
        style={{
          padding: "14px",
          borderRadius: "10px",
          background: "#0b0c10",
          border: "1px solid #20222a",
        }}
      >
        {/* TARGET */}
        <div style={{ marginBottom: "14px" }}>
          <div
            style={{
              color: "#fbbf24",
              fontSize: "9px",
              fontWeight: 800,
              letterSpacing: "1px",
              marginBottom: "6px",
            }}
          >
            TARGET
          </div>

          <div
            style={{
              color: "#e5e7eb",
              fontSize: "12px",
              fontWeight: 800,
            }}
          >
            {changedFunction
              ? `${changedFunction}()`
              : changedFile}
          </div>

          {changedFunction && (
            <div
              style={{
                color: "#9ca3af",
                fontSize: "10px",
                marginTop: "4px",
              }}
            >
              {changedFile}
            </div>
          )}
        </div>

        {/* METRICS */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(3, minmax(0, 1fr))",
            gap: "8px",
            marginBottom: "14px",
          }}
        >
          <div
            style={{
              padding: "10px",
              borderRadius: "8px",
              background: "#111218",
              border: "1px solid #1d2028",
            }}
          >
            <div
              style={{
                color: "#9ca3af",
                fontSize: "8px",
                fontWeight: 800,
                letterSpacing: "0.8px",
              }}
            >
              IMPACTED
            </div>

            <div
              style={{
                color: "#e5e7eb",
                fontSize: "18px",
                fontWeight: 800,
                marginTop: "4px",
              }}
            >
              {impactCount}
            </div>

            <div
              style={{
                color: "#6b7280",
                fontSize: "8px",
              }}
            >
              files
            </div>
          </div>

          <div
            style={{
              padding: "10px",
              borderRadius: "8px",
              background: "#111218",
              border: "1px solid #1d2028",
            }}
          >
            <div
              style={{
                color: "#9ca3af",
                fontSize: "8px",
                fontWeight: 800,
                letterSpacing: "0.8px",
              }}
            >
              DIRECT
            </div>

            <div
              style={{
                color: "#86efac",
                fontSize: "18px",
                fontWeight: 800,
                marginTop: "4px",
              }}
            >
              {direct.length}
            </div>

            <div
              style={{
                color: "#6b7280",
                fontSize: "8px",
              }}
            >
              dependencies
            </div>
          </div>

          <div
            style={{
              padding: "10px",
              borderRadius: "8px",
              background: "#111218",
              border: "1px solid #1d2028",
            }}
          >
            <div
              style={{
                color: "#9ca3af",
                fontSize: "8px",
                fontWeight: 800,
                letterSpacing: "0.8px",
              }}
            >
              INDIRECT
            </div>

            <div
              style={{
                color: "#fcd34d",
                fontSize: "18px",
                fontWeight: 800,
                marginTop: "4px",
              }}
            >
              {indirect.length}
            </div>

            <div
              style={{
                color: "#6b7280",
                fontSize: "8px",
              }}
            >
              dependencies
            </div>
          </div>
        </div>

        {/* CHANGE NATURE */}
        {semanticChange && (
          <div
            style={{
              marginBottom: "14px",
              padding: "10px",
              borderRadius: "8px",
              background: "#111218",
              border: "1px solid #1d2028",
            }}
          >
            <div
              style={{
                color: "#9ca3af",
                fontSize: "8px",
                fontWeight: 800,
                letterSpacing: "0.8px",
                marginBottom: "6px",
              }}
            >
              CHANGE NATURE
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "8px",
              }}
            >
              <div
                style={{
                  color: "#e5e7eb",
                  fontSize: "11px",
                  fontWeight: 800,
                }}
              >
                {semanticChange.category}
              </div>

              <div
                style={{
                  color:
                    semanticChange.confidence === "HIGH"
                      ? "#86efac"
                      : semanticChange.confidence === "MEDIUM"
                      ? "#fcd34d"
                      : "#fca5a5",
                  fontSize: "8px",
                  fontWeight: 800,
                }}
              >
                {semanticChange.confidence}
              </div>
            </div>
          </div>
        )}

        {/* RISK AREAS */}
        {riskAreas.length > 0 && (
          <div
            style={{
              marginBottom: "14px",
            }}
          >
            <div
              style={{
                color: "#fbbf24",
                fontSize: "9px",
                fontWeight: 800,
                letterSpacing: "1px",
                marginBottom: "7px",
              }}
            >
              RISK AREAS
            </div>

            {riskAreas.map((risk, index) => (
              <div
                key={index}
                style={{
                  color: "#cbd5e1",
                  fontSize: "10px",
                  lineHeight: 1.5,
                  marginBottom:
                    index === riskAreas.length - 1
                      ? "0"
                      : "4px",
                }}
              >
                • {risk}
              </div>
            ))}
          </div>
        )}

        {/* REPOSITORY STATUS */}
        <div
          style={{
            paddingTop: "10px",
            borderTop: "1px solid #1d2028",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <div
            style={{
              color: "#9ca3af",
              fontSize: "9px",
              fontWeight: 800,
              letterSpacing: "0.8px",
            }}
          >
            REPOSITORY MODIFIED
          </div>

          <div
            style={{
              color: "#86efac",
              fontSize: "9px",
              fontWeight: 800,
            }}
          >
            NO
          </div>
        </div>
      </div>
    </section>
  );
}

function Results({
  result,
  onBack,
  onNew,
}) {
  const simulation = result.simulation || {};

  const dependencyImpact =
    simulation.dependency_impact || null;

  const consequences =
    simulation.consequences || [];

  const semanticChange =
    simulation.semantic_change || null;

  console.log("PROJECTTWIN SIMULATION:", simulation);

  const direct =
    simulation.direct_dependencies || [];

  const indirect =
    simulation.indirect_dependencies || [];

  const removed =
    simulation.removed || [];

  const modified =
    simulation.modified || [];

  const added =
    simulation.added || [];

  const functions =
    simulation.function_impact || [];

  const breakage =
    simulation.possible_breakage || [];

  const testImpact =
    simulation.test_impact || [];

  const featureImpact =
    simulation.feature_impact || [];

  const repositoryFeatureMap =
    simulation.repository_feature_map || [];
  
  return (
    <div>
      <div style={styles.resultActions}>
        <button
          style={styles.secondary}
          onClick={onBack}
        >
          ← Edit Simulation
        </button>

        <button
          style={styles.primary}
          onClick={onNew}
        >
          New Simulation
        </button>
      </div>

      <div style={styles.summaryGrid}>
        <Metric
          label="CHANGE TYPE"
          value={result.change_type || "MODIFY"}
        />

        <Metric
          label="IMPACTED FILES"
          value={simulation.impact_count ?? 0}
        />

        <Metric
          label="DIRECT"
          value={direct.length}
        />

        <Metric
          label="INDIRECT"
          value={indirect.length}
        />
      </div>

      <section style={styles.panel}>
        <div style={styles.resultHeading}>
          <div>
            <div style={styles.cardLabel}>
              SIMULATION
            </div>

            <h2 style={styles.panelTitle}>
              {result.changed_file}
            </h2>

            <p style={styles.cardText}>
              {result.change_description}
            </p>
          </div>

          <span style={styles.typeBadge}>
            {result.change_type}
          </span>
        </div>

        <ChangeImpactSummary
          simulation={simulation}
          semanticChange={semanticChange}
          direct={direct}
          indirect={indirect}
          breakage={breakage}
        />

        <ImpactList
          title="Predicted Removed"
          items={removed}
          empty="Nothing predicted for removal."
        />

        <ImpactList
          title="Predicted Modified"
          items={modified}
          empty="No files predicted as modified."
        />

        <ImpactList
          title="Predicted Added"
          items={added}
          empty="No new files predicted."
        />

        <ImpactList
          title="Direct Dependencies"
          items={direct}
          empty="No direct dependencies detected."
        />

        <ImpactList
          title="Indirect Dependencies"
          items={indirect}
          empty="No indirect dependencies detected."
        />

        <ImpactEvidence
          dependencyImpact={dependencyImpact}
        />

        {semanticChange && (
  <section style={styles.subsection}>
    <h3 style={styles.sectionTitle}>
      Change Nature
    </h3>

    <div
      style={{
        padding: "14px",
        borderRadius: "10px",
        background: "#0b0c10",
        border: "1px solid #20222a",
      }}
    >
      <div
        style={{
          color: "#fbbf24",
          fontSize: "10px",
          fontWeight: 800,
          letterSpacing: "1px",
          marginBottom: "10px",
        }}
      >
        SEMANTIC CHANGE ANALYSIS
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          marginBottom: "10px",
        }}
      >
        <div
          style={{
            color: "#e5e7eb",
            fontSize: "13px",
            fontWeight: 800,
          }}
        >
          {semanticChange.category}
        </div>

        <div
          style={{
            color:
              semanticChange.confidence === "HIGH"
                ? "#86efac"
                : semanticChange.confidence === "MEDIUM"
                ? "#fcd34d"
                : "#fca5a5",
            fontSize: "9px",
            fontWeight: 800,
            letterSpacing: "0.8px",
          }}
        >
          {semanticChange.confidence} CONFIDENCE
        </div>
      </div>

      <div
        style={{
          color: "#9ca3af",
          fontSize: "11px",
          lineHeight: 1.55,
        }}
      >
        {semanticChange.evidence}
      </div>
    </div>
  </section>
)}

        <ConsequencePrediction
          consequences={consequences}
        />

        <FeatureImpact
          featureImpact={featureImpact}
          repositoryFeatureMap={repositoryFeatureMap}
        />

        <TestImpact
          testImpact={testImpact}
        />

        <section style={styles.subsection}>
          <h3 style={styles.sectionTitle}>
            Function-Level Impact
          </h3>

          {functions.length === 0 ? (
            <p style={styles.muted}>
              No function-level relationships
              were detected.
            </p>
          ) : (
            functions.map((item, i) => (
              <div
                key={i}
                style={styles.relationship}
              >
                <b>
                  {item.dependent_function ||
                    "unknown"}
                  ()
                </b>

                <span>
                  {item.dependent_file}
                </span>

                <span>
                  →{" "}
                  {item.changed_function ||
                    result.changed_file}
                </span>
              </div>
            ))
          )}
        </section>

        <section style={styles.subsection}>
          <h3 style={styles.sectionTitle}>
            Possible Breakage
          </h3>

          {breakage.length === 0 ? (
            <p style={styles.muted}>
              No possible breakage was identified
              by the dependency analysis.
            </p>
          ) : (
            breakage.map((item, i) => (
              <div
                key={i}
                style={styles.breakage}
              >
                <b>{item.file}</b>

                {item.function && (
                  <span>
                    {" "}
                    · {item.function}()
                  </span>
                )}

                <p>{item.reason}</p>
              </div>
            ))
          )}
        </section>
      </section>

      <section style={styles.aiCard}>
        <div style={styles.aiHeader}>
          <span style={styles.aiIcon}>
            ✦
          </span>

          <div>
            <div style={styles.cardLabel}>
              AI ANALYSIS
            </div>

            <h2 style={styles.panelTitle}>
              ProjectTwin reasoning
            </h2>
          </div>
        </div>

        <pre style={styles.aiText}>
          {result.ai_analysis ||
            "No AI analysis returned."}
        </pre>
      </section>
    </div>
  );
}
function GraphView({ data, loading }) {
  const nodes = (data?.nodes || []).map((node, index) => ({
    id: node.id,
    position: {
      x: (index % 4) * 280,
      y: Math.floor(index / 4) * 160,
    },
    data: {
      label: node.label,
    },
    style: {
      background: "#111218",
      color: "#e5e7eb",
      border: "1px solid #7c3aed",
      borderRadius: "10px",
      padding: "12px",
      width: 220,
      fontSize: "11px",
    },
  }));

  const edges = (data?.edges || []).map(
    (edge, index) => ({
      id: `edge-${index}`,
      source: edge.source,
      target: edge.target,
      animated: false,
      style: {
        stroke: "#7c3aed",
        strokeWidth: 1.5,
      },
    })
  );

  return (
    <section style={styles.graphSection}>
      <div style={styles.graphTop}>
        <div>
          <div style={styles.eyebrow}>
            PROJECT ARCHITECTURE
          </div>

          <h2 style={styles.sectionHeading}>
            Dependency Graph
          </h2>

          <p style={styles.description}>
            Visual representation of relationships
            between files in the analyzed repository.
          </p>
        </div>

        {data && (
          <div style={styles.graphStats}>
            <div style={styles.graphStat}>
              <b>{data.node_count}</b>
              <span>FILES</span>
            </div>

            <div style={styles.graphStat}>
              <b>{data.edge_count}</b>
              <span>RELATIONSHIPS</span>
            </div>
          </div>
        )}
      </div>

      {loading && (
        <div style={styles.graphEmpty}>
          <div style={styles.loadingIcon}>◌</div>

          <h3>Analyzing repository...</h3>

          <p>
            ProjectTwin is building the dependency
            graph.
          </p>
        </div>
      )}

      {!loading && !data && (
        <div style={styles.graphEmpty}>
          <div style={styles.loadingIcon}>
            ⌘
          </div>

          <h3>No graph loaded</h3>

          <p>
            Enter a repository and open the
            Dependency Graph.
          </p>
        </div>
      )}

      {!loading && data && (
        <div style={styles.graphCanvas}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            fitView
            minZoom={0.15}
            maxZoom={2}
          >
            <MiniMap />

            <Controls />

            <Background gap={24} />
          </ReactFlow>
        </div>
      )}
    </section>
  );
}


const styles = {
  app: {
    minHeight: "100vh",
    display: "flex",
    background: "#08090d",
    color: "#f5f5f7",
    fontFamily:
      "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
  },

  sidebar: {
    width: "245px",
    minHeight: "100vh",
    boxSizing: "border-box",
    padding: "28px 18px",
    background: "#0c0d12",
    borderRight: "1px solid #22242d",
    display: "flex",
    flexDirection: "column",
    position: "sticky",
    top: 0,
  },

  brand: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "5px 8px 38px",
  },

  logo: {
    width: "42px",
    height: "42px",
    borderRadius: "12px",
    background:
      "linear-gradient(135deg, #7c3aed, #4f46e5)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 800,
    fontSize: "14px",
  },

  brandName: {
    fontSize: "17px",
    fontWeight: 800,
  },

  brandSub: {
    color: "#707481",
    fontSize: "11px",
    marginTop: "3px",
  },

  navTitle: {
    color: "#555967",
    fontSize: "9px",
    fontWeight: 800,
    letterSpacing: "1.5px",
    padding: "0 10px 10px",
  },

  nav: {
    width: "100%",
    border: "1px solid transparent",
    background: "transparent",
    color: "#858997",
    borderRadius: "9px",
    padding: "12px 13px",
    display: "flex",
    alignItems: "center",
    gap: "11px",
    fontSize: "13px",
    cursor: "pointer",
    textAlign: "left",
    marginBottom: "5px",
  },

  navActive: {
    background: "rgba(124, 58, 237, 0.13)",
    color: "#c4b5fd",
    border:
      "1px solid rgba(124, 58, 237, 0.22)",
  },

  navIcon: {
    width: "20px",
    textAlign: "center",
    fontSize: "15px",
  },

  sidebarBottom: {
    marginTop: "auto",
    borderTop: "1px solid #22242d",
    padding: "20px 8px 4px",
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },

  statusDot: {
    width: "8px",
    height: "8px",
    borderRadius: "50%",
    background: "#34d399",
    boxShadow:
      "0 0 10px rgba(52, 211, 153, 0.7)",
  },

  statusText: {
    color: "#d1d5db",
    fontSize: "11px",
    fontWeight: 700,
  },

  statusSub: {
    color: "#626674",
    fontSize: "9px",
    marginTop: "3px",
  },

  main: {
    flex: 1,
    minWidth: 0,
    padding: "42px 50px",
    boxSizing: "border-box",
  },

  header: {
    maxWidth: "1120px",
    margin: "0 auto 34px",
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "space-between",
  },

  eyebrow: {
    color: "#8b5cf6",
    fontSize: "9px",
    fontWeight: 800,
    letterSpacing: "1.8px",
    marginBottom: "9px",
  },

  title: {
    margin: 0,
    fontSize: "32px",
    letterSpacing: "-1px",
  },

  headerBadge: {
    border:
      "1px solid rgba(52, 211, 153, 0.25)",
    color: "#6ee7b7",
    background:
      "rgba(52, 211, 153, 0.06)",
    borderRadius: "999px",
    padding: "8px 12px",
    fontSize: "9px",
    fontWeight: 800,
    letterSpacing: "1px",
  },

  hero: {
    maxWidth: "1120px",
    margin: "0 auto 25px",
    padding: "42px",
    borderRadius: "20px",
    border: "1px solid #252732",
    background:
      "radial-gradient(circle at 90% 30%, rgba(124,58,237,0.2), transparent 32%), #111218",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "30px",
  },

  heroKicker: {
    color: "#a78bfa",
    fontSize: "9px",
    fontWeight: 800,
    letterSpacing: "2px",
    marginBottom: "12px",
  },

  heroTitle: {
    margin: 0,
    maxWidth: "680px",
    fontSize: "30px",
    lineHeight: 1.15,
    letterSpacing: "-1px",
  },

  heroText: {
    color: "#858997",
    maxWidth: "650px",
    fontSize: "13px",
    lineHeight: 1.7,
    marginTop: "15px",
  },

  heroButtons: {
    display: "flex",
    gap: "10px",
    marginTop: "24px",
    flexWrap: "wrap",
  },

  heroOrb: {
    width: "150px",
    height: "150px",
    minWidth: "150px",
    borderRadius: "50%",
    border:
      "1px solid rgba(139,92,246,0.35)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background:
      "radial-gradient(circle, rgba(124,58,237,0.25), transparent 65%)",
  },

  orbInner: {
    width: "80px",
    height: "80px",
    borderRadius: "24px",
    background:
      "linear-gradient(135deg, #7c3aed, #4f46e5)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 900,
    fontSize: "24px",
  },

  primary: {
    border: 0,
    borderRadius: "9px",
    padding: "12px 17px",
    background:
      "linear-gradient(135deg, #7c3aed, #5b4ee8)",
    color: "white",
    fontWeight: 700,
    cursor: "pointer",
    fontSize: "12px",
  },

  secondary: {
    border: "1px solid #343640",
    borderRadius: "9px",
    padding: "12px 17px",
    background: "#111218",
    color: "#c5c7d0",
    fontWeight: 600,
    cursor: "pointer",
    fontSize: "12px",
  },

  cardGrid: {
    maxWidth: "1120px",
    margin: "0 auto 25px",
    display: "grid",
    gridTemplateColumns:
      "repeat(4, minmax(0, 1fr))",
    gap: "12px",
  },

  feature: {
    background: "#111218",
    border: "1px solid #252732",
    borderRadius: "14px",
    padding: "20px",
  },

  featureIcon: {
    color: "#a78bfa",
    fontSize: "20px",
    marginBottom: "15px",
  },

  featureTitle: {
    margin: 0,
    fontSize: "14px",
  },

  featureText: {
    color: "#777b89",
    fontSize: "11px",
    lineHeight: 1.6,
    marginTop: "8px",
  },

  infoCard: {
    maxWidth: "1120px",
    margin: "0 auto",
    padding: "25px",
    borderRadius: "15px",
    border: "1px solid #252732",
    background: "#0f1015",
    display: "flex",
    justifyContent: "space-between",
    gap: "30px",
    alignItems: "center",
  },

  cardLabel: {
    color: "#777b89",
    fontSize: "9px",
    fontWeight: 800,
    letterSpacing: "1.5px",
    marginBottom: "7px",
  },

  cardTitle: {
    margin: 0,
    fontSize: "17px",
  },

  cardText: {
    color: "#7d818e",
    fontSize: "12px",
    lineHeight: 1.6,
    maxWidth: "650px",
  },

  flowMini: {
    display: "flex",
    gap: "10px",
    alignItems: "center",
    color: "#a78bfa",
    fontSize: "11px",
    whiteSpace: "nowrap",
  },

  panel: {
    maxWidth: "1120px",
    margin: "0 auto 18px",
    padding: "27px",
    borderRadius: "17px",
    border: "1px solid #252732",
    background: "#111218",
  },

  panelHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: "25px",
  },

  panelTitle: {
    margin: 0,
    fontSize: "20px",
  },

  field: {
    display: "block",
    marginBottom: "20px",
  },

  fieldTop: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "8px",
    color: "#d5d7de",
    fontSize: "12px",
  },

  fieldTopSmall: {
    color: "#666a77",
  },

  input: {
    width: "100%",
    boxSizing: "border-box",
    background: "#0b0c10",
    border: "1px solid #2b2e38",
    borderRadius: "9px",
    padding: "13px 14px",
    color: "#f5f5f7",
    outline: "none",
    fontSize: "12px",
  },

  textarea: {
    width: "100%",
    minHeight: "130px",
    boxSizing: "border-box",
    resize: "vertical",
    background: "#0b0c10",
    border: "1px solid #2b2e38",
    borderRadius: "9px",
    padding: "13px 14px",
    color: "#f5f5f7",
    outline: "none",
    fontSize: "12px",
    fontFamily: "inherit",
  },

  twoCol: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "16px",
  },

  simulationNote: {
    border:
      "1px solid rgba(139,92,246,0.2)",
    background:
      "rgba(124,58,237,0.06)",
    color: "#9a9dab",
    borderRadius: "9px",
    padding: "12px",
    fontSize: "11px",
    marginBottom: "15px",
  },

  primaryWide: {
    width: "100%",
    border: 0,
    borderRadius: "9px",
    padding: "14px",
    background:
      "linear-gradient(135deg, #7c3aed, #5b4ee8)",
    color: "white",
    fontWeight: 800,
    cursor: "pointer",
  },

  alert: {
    maxWidth: "1120px",
    margin: "0 auto 18px",
    padding: "13px 15px",
    borderRadius: "9px",
    border: "1px solid rgba(248,113,113,0.3)",
    background: "rgba(248,113,113,0.07)",
    color: "#fca5a5",
    fontSize: "12px",
  },

  resultActions: {
    maxWidth: "1120px",
    margin: "0 auto 18px",
    display: "flex",
    justifyContent: "space-between",
  },

  summaryGrid: {
    maxWidth: "1120px",
    margin: "0 auto 18px",
    display: "grid",
    gridTemplateColumns:
      "repeat(4, minmax(0, 1fr))",
    gap: "12px",
  },

  metric: {
    background: "#111218",
    border: "1px solid #252732",
    borderRadius: "13px",
    padding: "19px",
  },

  metricLabel: {
    color: "#6f7380",
    fontSize: "9px",
    fontWeight: 800,
    letterSpacing: "1.3px",
  },

  metricValue: {
    marginTop: "9px",
    fontSize: "22px",
    fontWeight: 800,
  },

  resultHeading: {
    display: "flex",
    justifyContent: "space-between",
    gap: "20px",
    marginBottom: "25px",
  },

  typeBadge: {
    height: "fit-content",
    padding: "8px 11px",
    borderRadius: "999px",
    background:
      "rgba(124,58,237,0.12)",
    color: "#c4b5fd",
    fontSize: "9px",
    fontWeight: 800,
  },

  subsection: {
    marginTop: "22px",
    paddingTop: "20px",
    borderTop: "1px solid #22242d",
  },

  sectionTitle: {
    margin: "0 0 12px",
    fontSize: "14px",
  },

  muted: {
    color: "#686c78",
    fontSize: "11px",
  },

  relationship: {
    display: "flex",
    gap: "12px",
    alignItems: "center",
    padding: "11px 12px",
    marginBottom: "6px",
    borderRadius: "8px",
    background: "#0b0c10",
    color: "#b9bbc5",
    fontSize: "11px",
  },

  breakage: {
    padding: "12px",
    marginBottom: "7px",
    borderRadius: "8px",
    background:
      "rgba(248,113,113,0.05)",
    border:
      "1px solid rgba(248,113,113,0.14)",
    color: "#e5e7eb",
    fontSize: "11px",
  },

  aiCard: {
    maxWidth: "1120px",
    margin: "0 auto 18px",
    padding: "27px",
    borderRadius: "17px",
    border:
      "1px solid rgba(124,58,237,0.28)",
    background:
      "linear-gradient(135deg, rgba(124,58,237,0.08), #111218)",
  },

  aiHeader: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    marginBottom: "18px",
  },

  aiIcon: {
    width: "36px",
    height: "36px",
    borderRadius: "10px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background:
      "rgba(124,58,237,0.18)",
    color: "#c4b5fd",
  },

  aiText: {
    whiteSpace: "pre-wrap",
    fontFamily: "inherit",
    color: "#b9bbc5",
    fontSize: "12px",
    lineHeight: 1.7,
    margin: 0,
  },

  fileList: {
    display: "flex",
    flexDirection: "column",
    gap: "6px",
  },

  fileItem: {
    padding: "10px 12px",
    borderRadius: "8px",
    background: "#0b0c10",
    border: "1px solid #20222a",
    color: "#b9bbc5",
    fontSize: "11px",
  },

  emptyState: {
    color: "#696d79",
    padding: "15px",
    fontSize: "11px",
    background: "#0b0c10",
    borderRadius: "8px",
  },

  graphSection: {
    maxWidth: "1120px",
    margin: "0 auto",
  },

  graphTop: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: "20px",
  },

  sectionHeading: {
    margin: 0,
    fontSize: "27px",
  },

  graphStats: {
    display: "flex",
    gap: "10px",
  },

  graphStat: {
    minWidth: "90px",
    padding: "12px 15px",
    borderRadius: "10px",
    border: "1px solid #252732",
    background: "#111218",
    textAlign: "center",
  },

  "graphStat b": {
    display: "block",
    fontSize: "18px",
  },

  "graphStat span": {
    display: "block",
    marginTop: "4px",
    color: "#6f7380",
    fontSize: "8px",
    letterSpacing: "1px",
  },

  graphCanvas: {
    height: "650px",
    borderRadius: "16px",
    overflow: "hidden",
    border: "1px solid #252732",
    background: "#0b0c10",
  },

  graphEmpty: {
    height: "400px",
    borderRadius: "16px",
    border: "1px solid #252732",
    background: "#111218",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    color: "#8b8f9d",
  },

  loadingIcon: {
    fontSize: "34px",
    color: "#a78bfa",
    marginBottom: "10px",
  },
};

export default App;
