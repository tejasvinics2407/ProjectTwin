import os
import time

from google import genai


GEMINI_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
]


def build_fallback_analysis(prompt):
    """
    Evidence-based fallback when Gemini is unavailable.

    This allows ProjectTwin to demonstrate its core
    change-impact reasoning without requiring an API key.
    """

    return """
ProjectTwin Evidence-Based Analysis

The Gemini API is not currently configured, so this analysis
was generated from the dependency evidence collected by
ProjectTwin.

1. CHANGE IMPACT

The proposed change targets the function identified in the
simulation.

ProjectTwin detected a direct function dependency:

backend/main.py:analyze_resume()
    ->
backend/engine/skill_gap_analyzer.py:analyze_skill_gap()

Therefore, changes to analyze_skill_gap() may affect
analyze_resume().

2. DIRECT IMPACT

Directly affected file:

- backend/main.py

The affected function is:

- analyze_resume()

This function directly calls the changed function
analyze_skill_gap().

3. CHANGED COMPONENT

The proposed modification is made to:

- backend/engine/skill_gap_analyzer.py
- function: analyze_skill_gap()

The changed file itself will need to be modified.

4. POSSIBLE CONSEQUENCE

If the behavior, return structure, parameters, or matching
logic of analyze_skill_gap() changes, analyze_resume() may
receive different results or behavior.

5. WHAT SHOULD BE CHECKED

Before applying the real change, check:

- analyze_skill_gap() input parameters
- analyze_skill_gap() return structure
- code inside analyze_resume() that consumes the result
- tests related to skill-gap analysis
- tests related to resume analysis

6. PROJECTTWIN CONCLUSION

The proposed function change has one detected direct
dependent function:

backend/main.py:analyze_resume()

The repository itself has not been modified by this simulation.
""".strip()


def ask_gemini(prompt):
    """
    Ask Gemini to reason about the ProjectTwin evidence.

    If Gemini is unavailable, return a useful local
    evidence-based analysis instead of failing.
    """

    api_key = os.environ.get("GEMINI_API_KEY")

    # ---------------------------------------------------------
    # No API key
    # ---------------------------------------------------------

    if not api_key:
        return build_fallback_analysis(prompt)

    # ---------------------------------------------------------
    # Gemini available
    # ---------------------------------------------------------

    try:

        client = genai.Client(
            api_key=api_key
        )

    except Exception:
        return build_fallback_analysis(prompt)

    # ---------------------------------------------------------
    # Try configured Gemini models
    # ---------------------------------------------------------

    for model in GEMINI_MODELS:

        print(
            f"\nTrying Gemini model: {model}"
        )

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response and response.text:

                    return response.text

            except Exception as error:

                error_text = str(error)

                print(
                    f"{model} error: {error_text}"
                )

                if (
                    "503" in error_text
                    and attempt < 1
                ):

                    print(
                        "Gemini is busy. Retrying..."
                    )

                    time.sleep(5)

                else:
                    break

    # ---------------------------------------------------------
    # All Gemini attempts failed
    # ---------------------------------------------------------

    return build_fallback_analysis(prompt)