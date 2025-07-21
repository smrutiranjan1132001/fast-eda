import openai
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import os
import pandasql as psql
import re

load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("API Key loaded:", os.getenv("OPENAI_API_KEY") is not None)




def ask_question(df: pd.DataFrame, query: str) -> str:
    df_head = df.head(3).to_string(index=False)

    prompt = f"""
    You are a data analyst. Here's a sample of a pandas DataFrame named `df`:
    {df_head}

    Write a SQL query to answer this question:
    \"\"\"{query}\"\"\"

    Only return the raw SQL query without explanation. Assume table name is 'df'.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert SQL data analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract SQL query and clean markdown/code block formatting
        raw_sql = response.choices[0].message.content.strip()
        # Remove triple backticks and 'sql' if present
        cleaned_sql = re.sub(r"^```sql\\s*|```$", "", raw_sql, flags=re.IGNORECASE).strip()

        # Run the SQL
        result_df = psql.sqldf(cleaned_sql, {"df": df})

        # Return nicely formatted response
        if result_df.empty:
            return f"✅ Generated SQL:\n```sql\n{cleaned_sql}\n```\n\nNo matching results."
        else:
            return f"✅ Generated SQL:\n```sql\n{cleaned_sql}\n```\n\n{result_df.to_markdown(index=False)}"

    except Exception as e:
        return f"❌ Error occurred: {str(e)}\n\nTried SQL:\n```sql\n{cleaned_sql}```"