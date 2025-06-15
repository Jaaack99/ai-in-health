import openai
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_explanation_and_options(question: str, age: int, education: str, tone: str) -> tuple[str, list[str]]:
    """
    Generates an explanation tailored to the user's age, education, and tone preference,
    and returns a list of 2–3 related subtopics for further exploration.
    """

    # Customize tone guidance
    tone_instruction = (
        "Use a simple, clear, and engaging tone suitable for a general audience. "
        "Avoid jargon and explain concepts as if to a curious student."
        if tone == "informative"
        else "Use a precise and technical tone suitable for an educated reader familiar with scientific terminology."
    )

    # Age-based simplification guidance
    if age < 16:
        audience_note = "Explain the topic in very simple terms, suitable for a child or teenager."
    elif age < 25 and education in ["Primary", "Secondary"]:
        audience_note = "Explain the topic in simple and relatable terms, avoiding technical words."
    elif education in ["University", "PhD"]:
        audience_note = "Feel free to include moderate to advanced technical details."
    else:
        audience_note = "Keep the explanation clear and easy to follow."

    system_prompt = (
        f"You are an expert science communicator helping the public understand how AI is used in health.\n"
        f"Your job is to answer the user's question clearly and give 2–3 related subtopics to explore further.\n\n"
        f"{tone_instruction}\n"
        f"{audience_note}\n\n"
        f"Structure your response like this:\n"
        f"1. Start with a short paragraph (3–5 sentences) answering the question.\n"
        f"2. Then list 2 or 3 short, clickable subtopics the user could explore next.\n"
        f"Only use markdown formatting. No extra comments or instructions.\n"
    )

    user_prompt = f"User question: {question}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message["content"].strip()

        # Parse explanation and follow-up options
        lines = content.split("\n")
        explanation_lines = []
        options = []

        for line in lines:
            if line.strip().startswith("-") or line.strip().startswith("•"):
                options.append(line.strip("-• ").strip())
            elif line.strip():
                explanation_lines.append(line.strip())

        explanation = " ".join(explanation_lines)
        return explanation, options[:3]  # Limit to max 3 options

    except Exception as e:
        return f"❌ Error getting explanation: {e}", []