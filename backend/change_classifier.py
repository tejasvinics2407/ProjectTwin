"""
ProjectTwin Semantic Change Classifier

Classifies a proposed software change into a more specific
semantic category.

This is a heuristic classifier based on the user's change
description. It does not modify the repository.
"""


def classify_semantic_change(change_description):
    """
    Classify the semantic nature of a proposed software change.

    Returns:
        dict containing:
        - category
        - confidence
        - evidence
    """

    description = (change_description or "").strip().lower()

    if not description:
        return {
            "category": "UNKNOWN",
            "confidence": "LOW",
            "evidence": "No change description was provided.",
        }

    # ---------------------------------------------------------
    # RETURN CONTRACT
    # ---------------------------------------------------------

    return_keywords = [
        "return value",
        "return type",
        "return structure",
        "return format",
        "output format",
        "response format",
        "response structure",
        "change what it returns",
        "change the returned",
    ]

    if any(keyword in description for keyword in return_keywords):
        return {
            "category": "RETURN_CONTRACT",
            "confidence": "HIGH",
            "evidence": (
                "The change description refers to the function's "
                "returned value, type, structure, or output format."
            ),
        }

    # ---------------------------------------------------------
    # INPUT CONTRACT
    # ---------------------------------------------------------

    input_keywords = [
        "parameter",
        "parameters",
        "argument",
        "arguments",
        "input",
        "inputs",
        "function signature",
        "signature",
    ]

    if any(keyword in description for keyword in input_keywords):
        return {
            "category": "INPUT_CONTRACT",
            "confidence": "HIGH",
            "evidence": (
                "The change description refers to function inputs, "
                "arguments, parameters, or the function signature."
            ),
        }

    # ---------------------------------------------------------
    # API COMPATIBILITY
    # ---------------------------------------------------------

    api_keywords = [
        "api",
        "endpoint",
        "route",
        "request format",
        "http response",
        "http request",
        "breaking api",
        "api contract",
    ]

    if any(keyword in description for keyword in api_keywords):
        return {
            "category": "API_COMPATIBILITY",
            "confidence": "HIGH",
            "evidence": (
                "The change description refers to an API, endpoint, "
                "request, response, or API contract."
            ),
        }

    # ---------------------------------------------------------
    # DATA FLOW
    # ---------------------------------------------------------

    data_keywords = [
        "data flow",
        "data structure",
        "database",
        "schema",
        "query",
        "field",
        "column",
        "record",
        "store",
        "save data",
        "load data",
    ]

    if any(keyword in description for keyword in data_keywords):
        return {
            "category": "DATA_FLOW",
            "confidence": "HIGH",
            "evidence": (
                "The change description refers to data movement, "
                "storage, schemas, database operations, or data structures."
            ),
        }

    # ---------------------------------------------------------
    # STRUCTURAL
    # ---------------------------------------------------------

    structural_keywords = [
        "rename",
        "move file",
        "move function",
        "move class",
        "split file",
        "merge files",
        "new class",
        "new function",
        "remove function",
        "delete function",
        "remove class",
        "delete class",
        "refactor",
        "restructure",
    ]

    if any(keyword in description for keyword in structural_keywords):
        return {
            "category": "STRUCTURAL",
            "confidence": "HIGH",
            "evidence": (
                "The change description refers to changing the "
                "structure, organization, or existence of project components."
            ),
        }

    # ---------------------------------------------------------
    # BEHAVIORAL
    # ---------------------------------------------------------

    behavioral_keywords = [
        "logic",
        "calculation",
        "algorithm",
        "behavior",
        "behaviour",
        "validation",
        "condition",
        "rule",
        "matching",
        "calculation logic",
        "change how",
        "modify how",
    ]

    if any(keyword in description for keyword in behavioral_keywords):
        return {
            "category": "BEHAVIORAL",
            "confidence": "MEDIUM",
            "evidence": (
                "The change description refers to changing the "
                "logic, rules, calculations, validation, or behavior."
            ),
        }

    # ---------------------------------------------------------
    # GENERIC MODIFY
    # ---------------------------------------------------------

    if any(
        keyword in description
        for keyword in ["modify", "change", "update", "improve", "edit"]
    ):
        return {
            "category": "BEHAVIORAL",
            "confidence": "LOW",
            "evidence": (
                "The change is described as a general modification, "
                "but its specific semantic effect could not be determined."
            ),
        }

    # ---------------------------------------------------------
    # UNKNOWN
    # ---------------------------------------------------------

    return {
        "category": "UNKNOWN",
        "confidence": "LOW",
        "evidence": (
            "The change description does not contain enough information "
            "to determine its semantic category."
        ),
    }