from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_code_explanation(query, code_snippets):

    context = "\n\n".join(code_snippets)

    prompt = f"""
You are a senior software engineer helping analyze a codebase.

User Question:
{query}

Relevant Code Snippets:
{context}

Explain clearly how the code works.
Mention filenames if useful.
Be concise but technical.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert software engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content