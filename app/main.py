import streamlit as st
from agents.explainer import get_explanation_and_options
from agents.visualizer import generate_graph_and_description
from dotenv import load_dotenv
import os

load_dotenv()

# Optional: make sure the key is present, or exit
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ Missing OpenAI API Key. Please check your .env file.")
    st.stop()

st.set_page_config(layout="wide", page_title="AI in Health", page_icon="🧬")

# Session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.explanation = ""
    st.session_state.options = []
    st.session_state.selected_topic = ""
    st.session_state.fig = None
    st.session_state.graph_description = ""
    st.session_state.age = 30
    st.session_state.education = "University"
    st.session_state.tone = "informative"

st.title("🧬 Welcome to the AI in Health Demo")

st.markdown("### 👋 Hello! What would you like to know about AI in health?")
question = st.text_input("Your question")

with st.form("user_info_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Your age", 10, 80, 30)

    with col2:
        education = st.selectbox("Education level", ["Primary", "Secondary", "University", "PhD"])

    with col3:
        tone = st.radio("Answer style", ["Informative", "Technical"])

    submitted = st.form_submit_button("Submit")

if submitted and question:
    # Save inputs to session state
    st.session_state.submitted = True
    st.session_state.age = age
    st.session_state.education = education
    st.session_state.tone = tone.lower()

    # Get explanation + follow-ups
    st.session_state.explanation, st.session_state.options = get_explanation_and_options(
        question=question,
        age=age,
        education=education,
        tone=tone.lower()
    )

    # Generate initial graph
    st.session_state.fig, st.session_state.graph_description = generate_graph_and_description(question)

# After submission
if st.session_state.submitted:
    col_left, col_right = st.columns([2, 3])

    with col_left:
        st.subheader("📘 Explanation")
        st.markdown(st.session_state.explanation)

        st.subheader("🔍 Explore further:")
        for opt in st.session_state.options:
            if st.button(opt):
                st.session_state.selected_topic = opt

    with col_right:
        if st.session_state.fig:
            st.subheader("📊 Visual support")
            st.pyplot(st.session_state.fig)
            st.caption(st.session_state.graph_description)

# Deeper dive if a follow-up topic was selected
if st.session_state.selected_topic:
    st.divider()
    st.subheader(f"🔎 Deeper Dive: {st.session_state.selected_topic}")

    deeper_explanation, _ = get_explanation_and_options(
        question=st.session_state.selected_topic,
        age=st.session_state.age,
        education=st.session_state.education,
        tone=st.session_state.tone
    )
    st.markdown(deeper_explanation)

    deeper_fig, deeper_desc = generate_graph_and_description(st.session_state.selected_topic)
    if deeper_fig:
        st.pyplot(deeper_fig)
        st.caption(deeper_desc)
    else:
        st.warning("⚠️ Couldn’t generate a graph for the selected topic.")

    # Reset so user can click other topics later
    st.session_state.selected_topic = ""