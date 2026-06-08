import json
import re
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


def enrich_company(
    website_url,
    content,
    emails,
    phones
):

    prompt = f"""
You are an expert business analyst.

STRICT RULES:

1. Extract only information present in the website content.
2. Never invent emails.
3. Never invent phone numbers.
4. Never invent addresses.
5. If unavailable return empty string "".
6. For mail return [].
7. Keep responses concise.
8. Return VALID JSON ONLY.

Website URL:
{website_url}

Detected Emails:
{emails}

Detected Phones:
{phones}

Website Content:
{content}

Return:

{{
  "website_name":"",
  "company_name":"",
  "address":"",
  "mobile_number":"",
  "mail":[],
  "core_service":"",
  "target_customer":"",
  "probable_pain_point":"",
  "outreach_opener":""
}}
"""

    response = llm.invoke(prompt)

    text = response.content.strip()

    text = text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    )

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        raise Exception(
            f"Unable to parse LLM response: {text}"
        )

    return json.loads(
        match.group()
    )
