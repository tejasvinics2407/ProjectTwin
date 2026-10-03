"""
ProjectTwin Repository-Grounded Feature Mapper

Builds feature relationships from the actual ProjectTwin
dependency/function evidence.

This module does not modify the repository.
"""


def _normalize(value):
    return (
        (value or "")
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def _humanize(value):
    value = (value or "").strip()

    if not value:
        return "Unknown Feature"

    return value.replace("_", " ").replace("-", " ").title()


def infer_feature_from_symbols(
    changed_function,
    dependent_function
):
    """
    Infer a feature from the actual relationship between
    the changed and dependent functions.

    This uses repository symbols as evidence rather than
    only looking at the changed function name.
    """

    changed = _normalize(changed_function)
    dependent = _normalize(dependent_function)

    # Resume + skill-gap workflow
    if "resume" in dependent and "skill" in changed:
        return {
            "feature": "Resume Skill Gap Analysis",
            "basis": (
                f"{dependent_function}() consumes functionality "
                f"provided by {changed_function}()."
            ),
        }

    # Authentication workflow
    if (
        any(word in dependent for word in [
            "login",
            "authenticate",
            "auth",
        ])
        and any(word in changed for word in [
            "login",
            "authenticate",
            "auth",
        ])
    ):
        return {
            "feature": "User Authentication",
            "basis": (
                f"{dependent_function}() is connected to "
                f"authentication functionality."
            ),
        }

    # Upload workflow
    if (
        "upload" in dependent
        or "upload" in changed
    ):
        return {
            "feature": "File Upload",
            "basis": (
                f"{dependent_function}() is connected to "
                f"file-upload functionality."
            ),
        }

    # Search workflow
    if (
        "search" in dependent
        or "search" in changed
    ):
        return {
            "feature": "Search",
            "basis": (
                f"{dependent_function}() is connected to "
                f"search functionality."
            ),
        }

    # Recommendation workflow
    if (
        "recommend" in dependent
        or "recommend" in changed
    ):
        return {
            "feature": "Recommendations",
            "basis": (
                f"{dependent_function}() is connected to "
                f"recommendation functionality."
            ),
        }

    # Prediction workflow
    if (
        "predict" in dependent
        or "predict" in changed
    ):
        return {
            "feature": "Prediction",
            "basis": (
                f"{dependent_function}() is connected to "
                f"prediction functionality."
            ),
        }

    # Dashboard workflow
    if (
        "dashboard" in dependent
        or "dashboard" in changed
    ):
        return {
            "feature": "Dashboard",
            "basis": (
                f"{dependent_function}() is connected to "
                f"dashboard functionality."
            ),
        }

    # Reporting workflow
    if (
        "report" in dependent
        or "report" in changed
    ):
        return {
            "feature": "Reporting",
            "basis": (
                f"{dependent_function}() is connected to "
                f"reporting functionality."
            ),
        }

    # Generic repository-grounded feature
    return {
        "feature": _humanize(dependent_function),
        "basis": (
            f"The feature is inferred from the repository "
            f"relationship between {dependent_function}() "
            f"and {changed_function}()."
        ),
    }


def map_feature_relationship(
    changed_file,
    changed_function,
    dependent_file,
    dependent_function,
    relationship_type="calls",
):
    """
    Convert a repository dependency relationship into a
    feature-level relationship.

    Returns:
        A repository-grounded feature mapping.
    """

    feature_info = infer_feature_from_symbols(
        changed_function,
        dependent_function,
    )

    return {
        "feature": feature_info["feature"],
        "changed_component": {
            "file": changed_file,
            "function": changed_function,
        },
        "dependent_component": {
            "file": dependent_file,
            "function": dependent_function,
        },
        "relationship_type": relationship_type,
        "confidence": "INFERRED",
        "basis": feature_info["basis"],
        "repository_grounded": True,
    }


def build_repository_feature_map(
    function_impact,
):
    """
    Build repository-grounded feature mappings from
    ProjectTwin's existing function dependency evidence.

    Parameters:
        function_impact:
            Function-level dependency relationships already
            detected by ProjectTwin.

    Returns:
        List of repository-grounded feature mappings.
    """

    mappings = []

    for relationship in function_impact:

        changed_file = relationship.get(
            "changed_file"
        )

        changed_function = relationship.get(
            "changed_function"
        )

        dependent_file = relationship.get(
            "dependent_file"
        )

        dependent_function = relationship.get(
            "dependent_function"
        )

        relationship_type = relationship.get(
            "relationship_type",
            "calls",
        )

        if not changed_function:
            continue

        if not dependent_function:
            continue

        mapping = map_feature_relationship(
            changed_file,
            changed_function,
            dependent_file,
            dependent_function,
            relationship_type,
        )

        mappings.append(mapping)

    # Remove duplicates
    unique = {}

    for mapping in mappings:

        key = (
            mapping["feature"],
            mapping["changed_component"]["file"],
            mapping["changed_component"]["function"],
            mapping["dependent_component"]["file"],
            mapping["dependent_component"]["function"],
        )

        unique[key] = mapping

    return list(unique.values())