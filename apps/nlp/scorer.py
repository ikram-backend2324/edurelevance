import json
import requests
import time
from django.conf import settings


MODELS = [
    "meta-llama/llama-3.1-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-3-12b-it:free",
]

LANG_INSTRUCTIONS = {
    'uz': "Respond in Uzbek language.",
    'ru': "Respond in Russian language.",
    'en': "Respond in English language.",
}


def evaluate_relevance(topic_name, topic_description, resource_title, resource_text):
    return evaluate_relevance_with_lang(topic_name, topic_description, resource_title, resource_text, language='uz')


def evaluate_relevance_with_lang(topic_name, topic_description, resource_title, resource_text, language='uz'):
    resource_text_trimmed = resource_text[:2000] if resource_text else "No content"
    lang_instruction = LANG_INSTRUCTIONS.get(language, LANG_INSTRUCTIONS['uz'])

    prompt = f"""You are an educational resource evaluator. {lang_instruction}

Topic Name: {topic_name}
Topic Description: {topic_description}

Resource Title: {resource_title}
Resource Content: {resource_text_trimmed}

Evaluate the relevance of this resource to the topic above.

Return ONLY a valid JSON object with no extra text, no markdown, no explanation outside the JSON:
{{
    "score": 0.85,
    "label": "High",
    "reason": "Brief explanation in {language} why this resource is relevant or not",
    "key_matches": ["keyword1", "keyword2"],
    "missing": ["missing_topic1", "missing_topic2"]
}}

Rules:
- score must be a float between 0.0 and 1.0
- label must be exactly one of: "High", "Medium", "Low"
  - High: score >= 0.70
  - Medium: score >= 0.40
  - Low: score < 0.40
- reason, key_matches, missing must ALL be written in {lang_instruction}
- key_matches: list of keywords from the resource that match the topic (max 5)
- missing: list of topic aspects not covered in the resource (max 3)
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

    raise Exception(f"All models failed: {last_error}")


def _call_openrouter(model, prompt):
    api_key = settings.OPENROUTER_API_KEY
    if not api_key:
        raise Exception("OPENROUTER_API_KEY not configured")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://edurelevance.app",
        "X-Title": "EduRelevance"
    }

    payload = {
        "model": model,
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f"API error {response.status_code}: {response.text}")

    data = response.json()
    content = data['choices'][0]['message']['content'].strip()

    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:]
    content = content.strip()

    result = json.loads(content)

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

    label_map = {'High': 'high', 'Medium': 'medium', 'Low': 'low'}
    label = label_map.get(label, 'low')

    return {
        'score': score,
        'label': label,
        'reason': result.get('reason', ''),
        'key_matches': result.get('key_matches', []),
        'missing': result.get('missing', []),
    }