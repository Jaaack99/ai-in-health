import openai
import matplotlib.pyplot as plt
import textwrap
import os
from dotenv import load_dotenv

# Load .env and set API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_graph_and_description(topic: str):
    """
    Calls OpenAI to generate a matplotlib chart based on the topic.
    Returns a matplotlib figure and a simple description.
    """

    system_prompt = (
        "You are a Python assistant helping visualize concepts related to how AI is used in healthcare. "
        "Your job is to write valid, runnable Python code using matplotlib to generate a simple, readable chart. "
        "Use mock or made-up data to illustrate trends. Only output code. Do not include explanations or markdown."
    )

    user_prompt = f"Create a matplotlib chart about: {topic}"

    try:
        # Request code from GPT
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6
        )

        code = response.choices[0].message["content"].strip()

        # Print code for debugging
        print("=== GENERATED CODE ===")
        print(code)
        print("======================")

        # Clean GPT output
        code = code.replace("```python", "").replace("```", "")
        code = code.replace("plt.show()", "")


        # Clear previous figures
        plt.clf()

        # Execute the cleaned code in a safe scope
        scope = {"plt": plt}
        exec(code, scope)

        # Get the figure
        fig = plt.gcf()
        if not fig.get_axes():
            raise ValueError("The generated code did not create a visible chart.")

        description = generate_description_from_topic(topic)
        return fig, description

    except Exception as e:
        return None, f"❌ Error generating or rendering graph: {e}"

def generate_description_from_topic(topic: str) -> str:
    """
    Generates a simple caption based on the topic.
    """
    return textwrap.fill(
        f"This graph supports the topic: '{topic}'. It visualizes one aspect of how AI can be applied in this area using simplified, illustrative data.",
        width=80
    )