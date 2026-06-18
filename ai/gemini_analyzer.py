import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

if not API_KEY:
    raise Exception(
        "GEMINI_API_KEY not found in .env"
    )

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def analyze_career(
    cv_text,
    target_job,
    skill_gap
):

    prompt = f"""
You are a senior career advisor.

Candidate CV:

{cv_text[:5000]}

Target Job:

{target_job}

Skill Coverage:

{skill_gap["coverage"]}%

Matched Skills:

{", ".join(skill_gap["matched"])}

Missing Skills:

{", ".join(skill_gap["missing"])}

Please provide:

# Career Fit Analysis

# Strengths

# Weaknesses

# Missing Skills Explanation

# Learning Roadmap
(30-60-90 day plan)

# Suggested Portfolio Projects

# Interview Preparation Tips

# Salary Expectation

Return Markdown only.
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return (
            f"Gemini Error: {str(e)}"
        )