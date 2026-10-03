"""
ProjectTwin Feature Impact Engine

Maps low-level code impact to higher-level software
features and predicts possible user-facing effects.

This module does NOT modify the repository.
"""


def _normalize_name(value):
    """Normalize a name for simple matching."""
    return (value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _humanize_name(value):
    """Convert a code-style name into readable text."""
    value = (value or "").strip()

    if not value:
        return "Unknown feature"

    value = value.replace("_", " ")
    value = value.replace("-", " ")

    return value.strip().capitalize()


def infer_feature_from_function(function_name):
    """
    Infer a likely feature name from a function name.

    This is an inference, not a guaranteed fact.
    """

    normalized = _normalize_name(function_name)

    feature_keywords = {
        "skill_gap": "Skill Gap Analysis",
        "skill": "Skill Analysis",
        "resume": "Resume Analysis",
        "analyze_resume": "Resume Analysis",
        "login": "User Authentication",
        "authenticate": "User Authentication",
        "signup": "User Registration",
        "register": "User Registration",
        "upload": "File Upload",
        "download": "File Download",
        "search": "Search",
        "recommend": "Recommendation",
        "recommendation": "Recommendation",
        "predict": "Prediction",
        "prediction": "Prediction",
        "dashboard": "Dashboard",
        "report": "Reporting",
        "generate_report": "Report Generation",
        "profile": "User Profile",
        "payment": "Payment Processing",
        "checkout": "Checkout",
        "notification": "Notifications",
        "email": "Email Communication",
        "chat": "Chat",
        "message": "Messaging",
    }

    for keyword, feature in feature_keywords.items():
        if keyword in normalized:
            return feature

    return _humanize_name(function_name)


def infer_feature_relationship(
    changed_function,
    dependent_function,
    changed_file,
    dependent_file
):
    """
    Infer the likely feature relationship between the changed
    component and its dependent component.

    Returns evidence describing why the feature relationship
    was inferred.
    """

    changed_name = _normalize_name(changed_function)
    dependent_name = _normalize_name(dependent_function)

    changed_feature = infer_feature_from_function(
        changed_function
    )

    dependent_feature = infer_feature_from_function(
        dependent_function
    )

    # Same feature family
    if (
        changed_feature.lower()
        == dependent_feature.lower()
    ):
        feature = changed_feature
        relationship = (
            f"{dependent_function}() and "
            f"{changed_function}() appear to participate "
            f"in the same feature."
        )

    # Resume -> skill gap relationship
    elif (
        "resume" in dependent_name
        and "skill" in changed_name
    ):
        feature = "Resume Skill Gap Analysis"
        relationship = (
            f"{dependent_function}() appears to consume "
            f"skill-related results produced by "
            f"{changed_function}()."
        )

    # Generic dependency-based inference
    else:
        feature = dependent_feature
        relationship = (
            f"{dependent_function}() depends on "
            f"{changed_function}(), so the functionality "
            f"associated with {dependent_function}() may "
            f"be affected."
        )

    return {
        "feature": feature,
        "relationship": relationship,
        "confidence": "INFERRED",
        "evidence": (
            f"Feature inferred from the relationship between "
            f"{dependent_file}:{dependent_function}() and "
            f"{changed_file}:{changed_function}()."
        ),
    }


def build_feature_impact(
    function_impact,
    changed_file,
    changed_function,
    change_type,
    change_description
):
    """
    Build feature-level impact predictions from existing
    function dependency evidence.

    Parameters:
        function_impact:
            Existing ProjectTwin function dependency results.

        changed_file:
            File containing the proposed change.

        changed_function:
            Function being changed.

        change_type:
            ADD / MODIFY / REMOVE.

        change_description:
            User's natural-language description of the change.

    Returns:
        List of feature-impact predictions.
    """

    feature_impacts = []

    if not function_impact:
        return feature_impacts

    for relationship in function_impact:

        dependent_file = relationship.get(
            "dependent_file"
        )

        dependent_function = relationship.get(
            "dependent_function"
        )

        relationship_changed_function = relationship.get(
            "changed_function"
        ) or changed_function

        if not dependent_function:
            continue

        feature_info = infer_feature_relationship(
            relationship_changed_function,
            dependent_function,
            changed_file,
            dependent_file
        )

        feature = feature_info["feature"]

        # MODIFY
        if change_type == "MODIFY":

            effect = (
                f"The {feature} feature may produce "
                f"different results or behavior if "
                f"{changed_function}() changes."
            )

        # REMOVE
        elif change_type == "REMOVE":

            effect = (
                f"The {feature} feature may be affected "
                f"because {dependent_function}() depends "
                f"on the removed {changed_function}() "
                f"function."
            )

        # ADD
        elif change_type == "ADD":

            effect = (
                f"The {feature} feature may require "
                f"integration with the new behavior in "
                f"{changed_function}()."
            )

        else:

            effect = (
                f"The {feature} feature may be affected "
                f"by the proposed change to "
                f"{changed_function}()."
            )

        feature_impacts.append({
            "feature": feature,
            "affected_file": dependent_file,
            "affected_function": dependent_function,
            "changed_file": changed_file,
            "changed_function": changed_function,
            "change_type": change_type,
            "impact_level": "POTENTIAL",
            "confidence": "INFERRED",
            "relationship": feature_info[
                "relationship"
            ],
            "evidence": feature_info[
                "evidence"
            ],
            "predicted_effect": effect,
            "change_description": change_description,
            "recommended_checks": [
                f"{dependent_function}()",
                f"{changed_function}()",
                f"Tests related to {feature}",
            ],
        })

    # Remove duplicates
    unique = {}

    for item in feature_impacts:

        key = (
            item["feature"],
            item["affected_file"],
            item["affected_function"],
        )

        unique[key] = item

    return list(unique.values())