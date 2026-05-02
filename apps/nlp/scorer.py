import json
import requests
import time
from django.conf import settings


MODELS = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-3-12b-it:free",
]


def evaluate_relevance(topic_name, topic_description, resource_title, resource_text):
    """
    Evaluate the relevance of a resource to a topic using OpenRouter LLM.
    Returns dict with score, label, reason, key_matches, missing.
    """
    # Trim resource text to avoid token limits
    resource_text_trimmed = resource_text[:2000] if resource_text else "Matn mavjud emas"

    prompt = f"""You are a STRICT educational resource relevance evaluator.

    Topic Name: {topic_name}
    Topic Description: {topic_description}

    Resource Title: {resource_title}
    Resource Content: {resource_text_trimmed}

    Your job is to evaluate if this resource DIRECTLY teaches the topic above.

    STRICT RULES:
    - Score HIGH (0.70-1.0) ONLY if the resource DIRECTLY and SPECIFICALLY covers the topic
    - Score MEDIUM (0.40-0.69) if the resource is partially related but missing key concepts
    - Score LOW (0.0-0.39) if the resource is about a DIFFERENT subject entirely
    - A Python programming resource for a Biology topic = LOW score (0.05-0.15)
    - A Math resource for a History topic = LOW score
    - Do NOT give high scores just because a subject CAN be used to study another subject indirectly
    - Be STRICT. When in doubt, score LOWER.

    LANGUAGE RULES:
    - The resource can be in ANY language (Uzbek, Russian, English, etc.)
    - Always evaluate the MEANING and CONTENT, not the language
    - The reason field must always be written in Uzbek language
    - key_matches should use the same language as the resource
    - A Russian biology textbook about fotosintez = HIGH score for Fotosintez topic
    - An English Python tutorial for a Biology topic = LOW score

    Return ONLY a valid JSON object, no extra text:
    {{
        "score": 0.08,
        "label": "Low",
        "reason": "Sabab o'zbek tilida",
        "key_matches": [],
        "missing": ["mavzu1", "mavzu2"]
    }}

    Rules:
    - score: float 0.0 to 1.0
    - label: exactly "High" (>=0.70), "Medium" (>=0.40), or "Low" (<0.40)
    - reason: in Uzbek language, explain clearly why relevant or NOT relevant
    - key_matches: keywords from resource matching the topic (empty list if not relevant)
    - missing: important topic concepts missing from the resource (max 5)
    """

    last_error = None
    for model in MODELS:
        try:
            result = _call_openrouter(model, prompt)
            if result:
                return result
        except Exception as e:
            last_error = e
            time.sleep(1)
            continue

    # Fallback if all models fail
    raise Exception(f"Barcha modellar ishlamadi: {last_error}")


def _call_openrouter(model, prompt):
    """Make API call to OpenRouter."""
    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        raise Exception("OPENROUTER_API_KEY sozlanmagan")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://edurelevance.app",
        "X-Title": "EduRelevance"
    }

    payload = {
        "model": model,
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"API xato {response.status_code}: {response.text}")

    data = response.json()
    content = data['choices'][0]['message']['content'].strip()

    # Clean up response in case of markdown wrapping
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    content = content.strip()

    result = json.loads(content)

    # Validate and normalize
    score = float(result.get('score', 0.5))
    score = max(0.0, min(1.0, score))

    label = result.get('label', '')
    if label not in ['High', 'Medium', 'Low']:
        if score >= 0.70:
            label = 'High'
        elif score >= 0.40:
            label = 'Medium'
        else:
            label = 'Low'

    # Normalize label to db values
    label_map = {'High': 'high', 'Medium': 'medium', 'Low': 'low'}
    label = label_map.get(label, 'low')

    return {
        'score': score,
        'label': label,
        'reason': result.get('reason', 'Baholash amalga oshirildi'),
        'key_matches': result.get('key_matches', []),
        'missing': result.get('missing', [])
    }
