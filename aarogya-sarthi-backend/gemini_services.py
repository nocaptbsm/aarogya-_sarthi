import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

# --- Gemini AI Configuration ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY not found in .env file. AI features will fail.")
    
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"

def get_gemini_response(chat_history, system_prompt):
    """
    Sends a chat history and a specific system prompt to Gemini and gets the response.
    """
    if not GEMINI_API_KEY:
         return "AI functionality is disabled. Missing API Key."

    payload = {
        "contents": chat_history,
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        }
    }
    try:
        response = requests.post(GEMINI_API_URL, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        
        # Check for safety ratings and blocked content
        if 'promptFeedback' in result and result['promptFeedback']['blockReason']:
            logging.error(f"Gemini prompt blocked. Reason: {result['promptFeedback']['blockReason']}")
            return "I'm sorry, I can't respond to that topic. Let's talk about something else."

        return result['candidates'][0]['content']['parts'][0]['text']

    except requests.exceptions.RequestException as e:
        logging.error(f"Gemini API request failed: {e}")
        return "Sorry, I'm having trouble connecting to my AI brain right now. Please try again later."
    except (KeyError, IndexError) as e:
        logging.error(f"Error parsing Gemini response: {e} - Response: {response.text}")
        return "Sorry, I received an unusual response from the AI. Please try again."

