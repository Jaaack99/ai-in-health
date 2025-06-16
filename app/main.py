import streamlit as st
from agents.explainer import get_explanation_and_options
from agents.visualizer import generate_graph_and_description
from dotenv import load_dotenv
import os
import textwrap

# Load environment variables
load_dotenv()

# Check API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ Missing OpenAI API Key. Please check your .env file.")
    st.stop()

# App layout
st.set_page_config(layout="wide", page_title="AI in Health", page_icon="🧬")

# Initialize session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False
    st.session_state.explanation = ""
    st.session_state.options = []
    st.session_state.selected_topic = ""
    st.session_state.fig = None
    st.session_state.graph_description = ""
    st.session_state.age = 30
    st.session_state.education = "University"
    st.session_state.tone = "Informative (for a more generic answer)"

# App UI
st.title("🧬 Welcome to the AI in Health Demo!")

st.markdown("### 👋 What would you like to know about AI in health?")
question = st.text_input("Your question")

# User form
with st.form("user_info_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Your age", 10, 80, 30)

    with col2:
        education = st.selectbox("Education level", ["Primary", "Secondary", "University", "PhD"])

    with col3:
        tone = st.radio("Answer style", ["Informative (for a more generic answer)", "Scientific (for a more technical answer)"])

    submitted = st.form_submit_button("Submit")

# On submit: get first explanation + graph
# On submit: reset previous outputs and get new explanation + graph
if submitted and question:
    st.session_state.submitted = True
    st.session_state.age = age
    st.session_state.education = education
    st.session_state.tone = tone.lower()

    # Clear old outputs
    st.session_state.explanation = ""
    st.session_state.options = []
    st.session_state.selected_topic = ""
    st.session_state.fig = None
    st.session_state.graph_description = ""

    # Get new explanation and visuals
    st.session_state.explanation, st.session_state.options = get_explanation_and_options(
        question=question,
        age=age,
        education=education,
        tone=tone.lower()
    )

    st.session_state.fig, st.session_state.graph_description = generate_graph_and_description(question)

# Main response display
if st.session_state.submitted:
    col_left, _, col_right = st.columns([2, 0.5, 3])

    with col_left:
        st.subheader("📘 Explanation")
        st.markdown(" ")  # space below title
        wrapped_explanation = f"""
        <div style='text-align: justify; max-width: 650px;'>
            {st.session_state.explanation}
        </div>
        """
        st.markdown(wrapped_explanation, unsafe_allow_html=True)



        st.subheader("🔍 Explore further:")
        for opt in st.session_state.options:
            if st.button(opt):
                st.session_state.selected_topic = opt

    with col_right:
        if st.session_state.fig:
            st.subheader("📊 Visual support")
            st.markdown(" ")  # space below title
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

    col_deep_left, _, col_deep_right = st.columns([2, 0.5, 3])

    with col_deep_left:
        st.markdown(" ")
        wrapped_deeper_explanation = f"""
        <div style='text-align: justify; max-width: 650px;'>
            {deeper_explanation}
        </div>
        """
        st.markdown(wrapped_deeper_explanation, unsafe_allow_html=True)


    with col_deep_right:
        st.markdown(" ")
        deeper_fig, deeper_desc = generate_graph_and_description(st.session_state.selected_topic)
        if deeper_fig:
            st.pyplot(deeper_fig)
            st.caption(deeper_desc)
        else:
            st.warning("⚠️ Couldn’t generate a graph for the selected topic.")
