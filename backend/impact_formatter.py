def format_impact_report(simulation, report, ai_analysis):
    """
    Create a clean human-readable summary of the simulated change.

    Parameters:
        simulation: predicted change information
        report: evidence-based impact report
        ai_analysis: Gemini explanation

    Returns:
        A formatted text report.
    """

    lines = []

    # ---------------------------------------------------------
    # CHANGE SUMMARY
    # ---------------------------------------------------------

    lines.append("PROJECTTWIN CHANGE SIMULATION")
    lines.append("=" * 60)

    lines.append(
        f"Changed File: {simulation.get('changed_file', 'Unknown')}"
    )

    changed_function = simulation.get("changed_function")

    if changed_function:
        lines.append(
            f"Changed Function: {changed_function}"
        )

    lines.append(
        f"Change Type: {simulation.get('change_type', 'MODIFY')}"
    )

    lines.append(
        f"Proposed Change: "
        f"{simulation.get('change_description', 'Unknown')}"
    )

    lines.append("")

    # ---------------------------------------------------------
    # IMPACT SUMMARY
    # ---------------------------------------------------------

    lines.append("IMPACT SUMMARY")
    lines.append("-" * 60)

    lines.append(
        f"Impacted Files: "
        f"{simulation.get('impact_count', 0)}"
    )

    direct = simulation.get("direct_dependencies", [])
    indirect = simulation.get("indirect_dependencies", [])

    lines.append(
        f"Direct Dependencies: {len(direct)}"
    )

    lines.append(
        f"Indirect Dependencies: {len(indirect)}"
    )

    lines.append("")

    # ---------------------------------------------------------
    # REMOVED
    # ---------------------------------------------------------

    removed = simulation.get("removed", [])

    lines.append("PREDICTED REMOVED")
    lines.append("-" * 60)

    if removed:
        for item in removed:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    lines.append("")

    # ---------------------------------------------------------
    # MODIFIED
    # ---------------------------------------------------------

    modified = simulation.get("modified", [])

    lines.append("PREDICTED MODIFIED")
    lines.append("-" * 60)

    if modified:
        for item in modified:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    lines.append("")

    # ---------------------------------------------------------
    # ADDED
    # ---------------------------------------------------------

    added = simulation.get("added", [])

    lines.append("PREDICTED ADDED")
    lines.append("-" * 60)

    if added:
        for item in added:
            lines.append(f"- {item}")
    else:
        lines.append("- None")

    lines.append("")

    # ---------------------------------------------------------
    # FUNCTION IMPACT
    # ---------------------------------------------------------

    function_impact = simulation.get(
        "function_impact",
        []
    )

    lines.append("FUNCTION-LEVEL IMPACT")
    lines.append("-" * 60)

    if function_impact:

        for relationship in function_impact:

            dependent_function = relationship.get(
                "dependent_function",
                "Unknown"
            )

            dependent_file = relationship.get(
                "dependent_file",
                "Unknown"
            )

            changed_function_name = relationship.get(
                "changed_function",
                "Unknown"
            )

            lines.append(
                f"- {dependent_function}() "
                f"in {dependent_file} "
                f"depends on "
                f"{changed_function_name}()"
            )

    else:
        lines.append("- No function-level relationships detected.")

    lines.append("")

    # ---------------------------------------------------------
    # POSSIBLE BREAKAGE
    # ---------------------------------------------------------

    possible_breakage = simulation.get(
        "possible_breakage",
        []
    )

    lines.append("POSSIBLE BREAKAGE")
    lines.append("-" * 60)

    if possible_breakage:

        for item in possible_breakage:

            file_name = item.get(
                "file",
                "Unknown"
            )

            function_name = item.get(
                "function"
            )

            reason = item.get(
                "reason",
                "No reason provided."
            )

            if function_name:
                lines.append(
                    f"- {file_name}:{function_name}()"
                )
            else:
                lines.append(
                    f"- {file_name}"
                )

            lines.append(
                f"  Reason: {reason}"
            )

    else:
        lines.append(
            "- No possible breakage identified."
        )

    lines.append("")

    # ---------------------------------------------------------
    # GIT EVIDENCE
    # ---------------------------------------------------------

    git_history = report.get(
        "git_history",
        ""
    )

    lines.append("GIT EVIDENCE")
    lines.append("-" * 60)

    if git_history:
        lines.append(git_history)
    else:
        lines.append(
            "- No Git history available."
        )

    lines.append("")

    # ---------------------------------------------------------
    # AI ANALYSIS
    # ---------------------------------------------------------

    lines.append("AI ANALYSIS")
    lines.append("-" * 60)

    if ai_analysis:
        lines.append(str(ai_analysis))
    else:
        lines.append(
            "- No AI analysis returned."
        )

    return "\n".join(lines)