import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("No se encontró la clave OPENAI_API_KEY en el archivo .env")

def extract_claims(text: str) -> list:

    prompt = f"Extract health-related claims from the following text:\n\n{text}\n\nSeparate each claim with a new line."
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in identifying health-related claims."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.7,
    )
    claims = response['choices'][0]['message']['content'].strip().split("\n")
    return [claim.strip() for claim in claims if claim.strip()]

def remove_duplicates(claims: list) -> list:

    unique_claims = list(set(claims))
    return unique_claims

def verify_claim(claim: str) -> dict:

    prompt = f"Verify the following claim using reliable scientific journals:\n\n{claim}\n\nProvide a summary of the verification."
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a reliable verifier of scientific claims."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.7,
    )
    verification = response['choices'][0]['message']['content'].strip()
    return {
        "claim": claim,
        "verification": verification
    }
