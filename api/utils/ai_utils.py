import os
import json
import openai

# Set the API key directly
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_differences(old_text, new_text):
    """Analyze differences between two versions of text using OpenAI."""
    prompt = f"""Compare these two versions of a pitch deck and identify the key differences in both content and meaning:

Old Version:
{old_text}

New Version:
{new_text}

Please provide a detailed analysis of:
1. Major content changes
2. Meaningful differences in messaging
3. Key additions or removals
4. Changes in tone or emphasis

Format the response as a JSON with the following structure:
{{
    "content_changes": ["list of specific content changes"],
    "meaning_changes": ["list of changes in meaning or messaging"],
    "additions": ["list of new content"],
    "removals": ["list of removed content"],
    "tone_changes": ["list of changes in tone or emphasis"]
}}"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a pitch deck analysis expert. Analyze the differences between two versions of a pitch deck."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response content as JSON
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        # Fallback if the response is not valid JSON
        return {
            "content_changes": ["Error parsing AI response"],
            "meaning_changes": [],
            "additions": [],
            "removals": [],
            "tone_changes": []
        } 