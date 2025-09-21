from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from database import get_user, add_user, delete_user
import logging
import os
import requests # To make API calls to Gemini

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- Gemini AI Configuration ---
GEMINI_API_KEY = "AIzaSyDAo1z9IA0k3dC8WqWXDasDGfGZ5PQFJco" # Handled by the execution environment, leave as is.
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
GEMINI_SYSTEM_PROMPT = """You are Aarogya Sarthi, a helpful AI health assistant. Your role is to understand a user's health symptoms and ask 2-3 clarifying questions to better understand the situation. Based on the conversation, provide potential next steps or things to look out for. IMPORTANT: You are not a doctor. Do not provide a diagnosis. Always end your response by strongly advising the user to consult a real medical professional for an accurate diagnosis and treatment."""


# --- Language Translations ---
MESSAGES = {
    'language_select': (
        "Please select your language:\n"
        "Reply with a number:\n"
        "1. English\n"
        "2. हिन्दी (Hindi)\n"
        "3. ଓଡ଼ିଆ (Odia)\n"
        "4. କୁଇ (Kui)\n"
        "5. ᱥᱟᱱᱛᱟᱲᱤ (Santali)"
    ),
    'en': {
        'welcome': "Welcome to Aarogya Sarthi! To get started, what is your full name?",
        'ask_age': "Great. What is your age?",
        'ask_gender': "Thanks. What is your gender?",
        'ask_state': "Which state do you live in?",
        'ask_district': "And which district?",
        'registered': "You are now registered! Thank you. We will now show you the main menu.",
        'welcome_back': "Welcome back, {name}! How can I help you today?\n\nReply with a number:\n1. Symptom Checker\n2. Vaccination Reminders\n3. Preventive Healthcare Tips\n4. Outbreak Alerts\n5. Exit",
        'main_menu': "How can I help you today?\n\nReply with a number:\n1. Symptom Checker\n2. Vaccination Reminders\n3. Preventive Healthcare Tips\n4. Outbreak Alerts\n5. Exit",
        'symptom_checker_start': "You've selected the Symptom Checker. Please describe your symptoms. To exit the checker at any time, just say 'exit'.",
        'exit_message': "Thank you for using Aarogya Sarthi. Have a healthy day!"
    },
    'hi': {
        'welcome': "आरोग्य सारथी में आपका स्वागत है! शुरू करने के लिए, आपका पूरा नाम क्या है?",
        'ask_age': "बढ़िया। आपकी उम्र क्या है?",
        'ask_gender': "धन्यवाद। आपका लिंग क्या है?",
        'ask_state': "आप किस राज्य में रहते हैं?",
        'ask_district': "और कौन सा जिला?",
        'registered': "अब आप पंजीकृत हो गए हैं! धन्यवाद। अब हम आपको मुख्य मेनू दिखाएंगे।",
        'welcome_back': "वापस स्वागत है, {name}! मैं आज आपकी कैसे मदद कर सकता हूँ?\n\nएक नंबर के साथ उत्तर दें:\n1. लक्षण परीक्षक\n2. टीकाकरण अनुस्मारक\n3. निवारक स्वास्थ्य युक्तियाँ\n4. प्रकोप अलर्ट\n5. बाहर निकलें",
        'main_menu': "मैं आज आपकी कैसे मदद कर सकता हूँ?\n\nएक नंबर के साथ उत्तर दें:\n1. लक्षण परीक्षक\n2. टीकाकरण अनुस्मारक\n3. निवारक स्वास्थ्य युक्तियाँ\n4. प्रकोप अलर्ट\n5. बाहर निकलें",
        'symptom_checker_start': "आपने लक्षण परीक्षक चुना है। कृपया अपने लक्षणों का वर्णन करें। चेकर से किसी भी समय बाहर निकलने के लिए, बस 'exit' कहें।",
        'exit_message': "आरोग्य सारथी का उपयोग करने के लिए धन्यवाद। आपका दिन स्वस्थ रहे!"
    },
    # Add other language translations here...
    'od': {}, 'kui': {}, 'sa': {}
}


# Temporary memory to track conversations
user_states = {}

def get_gemini_response(chat_history):
    """Sends a chat history to Gemini and gets the response."""
    payload = {
        "contents": chat_history,
        "systemInstruction": {
            "parts": [{"text": GEMINI_SYSTEM_PROMPT}]
        }
    }
    try:
        response = requests.post(GEMINI_API_URL, json=payload)
        response.raise_for_status() # Raises an exception for bad status codes
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        logging.error(f"Gemini API request failed: {e}")
        return "Sorry, I'm having trouble connecting to my AI brain right now. Please try again later."
    except (KeyError, IndexError) as e:
        logging.error(f"Error parsing Gemini response: {e} - Response: {response.text}")
        return "Sorry, I received an unusual response from the AI. Please try again."


@app.route("/")
def index():
    return "<h1>Aarogya Sarthi Backend is Running!</h1>"

@app.route("/message", methods=['POST'])
def reply():
    try:
        from_number = request.values.get('From', '')
        incoming_msg = request.values.get('Body', '').strip()
        resp = MessagingResponse()
        
        user = get_user(from_number)
        state_info = user_states.get(from_number, {})
        current_state = state_info.get('state')
        lang = state_info.get('lang', 'en') if not user else (user[8] if user and len(user) > 8 and user[8] else 'en')

        # --- Symptom Checker Logic ---
        if current_state == 'awaiting_symptoms':
            if incoming_msg.lower() == 'exit':
                del user_states[from_number]
                resp.message(MESSAGES[lang]['main_menu'])
            else:
                # Continue the conversation with Gemini
                chat_history = state_info.get('symptom_chat_history', [])
                chat_history.append({"role": "user", "parts": [{"text": incoming_msg}]})
                
                ai_response = get_gemini_response(chat_history)
                
                chat_history.append({"role": "model", "parts": [{"text": ai_response}]})
                state_info['symptom_chat_history'] = chat_history
                resp.message(ai_response)
        
        # --- Main Logic (Registration & Menu) ---
        elif user:
            # Existing user logic
            if current_state == 'awaiting_menu_choice':
                if incoming_msg == '1':
                    # Start Symptom Checker
                    resp.message(MESSAGES[lang]['symptom_checker_start'])
                    user_states[from_number] = {
                        'state': 'awaiting_symptoms', 
                        'lang': lang, 
                        'symptom_chat_history': []
                    }
                elif incoming_msg == '2': resp.message("Vaccination Reminders feature is coming soon!")
                elif incoming_msg == '3': resp.message("Preventive Healthcare Tips feature is coming soon!")
                elif incoming_msg == '4': resp.message("Outbreak Alerts feature is coming soon!")
                elif incoming_msg == '5':
                     del user_states[from_number]
                     resp.message(MESSAGES[lang]['exit_message'])
                else: 
                    resp.message("Invalid option. Please reply with a number from 1 to 5.")
            else:
                resp.message(MESSAGES[lang]['welcome_back'].format(name=user[1]))
                user_states[from_number] = {'state': 'awaiting_menu_choice', 'lang': lang}
        else:
            # New user registration logic
            if current_state is None and incoming_msg.lower() == 'hi':
                resp.message(MESSAGES['language_select'])
                user_states[from_number] = {'state': 'awaiting_language'}
            
            elif current_state == 'awaiting_language':
                # ... (language selection logic remains the same) ...
                if incoming_msg == '1': lang = 'en'
                elif incoming_msg == '2': lang = 'hi'
                elif incoming_msg == '3': lang = 'od'
                elif incoming_msg == '4': lang = 'kui'
                elif incoming_msg == '5': lang = 'sa'
                else:
                    resp.message("Invalid selection. " + MESSAGES['language_select'])
                    return str(resp)
                user_states[from_number] = {'state': 'awaiting_name', 'lang': lang}
                resp.message(MESSAGES[lang]['welcome'])

            elif current_state == 'awaiting_name':
                state_info['name'] = incoming_msg
                resp.message(MESSAGES[lang]['ask_age'])
                state_info['state'] = 'awaiting_age'
            
            elif current_state == 'awaiting_age':
                state_info['age'] = incoming_msg
                resp.message(MESSAGES[lang]['ask_gender'])
                state_info['state'] = 'awaiting_gender'
            
            elif current_state == 'awaiting_gender':
                state_info['gender'] = incoming_msg
                resp.message(MESSAGES[lang]['ask_state'])
                state_info['state'] = 'awaiting_state'

            elif current_state == 'awaiting_state':
                state_info['state_name'] = incoming_msg
                resp.message(MESSAGES[lang]['ask_district'])
                state_info['state'] = 'awaiting_district'

            elif current_state == 'awaiting_district':
                state_info['district'] = incoming_msg
                try:
                    add_user(
                        mobile=from_number, name=state_info['name'],
                        age=int(state_info['age']), gender=state_info['gender'],
                        state=state_info['state_name'], district=state_info['district'], 
                        language=lang
                    )
                    resp.message(MESSAGES[lang]['registered'])
                    # Transition to main menu after registration
                    resp.message(MESSAGES[lang]['main_menu'])
                    user_states[from_number] = {'state': 'awaiting_menu_choice', 'lang': lang}
                except Exception as e:
                    resp.message(f"Sorry, there was a database error: {e}")
                    if from_number in user_states:
                        del user_states[from_number]
            else:
                resp.message("Welcome! Please say 'hi' to start.")
                
        return str(resp)

    except Exception as e:
        logging.error(f"FATAL ERROR for number {request.values.get('From', '')}: {e}", exc_info=True)
        debug_resp = MessagingResponse()
        debug_resp.message(f"An unexpected error occurred in the backend. Please show this to the developer: {e}")
        return str(debug_resp)


@app.route("/delete_me")
def delete_my_data():
    my_number = "whatsapp:+918917226958" # Replace with your number in E.164 format
    try:
        delete_user(my_number)
        if my_number in user_states:
            del user_states[my_number]
        return f"User data for {my_number} has been deleted."
    except Exception as e:
        return f"Error deleting user: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

