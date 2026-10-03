from backend.dependency_model import DependencyModel


def find_direct_impact(
    dependency_model: DependencyModel,
    changed_file: str,
    changed_symbol: str | None = None
):
    """
    Find files/symbols that directly depend on the
    changed file or changed symbol.
    """

    impacted = []

    for dependency in dependency_model.get_all():

        # --------------------------------------------------
        # File-level impact
        # --------------------------------------------------

        if dependency.target_file != changed_file:
            continue

        # --------------------------------------------------
        # If a specific symbol is being changed,
        # only consider relationships targeting that symbol.
        # --------------------------------------------------

        if (
            changed_symbol is not None
            and dependency.target_symbol != changed_symbol
        ):
            continue

        impacted.append(
            {
                "source_file": dependency.source_file,
                "source_symbol": dependency.source_symbol,
                "target_file": dependency.target_file,
                "target_symbol": dependency.target_symbol,
                "relationship_type": dependency.relationship_type,
                "evidence": dependency.evidence
            }
        )

    return impacted


def find_indirect_impact(
    dependency_model: DependencyModel,
    changed_file: str,
    changed_symbol: str | None = None
):
    """
    Find indirect impact by walking backwards through
    the dependency relationships.
    """

    visited_files = set()
    queue = []

    direct = find_direct_impact(
        dependency_model,
        changed_file,
        changed_symbol
    )

    for dependency in direct:

        source_file = dependency["source_file"]

        if source_file != changed_file:
            queue.append(source_file)

    while queue:

        current_file = queue.pop(0)

        if current_file in visited_files:
            continue

        visited_files.add(current_file)

        for dependency in dependency_model.get_all():

            if dependency.target_file != current_file:
                continue

            source_file = dependency.source_file

            if (
                source_file != changed_file
                and source_file not in visited_files
            ):
                queue.append(source_file)

    return sorted(visited_files)


def analyze_dependency_impact(
    dependency_model: DependencyModel,
    changed_file: str,
    changed_symbol: str | None = None
):
    """
    Perform language-independent dependency impact analysis.
    """

    direct = find_direct_impact(
        dependency_model,
        changed_file,
        changed_symbol
    )

    indirect = find_indirect_impact(
        dependency_model,
        changed_file,
        changed_symbol
    )

    affected_files = set()

    for dependency in direct:

        affected_files.add(
            dependency["source_file"]
        )

    affected_files.update(
        indirect
    )

    return {
        "changed_file": changed_file,
        "changed_symbol": changed_symbol,
        "direct_impact": direct,
        "indirect_impact": indirect,
        "affected_files": sorted(
            affected_files
        ),
        "impact_count": len(
            affected_files
        )
    }