import logging
from gemini_services import get_gemini_response
from database import get_chat_history, save_chat_history

# This is the "persona" for the AI. It sets the rules for the conversation.
GEMINI_SYSTEM_PROMPT = """You are Aarogya Sarthi, a helpful AI health assistant. Your role is to understand a user's health symptoms in their chosen language (English, Hindi, Odia, Kui, or Santali) and ask 2-3 clarifying questions to better understand the situation. Respond ONLY in the language of the user's last message. Based on the conversation, provide potential next steps or things to look out for. IMPORTANT: You are not a doctor. Do not provide a diagnosis. Always end your response by strongly advising the user to consult a real medical professional for an accurate diagnosis and treatment."""

def handle_symptom_checker(user, state_info, incoming_msg, lang, MESSAGES):
    """
    Manages the state and conversation flow for the symptom checker feature using the database.
    """
    user_id = user[0] # The user's primary key ID is at index 0

    # If the user wants to exit, simply return them to the main menu message.
    if incoming_msg.lower() == 'exit':
        return MESSAGES[lang]['main_menu']

    # Retrieve the user's chat history from the database
    chat_history = get_chat_history(user_id)
    
    # Add the user's new message to the history
    chat_history.append({"role": "user", "parts": [{"text": incoming_msg}]})
    
    # Get the AI's response
    ai_response = get_gemini_response(chat_history, GEMINI_SYSTEM_PROMPT)
    
    # Add the AI's response to the history
    chat_history.append({"role": "model", "parts": [{"text": ai_response}]})
    
    # Save the updated history back to the database
    save_chat_history(user_id, chat_history)
    
    return ai_response