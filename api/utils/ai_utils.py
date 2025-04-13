import os
import json
import logging
import google.generativeai as genai
import re

# Configure logging
logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_differences(old_text, new_text):
    """Analyze differences between two versions of text using Gemini."""
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
}}

IMPORTANT: Your response must be valid JSON. Do not include any text before or after the JSON object."""

    # Initialize the model
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    
    # Generate the response
    response = model.generate_content(prompt)
    response_text = response.text
    logger.debug(f"Raw AI response: {response_text}")
    
    # Try to extract JSON from the response if it's not pure JSON
    try:
        # First attempt: try to parse the entire response as JSON
        return json.loads(response_text)
    except json.JSONDecodeError:
        logger.warning("Failed to parse response as JSON, attempting to extract JSON")
        try:
            # Second attempt: try to extract JSON using regex
            json_match = re.search(r'(\{[\s\S]*\})', response_text)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(json_str)
            else:
                logger.error("Could not extract JSON from response")
                # Fallback if the response is not valid JSON
                return {
                    "content_changes": ["Error parsing AI response"],
                    "meaning_changes": [],
                    "additions": [],
                    "removals": [],
                    "tone_changes": []
                }
        except Exception as e:
            logger.error(f"Error processing AI response: {str(e)}")
            # Fallback if the response is not valid JSON
            return {
                "content_changes": ["Error parsing AI response"],
                "meaning_changes": [],
                "additions": [],
                "removals": [],
                "tone_changes": []
            } 