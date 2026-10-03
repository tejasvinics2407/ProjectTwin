from backend.impact_analyzer import find_impact
from backend.dependency_impact import analyze_dependency_impact


def classify_change(change_description):

    """
    Classify the proposed software change.
    """

    description = change_description.lower()

    if any(
        word in description
        for word in [
            "remove",
            "delete",
            "drop",
            "eliminate"
        ]
    ):
        return "REMOVE"

    if any(
        word in description
        for word in [
            "add",
            "create",
            "introduce",
            "implement"
        ]
    ):
        return "ADD"

    if any(
        word in description
        for word in [
            "change",
            "modify",
            "update",
            "replace",
            "refactor",
            "improve"
        ]
    ):
        return "MODIFY"

    return "MODIFY"


def find_direct_dependencies(graph, changed_file):

    """
    Find files that directly depend on the changed file.
    """

    direct_dependencies = []

    for source, target in graph.edges():

        if target == changed_file:

            direct_dependencies.append(
                source
            )

    return sorted(
        set(direct_dependencies)
    )


def find_indirect_dependencies(
    graph,
    changed_file
):

    """
    Find files indirectly affected by a whole-file change.
    """

    direct = set(
        find_direct_dependencies(
            graph,
            changed_file
        )
    )

    all_affected = set(
        find_impact(
            graph,
            changed_file
        )[
            "affected_files"
        ]
    )

    indirect = all_affected - direct

    return sorted(
        indirect
    )


def find_function_impact(
    function_dependencies,
    changed_file,
    changed_function
):

    """
    Find exact functions that depend on
    the changed function.
    """

    function_impact = []

    if not changed_function:
        return function_impact

    for dependency in function_dependencies:

        target_file = dependency.get(
            "target_file"
        )

        target_function = dependency.get(
            "target_function"
        )

        source_file = dependency.get(
            "source_file"
        )

        source_function = dependency.get(
            "source_function"
        )

        if target_file != changed_file:
            continue

        if target_function != changed_function:
            continue

        if (
            source_file == changed_file
            and source_function == changed_function
        ):
            continue

        function_impact.append(
            {
                "changed_file": target_file,
                "changed_function": target_function,

                "dependent_file": source_file,
                "dependent_function": source_function,

                "assigned_to": dependency.get(
                    "assigned_to"
                ),

                "call_line": dependency.get(
                    "call_line"
                )
            }
        )

    return function_impact


def find_function_affected_files(
    function_impact
):

    """
    Convert function relationships into affected files.
    """

    affected_files = set()

    for relationship in function_impact:

        dependent_file = relationship.get(
            "dependent_file"
        )

        if dependent_file:

            affected_files.add(
                dependent_file
            )

    return sorted(
        affected_files
    )


def find_test_impact(
    graph,
    changed_file
):

    """
    Find test files that directly depend
    on the changed file.
    """

    test_files = []

    direct_dependencies = (
        find_direct_dependencies(
            graph,
            changed_file
        )
    )

    for file in direct_dependencies:

        normalized = file.replace(
            "\\",
            "/"
        ).lower()

        if (
            normalized.startswith("tests/")
            or "/tests/" in normalized
            or normalized.startswith("test_")
            or "/test_" in normalized
        ):

            test_files.append(
                file
            )

    return sorted(
        set(test_files)
    )


def build_function_breakage(
    function_impact
):

    """
    Create evidence-based explanations
    for function dependencies.
    """

    possible_breakage = []

    for relationship in function_impact:

        dependent_file = relationship[
            "dependent_file"
        ]

        dependent_function = relationship[
            "dependent_function"
        ]

        changed_file = relationship[
            "changed_file"
        ]

        changed_function = relationship[
            "changed_function"
        ]

        assigned_to = relationship.get(
            "assigned_to"
        )

        call_line = relationship.get(
            "call_line"
        )

        reason = (
            f"{dependent_function}() in "
            f"{dependent_file} depends on "
            f"{changed_function}() in "
            f"{changed_file}"
        )

        if assigned_to:

            reason += (
                f". The result is assigned to "
                f"'{assigned_to}'"
            )

        if call_line:

            reason += (
                f" at line {call_line}"
            )

        possible_breakage.append(
            {
                "file": dependent_file,
                "function": dependent_function,
                "reason": reason
            }
        )

    return possible_breakage


def build_consequence_analysis(
    function_impact,
    change_type,
    change_description
):

    """
    Generate structured consequence predictions
    from dependency and data-flow evidence.

    These are predictions, not guarantees.
    """

    consequences = []

    for relationship in function_impact:

        dependent_file = relationship[
            "dependent_file"
        ]

        dependent_function = relationship[
            "dependent_function"
        ]

        changed_function = relationship[
            "changed_function"
        ]

        assigned_to = relationship.get(
            "assigned_to"
        )

        if change_type == "MODIFY":

            if assigned_to:

                consequences.append(
                    {
                        "type": "DATA_FLOW",

                        "severity": "POTENTIAL",

                        "file": dependent_file,

                        "function": dependent_function,

                        "reason": (
                            f"{dependent_function}() receives "
                            f"the result of {changed_function}() "
                            f"through '{assigned_to}'. "
                            f"Changing the result structure or "
                            f"meaning may affect downstream logic."
                        )
                    }
                )

            else:

                consequences.append(
                    {
                        "type": "BEHAVIOR",

                        "severity": "POTENTIAL",

                        "file": dependent_file,

                        "function": dependent_function,

                        "reason": (
                            f"{dependent_function}() directly "
                            f"depends on {changed_function}(). "
                            f"Changes to its behavior may affect "
                            f"the caller."
                        )
                    }
                )

        elif change_type == "REMOVE":

            consequences.append(
                {
                    "type": "BREAKAGE",

                    "severity": "HIGH",

                    "file": dependent_file,

                    "function": dependent_function,

                    "reason": (
                        f"{dependent_function}() calls the "
                        f"function {changed_function}(). "
                        f"Removing it may leave this caller "
                        f"without the required function."
                    )
                }
            )

        elif change_type == "ADD":

            consequences.append(
                {
                    "type": "BEHAVIOR",

                    "severity": "POTENTIAL",

                    "file": dependent_file,

                    "function": dependent_function,

                    "reason": (
                        f"{changed_function}() is being extended "
                        f"or introduced. The caller should be "
                        f"checked for compatibility with the "
                        f"new behavior."
                    )
                }
            )

    return consequences


def predict_change(
    graph,
    changed_file,
    change_description,
    function_dependencies=None,
    changed_function=None,
    dependency_model=None
):

    """
    Predict consequences of a proposed software change.

    Function-level changes can use the new
    language-independent DependencyModel.

    The existing Python dependency logic is retained
    as a fallback for compatibility.
    """

    if function_dependencies is None:
        function_dependencies = []

    change_type = classify_change(
        change_description
    )

    # =========================================================
    # LANGUAGE-INDEPENDENT IMPACT
    # =========================================================

    dependency_impact = None

    if dependency_model is not None:

        dependency_impact = (
            analyze_dependency_impact(
                dependency_model,
                changed_file,
                changed_function
            )
        )

    # =========================================================
    # FUNCTION-LEVEL SIMULATION
    # =========================================================

    if changed_function:

        # -----------------------------------------------------
        # New language-independent engine
        # -----------------------------------------------------

        if dependency_impact is not None:

            direct_relationships = (
                dependency_impact[
                    "direct_impact"
                ]
            )

            function_impact = []

            for relationship in (
                direct_relationships
            ):

                if (
                    relationship[
                        "relationship_type"
                    ]
                    != "calls"
                ):
                    continue

                function_impact.append(
                    {
                        "changed_file": (
                            relationship[
                                "target_file"
                            ]
                        ),

                        "changed_function": (
                            relationship[
                                "target_symbol"
                            ]
                        ),

                        "dependent_file": (
                            relationship[
                                "source_file"
                            ]
                        ),

                        "dependent_function": (
                            relationship[
                                "source_symbol"
                            ]
                        ),

                        "assigned_to": None,

                        "call_line": None
                    }
                )

            affected_files = (
                dependency_impact[
                    "affected_files"
                ]
            )

            direct_dependencies = sorted(
                set(
                    relationship[
                        "source_file"
                    ]
                    for relationship
                    in direct_relationships
                )
            )

            indirect_dependencies = (
                dependency_impact[
                    "indirect_impact"
                ]
            )

        # -----------------------------------------------------
        # Existing Python fallback
        # -----------------------------------------------------

        else:

            function_impact = (
                find_function_impact(
                    function_dependencies,
                    changed_file,
                    changed_function
                )
            )

            affected_files = (
                find_function_affected_files(
                    function_impact
                )
            )

            direct_dependencies = (
                affected_files
            )

            indirect_dependencies = []

        # -----------------------------------------------------
        # Existing test analysis
        # -----------------------------------------------------

        test_files = find_test_impact(
            graph,
            changed_file
        )

        removed = []
        modified = []
        added = []

        if change_type == "MODIFY":

            modified.append(
                changed_file
            )

            modified.extend(
                affected_files
            )

        elif change_type == "REMOVE":

            modified.append(
                changed_file
            )

            modified.extend(
                affected_files
            )

        elif change_type == "ADD":

            modified.append(
                changed_file
            )

        possible_breakage = (
            build_function_breakage(
                function_impact
            )
        )

        # -----------------------------------------------------
        # Test evidence
        # -----------------------------------------------------

        for test_file in test_files:

            possible_breakage.append(
                {
                    "file": test_file,

                    "reason": (
                        f"{test_file} directly depends on "
                        f"{changed_file} and should be reviewed "
                        f"after changing {changed_function}()"
                    )
                }
            )

        # -----------------------------------------------------
        # Consequence analysis
        # -----------------------------------------------------

        consequences = (
            build_consequence_analysis(
                function_impact,
                change_type,
                change_description
            )
        )

        return {
            "changed_file": changed_file,

            "changed_function": changed_function,

            "change_description": change_description,

            "change_type": change_type,

            "impact_count": len(
                set(affected_files)
                | {changed_file}
            ),

            "affected_files": affected_files,

            "direct_dependencies": (
                direct_dependencies
            ),

            "indirect_dependencies": (
                indirect_dependencies
            ),

            "function_impact": function_impact,

            "test_impact": test_files,

            "consequences": consequences,

            "removed": sorted(
                set(removed)
            ),

            "modified": sorted(
                set(modified)
            ),

            "added": sorted(
                set(added)
            ),

            "possible_breakage": possible_breakage,

            "dependency_engine": (
                "language-independent"
                if dependency_model is not None
                else "python-legacy"
            )
        }

    # =========================================================
    # WHOLE-FILE SIMULATION
    # =========================================================

    if dependency_impact is not None:

        affected_files = (
            dependency_impact[
                "affected_files"
            ]
        )

        direct_dependencies = []

        for relationship in (
            dependency_impact[
                "direct_impact"
            ]
        ):

            source_file = (
                relationship[
                    "source_file"
                ]
            )

            if source_file not in direct_dependencies:

                direct_dependencies.append(
                    source_file
                )

        indirect_dependencies = (
            dependency_impact[
                "indirect_impact"
            ]
        )

    else:

        impact = find_impact(
            graph,
            changed_file
        )

        affected_files = impact[
            "affected_files"
        ]

        direct_dependencies = (
            find_direct_dependencies(
                graph,
                changed_file
            )
        )

        indirect_dependencies = (
            find_indirect_dependencies(
                graph,
                changed_file
            )
        )

    test_files = find_test_impact(
        graph,
        changed_file
    )

    function_impact = []

    consequences = []

    removed = []

    modified = []

    added = []

    possible_breakage = []

    # ---------------------------------------------------------
    # REMOVE FILE
    # ---------------------------------------------------------

    if change_type == "REMOVE":

        removed.append(
            changed_file
        )

        modified.extend(
            direct_dependencies
        )

        for file in direct_dependencies:

            possible_breakage.append(
                {
                    "file": file,

                    "reason": (
                        f"{file} depends directly on "
                        f"{changed_file}"
                    )
                }
            )

        for file in indirect_dependencies:

            possible_breakage.append(
                {
                    "file": file,

                    "reason": (
                        f"{file} is indirectly affected "
                        f"through project dependencies"
                    )
                }
            )

    # ---------------------------------------------------------
    # MODIFY FILE
    # ---------------------------------------------------------

    elif change_type == "MODIFY":

        modified.append(
            changed_file
        )

        modified.extend(
            direct_dependencies
        )

        for file in direct_dependencies:

            possible_breakage.append(
                {
                    "file": file,

                    "reason": (
                        f"{file} directly depends on "
                        f"{changed_file}"
                    )
                }
            )

        for file in indirect_dependencies:

            possible_breakage.append(
                {
                    "file": file,

                    "reason": (
                        f"{file} is indirectly affected "
                        f"through project dependencies"
                    )
                }
            )

    # ---------------------------------------------------------
    # ADD FILE
    # ---------------------------------------------------------

    elif change_type == "ADD":

        added.append(
            changed_file
        )

    return {
        "changed_file": changed_file,

        "changed_function": None,

        "change_description": change_description,

        "change_type": change_type,

        "impact_count": len(
            set(affected_files)
            | {changed_file}
        ),

        "affected_files": affected_files,

        "direct_dependencies": (
            direct_dependencies
        ),

        "indirect_dependencies": (
            indirect_dependencies
        ),

        "function_impact": function_impact,

        "test_impact": test_files,

        "consequences": consequences,

        "removed": sorted(
            set(removed)
        ),

        "modified": sorted(
            set(modified)
        ),

        "added": sorted(
            set(added)
        ),

        "possible_breakage": possible_breakage,

        "dependency_engine": (
            "language-independent"
            if dependency_model is not None
            else "python-legacy"
        )
    }