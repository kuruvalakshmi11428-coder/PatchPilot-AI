import os

from dotenv import load_dotenv
from google import genai

from app.memory import remember

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"

def get_gemini_client():
    """Create a Gemini client with a request timeout."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    return genai.Client(
        api_key=api_key,
        http_options={
            "timeout": 60000,
        },
    )


def debug_code(code, error_message="", project_context=""):
    """Use Gemini to analyse Python code and suggest fixes."""

    if not code.strip():
        return "Please provide the Python code you want to debug."

    if not error_message.strip():
        error_message = (
            "No traceback supplied. Check the code for likely bugs "
            "and edge cases."
        )

    prompt = f"""
You are PatchPilot AI, a careful Python debugging assistant.

Analyse the supplied code and explain:
1. The likely root cause.
2. The exact code or logic causing the problem.
3. The corrected implementation.
4. Why the correction works.
5. Tests that should be run.
6. Any assumptions or uncertainties.

Rules:
- Do not claim code was executed unless it actually was.
- Do not claim tests passed unless they actually ran.
- Preserve the original program's intended behaviour.
- Explain the solution in beginner-friendly language.
- Never request passwords or API keys.

PROJECT CONTEXT:
{project_context[:12000]}

USER'S PYTHON CODE:
{code[:16000]}

ERROR MESSAGE OR TRACEBACK:
{error_message[:8000]}
"""

    try:
        client = get_gemini_client()

        response = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
            timeout=30,
        )

        answer = response.output_text

        remember(
            "ai_debug_analysis",
            (
                "Gemini analysed a debugging request. "
                f"Error supplied: {error_message[:300]}"
            ),
        )

        return answer

    except Exception as exc:
        return (
            "PatchPilot could not complete the Gemini request.\n\n"
            f"Error type: {type(exc).__name__}\n"
            f"Details: {exc}\n\n"
            "Check your API key, model availability, internet connection, "
            "and Gemini API quota."
        )