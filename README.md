# Personality Detection Chatbot API

A **FastAPI** application that analyzes user responses to psychological questions and provides a personality assessment based on the **Big Five personality traits** using OpenAI's GPT models.

---

## Features

- Sequential question flow: ask one question at a time.
- Analyze user answers to determine:
  - **Openness to Experience**
  - **Conscientiousness**
  - **Extraversion**
  - **Agreeableness**
  - **Neuroticism**
- Provides JSON output with trait scores, explanations, and an overall summary.
- Detects whether a user is more **Introverted** or **Extroverted**.

---

## Prerequisites

- Python 3.10+
- OpenAI API key
- `pip` for installing dependencies

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/TehreemFati/personality-detection-chatbot.git
cd personality-detection-chatbot
```

2. Install dependencies:

```bash
pip install fastapi uvicorn python-dotenv openai
```

3. Create a .env file in the project root and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

4. Run the FastAPI server:

```bash
uvicorn main:app --reload
```