import streamlit as st

from app.agent import debug_code

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PatchPilot AI",
    page_icon="🛠️",
    layout="wide",
)

# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 17px;
        color: #9CA3AF;
        margin-top: 4px;
    }

    .feature-card {
        padding: 18px;
        border: 1px solid #374151;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🛠️ PatchPilot AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Your AI-powered Python debugging assistant"
    "</div>",
    unsafe_allow_html=True,
)

st.divider()

# --------------------------------------------------
# Introduction
# --------------------------------------------------

st.subheader("Debug smarter. Understand faster.")

st.write(
    "Paste your Python code, describe the error, and let Gemini "
    "analyse the problem and suggest a correction."
)

# --------------------------------------------------
# Feature cards
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🔍 Bug Analysis</h4>
            Identify likely bugs and their root causes.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🧠 AI Explanations</h4>
            Understand why a bug occurs and how to fix it.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🧪 Testing Guidance</h4>
            Get suggestions for tests that can verify a proposed fix.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# --------------------------------------------------
# AI debugging form
# --------------------------------------------------

st.header("🤖 AI Debugging Assistant")

with st.form("debugging_form"):
    project_context = st.text_area(
        "Project context (optional)",
        placeholder=(
            "Example: This is a Python calculator application "
            "using functions and unit tests."
        ),
        height=100,
    )

    code_input = st.text_area(
        "Python code",
        placeholder=(
            "Paste your Python code here...\n\n"
            "def subtract(a, b):\n"
            "    return a + b"
        ),
        height=220,
    )

    error_input = st.text_area(
        "Error message or problem description",
        placeholder=(
            "Example: subtract(10, 4) returns 14 instead of 6."
        ),
        height=120,
    )

    submitted = st.form_submit_button(
        "🧠 Analyse with Gemini",
        type="primary",
        use_container_width=True,
    )

# --------------------------------------------------
# Process debugging request
# --------------------------------------------------

if submitted:
    if not code_input.strip():
        st.warning("Please enter some Python code first.")

    else:
        with st.spinner(
            "PatchPilot is asking Gemini to analyse your code..."
        ):
            result = debug_code(
                code=code_input,
                error_message=error_input,
                project_context=project_context,
            )

        st.subheader("📋 Debugging Report")
        st.markdown(result)

st.divider()

st.caption(
    "PatchPilot AI | AI-assisted Python debugging | "
    "Powered by Google Gemini"
)