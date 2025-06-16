# 🧬 AI in Health – Educational Web App

This is a **Streamlit-based prototype** designed to make complex topics around **AI in healthcare** accessible to a broad audience. The app lets users ask natural-language questions, receive **tailored explanations** based on their background, and view **auto-generated visualizations** that clarify key concepts. It also supports **incremental exploration** by offering related subtopics to dive deeper into.

---

## 🧠 Architecture Overview

The prototype is organized around two modular **AI agents**, each fulfilling a distinct educational purpose:

### 1. Explainer Agent

- **Powered by:** OpenAI `gpt-4o`
- **Function:** Produces a clear, age- and education-tailored explanation of any user-submitted question about AI in health.
- **Tone Adaptation:** Based on user selection ("Informative" or "Scientific").
- **Output:** 
  - A short educational paragraph
  - 2–3 suggested subtopics for further exploration

### 2. Visualizer Agent

- **Powered by:** OpenAI `gpt-4o`
- **Function:** Converts a health-related AI concept into working `matplotlib` code.
- **Output:** A meaningful, simplified visualization that reinforces the main idea.
- **Execution:** Code is run safely in a sandboxed scope.

---

## How to Run the App

1. **Clone the repository**

```bash
git clone https://github.com/Jaaack99/ai-in-health.git
```

2. **Navigate to the folder**

```bash
cd ai-in-health
```

3. **Create and activate a virtual environment (optional)**

```bash
python -m venv venv
```
```bash
venv\Scripts\activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Create a .env file in the root directory with your OpenAI API key**

```bash
echo OPENAI_API_KEY=your-key-here > .env
```

6. **Run the app**

```bash
streamlit run app/main.py
```

---

## 💻 Usage

1. **Ask a question** about AI in healthcare.
2. **Enter your age and education level** to personalize the explanation.
3. **Choose a tone**: Informative (general public) or Scientific (more technical).
4. **Review the response**:
   - 📘 An explanation appears on the left.
   - 📊 A dynamic graph appears on the right.
   - 🔍 You can click suggested follow-up topics to explore further.

---

## 🔍 Tradeoffs of AI Use in the Prototype

| Aspect                     | Benefit                                                                 | Tradeoff                                                              |
|---------------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------|
| **Language Understanding** | Natural-language interface allows open-ended exploration                | Harder to constrain LLM answers to a fixed structure                  |
| **Adaptability**           | Responses adapt in tone, depth, and vocabulary                          | Can introduce inconsistencies or verbosity                            |
| **Code Generation**        | Fast visual creation via LLM-generated Python code                      | Risk of malformed or unexecutable code (had to add guardrails)        |
| **Knowledge Breadth**      | LLM can handle a wide range of health-AI topics                         | Hallucination risk—LLM may fabricate facts if prompt is ambiguous     |

---

## ⚙️ AI-Assisted Coding – Pros and Cons

### ✅ What worked well
- **Rapid prototyping**: LLMs accelerated the creation of both frontend (Streamlit UI) and backend logic (agents).
- **Dynamic content**: Being able to generate both explanations *and* charts gave the app real educational depth.
- **Modular design**: The AI-agent structure emerged naturally from asking LLMs to "split tasks" by purpose.

### ❌ What slowed me down
- **Code hallucinations**: LLM-generated matplotlib code occasionally referenced non-existent variables or used outdated syntax.
- **Hidden bugs**: Debugging was needed when the LLM silently failed or returned malformed Markdown.
- **UI quirks**: Maintaining layout consistency across recursive interactions required several iterations.

---

## 💡 Reflection

Building this app highlighted the **power of generative AI for fast idea-to-prototype translation**, especially in educational domains. However, it also reinforced the need for **clear boundaries and testing**, as AI assistance can just as easily introduce fragile or misleading elements into your codebase.

In this case:
- **AI sped me up** when brainstorming layouts, writing modular Python, and generating example visualizations.
- **AI misled me** when I trusted it to generate bug-free `matplotlib` code or markdown with consistent structure. It also misled me on fixing some very easy code bugs, which I eventually resolved manually.

The takeaway? **AI is a brilliant pair programmer**, but it’s not yet a replacement for *your* judgment, debugging, and interface design skills.

---

## 📦 Tech Stack

- [Streamlit](https://streamlit.io/) – UI Framework
- [OpenAI GPT-4o](https://platform.openai.com/docs) – LLM API
- [Matplotlib](https://matplotlib.org/) – Visualization
- [Python-dotenv](https://pypi.org/project/python-dotenv/) – API key management

---
