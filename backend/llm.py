import json
import re

from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

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
            "Unable to parse Gemini response"
        )

    return json.loads(
        match.group()
    )