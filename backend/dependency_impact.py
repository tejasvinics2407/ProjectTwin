from backend.dependency_model import DependencyModel


def find_direct_impact(
    dependency_model: DependencyModel,
    changed_file: str,
    changed_symbol=None
):
    """
    Find files/symbols that directly depend on the changed
    file or changed symbol.
    """

    impacted = []

    for dependency in dependency_model.get_all():

        if dependency.target_file != changed_file:
            continue

        if (
            changed_symbol is not None
            and dependency.target_symbol != changed_symbol
        ):
            continue

        impacted.append({
            "source_file": dependency.source_file,
            "source_symbol": dependency.source_symbol,
            "target_file": dependency.target_file,
            "target_symbol": dependency.target_symbol,
            "relationship_type": dependency.relationship_type,
            "evidence": dependency.evidence,
            "impact_level": "DIRECT",
            "confidence": "PROVEN",
        })

    return impacted


def find_indirect_impact(
    dependency_model: DependencyModel,
    changed_file: str,
    changed_symbol=None
):
    """
    Find files that are indirectly affected.

    Example:

        A -> B -> C

    If C changes:

        B = DIRECT
        A = INDIRECT
    """

    direct = find_direct_impact(
        dependency_model,
        changed_file,
        changed_symbol
    )

    direct_files = {
        item["source_file"]
        for item in direct
    }

    visited_files = set()
    queue = list(direct_files)
    indirect_files = set()

    while queue:

        current_file = queue.pop(0)

        if current_file in visited_files:
            continue

        visited_files.add(current_file)

        for dependency in dependency_model.get_all():

            if dependency.target_file != current_file:
                continue

            source_file = dependency.source_file

            if source_file == changed_file:
                continue

            # Direct files must NOT also appear as indirect.
            if source_file in direct_files:
                continue

            if source_file not in indirect_files:
                indirect_files.add(source_file)
                queue.append(source_file)

    return sorted(indirect_files)


def build_indirect_impact_details(
    dependency_model: DependencyModel,
    changed_file: str,
    direct_impact
):
    """
    Build evidence for indirect impacts.
    """

    direct_files = {
        item["source_file"]
        for item in direct_impact
    }

    details = []

    queue = [
        (file_path, [changed_file, file_path])
        for file_path in direct_files
    ]

    visited = set()

    while queue:

        current_file, path = queue.pop(0)

        if current_file in visited:
            continue

        visited.add(current_file)

        for dependency in dependency_model.get_all():

            if dependency.target_file != current_file:
                continue

            source_file = dependency.source_file

            if source_file == changed_file:
                continue

            new_path = path + [source_file]

            if source_file not in direct_files:

                details.append({
                    "source_file": source_file,
                    "impact_level": "INDIRECT",
                    "confidence": "LIKELY",
                    "dependency_chain": new_path,
                    "evidence": (
                        f"{source_file} depends on "
                        f"{current_file}, which is affected by "
                        f"{changed_file}"
                    ),
                })

            if source_file not in visited:
                queue.append(
                    (source_file, new_path)
                )

    # Remove duplicate entries.
    unique = {}

    for item in details:

        key = (
            item["source_file"],
            tuple(item["dependency_chain"])
        )

        unique[key] = item

    return list(unique.values())


def analyze_dependency_impact(
    dependency_model: DependencyModel,
    changed_file: str,
    changed_symbol=None
):
    """
    Complete language-independent dependency impact analysis.
    """

    direct = find_direct_impact(
        dependency_model,
        changed_file,
        changed_symbol
    )

    indirect_files = find_indirect_impact(
        dependency_model,
        changed_file,
        changed_symbol
    )

    indirect_details = build_indirect_impact_details(
        dependency_model,
        changed_file,
        direct
    )

    affected_files = {
        item["source_file"]
        for item in direct
    }

    affected_files.update(indirect_files)

    return {
        "changed_file": changed_file,
        "changed_symbol": changed_symbol,

        "direct_impact": direct,

        "indirect_impact": indirect_files,

        "indirect_impact_details": indirect_details,

        "affected_files": sorted(affected_files),

        "impact_count": len(affected_files),

        "impact_summary": {
            "direct_count": len(direct),
            "indirect_count": len(indirect_files),
            "total_affected": len(affected_files),
        },

        "confidence": {
            "direct": "PROVEN",
            "indirect": "LIKELY",
        },
    }