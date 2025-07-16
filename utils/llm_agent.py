import openai
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("API Key loaded:", os.getenv("OPENAI_API_KEY") is not None)


def ask_question(df: pd.DataFrame, query: str) -> str:
    df_head = df.head(5).to_csv(index=False)
    prompt = f"""You are a data science assistant. Here's a dataset preview:
{df_head}

Answer this question about the dataset: {query}
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert data analyst."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

