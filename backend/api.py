from pathlib import Path

import networkx as nx

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.github_ingestion import clone_repository
from backend.main import analyze_project

from backend.change_simulator import predict_change
from backend.impact_report import generate_impact_report
from backend.impact_rag import build_impact_prompt
from backend.llm import ask_gemini
from backend.impact_formatter import format_impact_report


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="ProjectTwin API",
    description="AI-powered Digital Twin for software projects",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# REQUEST MODELS
# =========================================================

class SimulationRequest(BaseModel):
    repo_url: str
    changed_file: str
    change_description: str
    changed_function: str | None = None


class GraphRequest(BaseModel):
    repo_url: str


# =========================================================
# PATH NORMALIZATION
# =========================================================

def normalize_path(path_value, repository_path):
    """
    Convert a full repository path into a project-relative
    POSIX-style path.
    """

    if not path_value:
        return path_value

    path_value = str(path_value)
    repository_path = str(Path(repository_path))

    try:
        relative = Path(path_value).resolve().relative_to(
            Path(repository_path).resolve()
        )

        return relative.as_posix()

    except ValueError:
        pass

    path_value = path_value.replace("\\", "/")
    repository_path = repository_path.replace("\\", "/").rstrip("/")

    if path_value.startswith(repository_path + "/"):
        return path_value[len(repository_path) + 1:]

    return path_value.lstrip("./")


# =========================================================
# GRAPH NORMALIZATION
# =========================================================

def normalize_graph(graph, repository_path):
    """
    Convert graph node paths into project-relative paths.
    """

    normalized_graph = nx.DiGraph()

    for source, target in graph.edges():

        normalized_source = normalize_path(
            source,
            repository_path
        )

        normalized_target = normalize_path(
            target,
            repository_path
        )

        normalized_graph.add_node(
            normalized_source
        )

        normalized_graph.add_node(
            normalized_target
        )

        normalized_graph.add_edge(
            normalized_source,
            normalized_target
        )

    return normalized_graph


# =========================================================
# FUNCTION DEPENDENCY NORMALIZATION
# =========================================================

def normalize_function_dependencies(
    function_dependencies,
    repository_path
):
    """
    Convert function dependency paths into
    project-relative paths.
    """

    normalized = []

    for dependency in function_dependencies:

        normalized.append(
            {
                **dependency,

                "source_file": normalize_path(
                    dependency["source_file"],
                    repository_path
                ),

                "target_file": normalize_path(
                    dependency["target_file"],
                    repository_path
                ),
            }
        )

    return normalized


# =========================================================
# LANGUAGE-INDEPENDENT DEPENDENCY NORMALIZATION
# =========================================================

def normalize_dependency_model(
    dependency_model,
    repository_path
):
    """
    Convert the language-independent DependencyModel
    into JSON-friendly dictionaries with project-relative
    file paths.
    """

    normalized = []

    for dependency in dependency_model.get_all():

        normalized.append(
            {
                "source_file": normalize_path(
                    dependency.source_file,
                    repository_path
                ),

                "source_symbol": dependency.source_symbol,

                "target_file": normalize_path(
                    dependency.target_file,
                    repository_path
                ),

                "target_symbol": dependency.target_symbol,

                "relationship_type": (
                    dependency.relationship_type
                ),

                "evidence": dependency.evidence,
            }
        )

    return normalized


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "ProjectTwin API is running!"
    }


# =========================================================
# CHANGE SIMULATION
# =========================================================

@app.post("/simulate")
def simulate_change(request: SimulationRequest):

    # -----------------------------------------------------
    # Clone repository
    # -----------------------------------------------------

    base_destination = Path(
        "data/repos/api_project"
    )

    repository_path = clone_repository(
        request.repo_url,
        base_destination
    )

    # -----------------------------------------------------
    # IMPORTANT:
    # clone_repository() may return a NEW destination
    # when another repository already exists there.
    #
    # We MUST analyze the returned destination.
    # -----------------------------------------------------

    repository_path = Path(repository_path)

    # -----------------------------------------------------
    # Analyze repository
    # -----------------------------------------------------

    (
        graph,
        function_dependencies,
        dependency_model
    ) = analyze_project(
        str(repository_path)
    )

    # -----------------------------------------------------
    # Normalize graph paths
    # -----------------------------------------------------

    graph = normalize_graph(
        graph,
        repository_path
    )

    # -----------------------------------------------------
    # Normalize function dependencies
    # -----------------------------------------------------

    function_dependencies = (
        normalize_function_dependencies(
            function_dependencies,
            repository_path
        )
    )

    # -----------------------------------------------------
    # Normalize language-independent dependencies
    # -----------------------------------------------------

    dependency_model_data = (
        normalize_dependency_model(
            dependency_model,
            repository_path
        )
    )

    # -----------------------------------------------------
    # Normalize changed file
    # -----------------------------------------------------

    changed_file = normalize_path(
        request.changed_file,
        repository_path
    )

    changed_function = request.changed_function

    # -----------------------------------------------------
    # Validate changed file
    # -----------------------------------------------------

    if changed_file not in graph.nodes:

        return {
            "status": "error",
            "message": (
                "Changed file was not found in the analyzed "
                f"project: {changed_file}"
            )
        }

    # -----------------------------------------------------
    # Run change simulation
    # -----------------------------------------------------

    simulation = predict_change(
        graph,
        changed_file,
        request.change_description,
        function_dependencies,
        changed_function,
        dependency_model
    )

    # -----------------------------------------------------
    # Generate evidence report
    # -----------------------------------------------------

    report = generate_impact_report(
        graph,
        str(repository_path),
        changed_file
    )

    # -----------------------------------------------------
    # Build AI prompt
    # -----------------------------------------------------

    prompt = build_impact_prompt(
        report
    )

    # -----------------------------------------------------
    # Ask Gemini
    # -----------------------------------------------------

    ai_analysis = ask_gemini(
        prompt
    )

    # -----------------------------------------------------
    # Format result
    # -----------------------------------------------------

    formatted_report = format_impact_report(
        simulation,
        report,
        ai_analysis
    )

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return {
        "status": "success",

        "repository": {
            "url": request.repo_url,
            "local_path": str(repository_path)
        },

        "simulation": simulation,

        "report": report,

        "ai_analysis": ai_analysis,

        "formatted_report": formatted_report,

        "dependency_model": {
            "dependency_count": len(
                dependency_model_data
            ),
            "dependencies": dependency_model_data
        }
    }


# =========================================================
# DEPENDENCY GRAPH
# =========================================================

@app.post("/graph")
def get_graph(request: GraphRequest):

    # -----------------------------------------------------
    # Clone repository
    # -----------------------------------------------------

    base_destination = Path(
        "data/repos/graph_project"
    )

    repository_path = clone_repository(
        request.repo_url,
        base_destination
    )

    # -----------------------------------------------------
    # IMPORTANT:
    # Use the destination actually returned by
    # clone_repository().
    # -----------------------------------------------------

    repository_path = Path(repository_path)

    # -----------------------------------------------------
    # Analyze repository
    # -----------------------------------------------------

    (
        graph,
        function_dependencies,
        dependency_model
    ) = analyze_project(
        str(repository_path)
    )

    # -----------------------------------------------------
    # Normalize graph
    # -----------------------------------------------------

    graph = normalize_graph(
        graph,
        repository_path
    )

    # -----------------------------------------------------
    # Normalize language-independent dependencies
    # -----------------------------------------------------

    dependency_model_data = (
        normalize_dependency_model(
            dependency_model,
            repository_path
        )
    )

    # -----------------------------------------------------
    # Create frontend nodes
    # -----------------------------------------------------

    nodes = []

    for node in graph.nodes:

        nodes.append(
            {
                "id": node,
                "label": node
            }
        )

    # -----------------------------------------------------
    # Create frontend edges
    # -----------------------------------------------------

    edges = []

    for source, target in graph.edges:

        edges.append(
            {
                "source": source,
                "target": target
            }
        )

    # -----------------------------------------------------
    # Return graph
    # -----------------------------------------------------

    return {
        "status": "success",

        "repository": {
            "url": request.repo_url,
            "local_path": str(repository_path)
        },

        "node_count": graph.number_of_nodes(),

        "edge_count": graph.number_of_edges(),

        "nodes": nodes,

        "edges": edges,

        "dependency_model": {
            "dependency_count": len(
                dependency_model_data
            ),
            "dependencies": dependency_model_data
        }
    }