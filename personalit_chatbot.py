from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(">>>>", client.chat.completions)

QUESTIONS = [
    "Do you enjoy spending time alone or with other people?",
    "How do you usually feel at large social gatherings?",
    "Do you prefer planning ahead or being spontaneous?",
    "How do you react when faced with a stressful situation?",
    "Do you often seek new experiences or stick to what you know?"
]

def main():
    print("Personality Detection Chatbot\nAnswer the following questions:\n")

    answers = []
    for i, question in enumerate(QUESTIONS):
        ans = input(f"Q{i+1}: {question}\nYour answer: ")
        answers.append(ans)

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
    {answers}

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

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert psychologist and data analyst."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        content = response.choices[0].message.content.strip()
        print("\nPersonality Analysis Result:", response.choices[0], response.choices[0].message, response.choices[0].message.content)
        print(content)

    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
