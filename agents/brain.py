import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = """
Kamu adalah OpenClaw-style Autonomous AI Agent.

Kamu mampu:
- berpikir langkah demi langkah
- membuat rencana
- menyelesaikan tugas
- membantu user secara autonomous
"""

def think(messages):

    response = client.chat.completions.create(
        model="openchat/openchat-7b:free",
        messages=messages,
        temperature=0.7,
        max_tokens=1200
    )

    return response.choices[0].message.content
