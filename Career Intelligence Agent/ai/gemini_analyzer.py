import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_career(cv_text, job_title, missing_skills):

    prompt = f"""
You are a senior career advisor.

Candidate CV:
{cv_text[:5000]}

Target Job:
{job_title}

Missing Skills:
{", ".join(missing_skills)}

Analyze and provide:

1. Career Fit Analysis
2. Strengths
3. Weaknesses
4. Missing Skills Explanation
5. Learning Roadmap
6. Suggested Projects
7. Interview Preparation Tips
8. Salary Expectation

Return the answer in Markdown format.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"