from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI 
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    models = client.models.list()
    print("Key works! Models available:", [m.id for m in models.data[:5]])
except Exception as e:
    print("Error:", e)

# Initialize FastAPI
app = FastAPI(
    title="Personality Detection Chatbot API",
    description="Analyzes user responses to determine personality traits",
    version="1.0"
)

# Request body model
class PersonalityRequest(BaseModel):
    question_index: int
    answers: list[str] = []

# List of questions (5 total)
QUESTIONS = [
    "Do you enjoy spending time alone or with other people?",
    "How do you usually feel at large social gatherings?",
    "Do you prefer planning ahead or being spontaneous?",
    "How do you react when faced with a stressful situation?",
    "Do you often seek new experiences or stick to what you know?"
]

@app.post('/analyze', tags=["Personality Detection"])
async def analyze_personality(request: PersonalityRequest):
    """Chatbot flow: ask one question at a time, and when done, analyze personality."""

    if request.question_index < len(QUESTIONS):
        return {
            "question": QUESTIONS[request.question_index],
            "next_index": request.question_index + 1
        }

    try:
        analysis_prompt = f"""
        You are a professional psychologist trained in the Big Five personality model:
        - Openness to Experience
        - Conscientiousness
        - Extraversion
        - Agreeableness
        - Neuroticism

        Analyze the following user's answers to psychological questions.
        Identify their Big Five scores (0–100), give a brief explanation for each,
        and provide an overall personality summary in plain language.

        User Answers:
        {request.answers}

        Format output as JSON:
        {{
            "openness": "score - explanation",
            "conscientiousness": "score - explanation",
            "extraversion": "score - explanation",
            "agreeableness": "score - explanation",
            "neuroticism": "score - explanation",
            "introvert_or_extrovert": "Introvert" or "Extrovert",
            "summary": "short plain summary"
        }}
        """

        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert psychologist and data analyst."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                },
            ],
            temperature = 0.7,
            max_tokens = 500
        )

        content = response.choices[0].message.content.strip()
        return {"personality_analysis": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))