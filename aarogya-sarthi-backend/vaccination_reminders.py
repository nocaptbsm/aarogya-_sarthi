import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Google Maps API Configuration ---
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
GOOGLE_PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


# --- Vaccine Data Structure ---
VACCINE_SCHEDULE = {
    'infant': {
        'title_en': "Recommended Vaccines for Infants (0-12 months)",
        'title_hi': "शिशुओं (0-12 महीने) के लिए अनुशंसित टीके",
        'title_od': "ଶିଶୁମାନଙ୍କ ପାଇଁ ସୁପାରିଶ କରାଯାଇଥିବା ଟିକା (୦-୧୨ ମାସ)",
        'title_kui': "କୁନି ପିଲାଙ୍କ ପାଇଁ ଟିକା (୦-୧୨ ମାସ)",
        'title_sa': "ᱦᱩᱰᱤᱧ ᱜᱤᱫᱽᱨᱟᱹ ᱞᱟᱹᱜᱤᱫ ଟᱤᱠᱟᱹ (᱐-᱑᱒ ᱪᱟᱸᱫᱚ)",
        'vaccines': ["BCG (Tuberculosis)", "Hepatitis B", "Oral Polio Vaccine (OPV)", "Pentavalent", "Rotavirus", "PCV", "Measles & Rubella (MR)"]
    },
    'child': {
        'title_en': "Recommended Vaccines for Children (1-10 years)",
        'title_hi': "बच्चों (1-10 वर्ष) के लिए अनुशंसित टीके",
        'title_od': "ପିଲାମାନଙ୍କ ପାଇଁ ସୁପାରିଶ କରାଯାଇଥିବା ଟିକା (୧-୧୦ ବର୍ଷ)",
        'title_kui': "ପିଲାଙ୍କ ପାଇଁ ଟିକା (୧-୧୦ ବର୍ଷ)",
        'title_sa': "ᱜᱤᱫᱽᱨᱟᱹ ᱞᱟᱹᱜᱤᱫ ଟᱤᱠᱟᱹ (᱑-᱑᱐ ᱥᱮᱨᱢᱟ)",
        'vaccines': ["DTP Booster", "OPV Booster", "MR 2nd dose", "Typhoid Conjugate Vaccine", "Hepatitis A", "Tdap/Td vaccine"]
    },
    'adult': {
        'title_en': "Recommended Vaccines for Adults (18+)",
        'title_hi': "वयस्कों (18+) के लिए अनुशंसित टीके",
        'title_od': "ବୟସ୍କମାନଙ୍କ ପାଇଁ ସୁପାରିଶ କରାଯାଇଥିବା ଟିକା (୧୮+)",
        'title_kui': "ବଡ଼ ଲୋକଙ୍କ ପାଇଁ ଟିକା (୧୮+)",
        'title_sa': "ᱦᱟᱲᱟᱢ ᱦᱚᱲ ᱞᱟᱹᱜᱤᱫ ଟᱤᱠᱟᱹ (᱑᱘+)",
        'vaccines': ["Tdap/Td (every 10 years)", "Influenza (yearly)", "HPV", "Pneumococcal (for adults 65+)", "Hepatitis B"]
    }
}

def get_vaccine_list(user, lang, MESSAGES):
    """
    Determines the correct vaccine schedule based on user's age and returns a formatted list.
    """
    try:
        user_age = int(user[3])  # Assuming age is at index 3 of the user tuple
        age_group = 'adult'
        if user_age <= 1: age_group = 'infant'
        elif user_age <= 10: age_group = 'child'
        
        vaccine_info = VACCINE_SCHEDULE[age_group]
        
        title = vaccine_info.get(f'title_{lang}', vaccine_info['title_en'])
        vaccine_intro = MESSAGES[lang].get('vaccine_info', "Reply with a number to find a nearby clinic for that vaccine:")

        response_text = f"{vaccine_intro}\n\n*{title}*\n"
        for i, vaccine in enumerate(vaccine_info['vaccines'], 1):
            response_text += f"{i}. {vaccine}\n"
        
        response_text += f"\n{MESSAGES[lang].get('return_to_menu', 'Reply menu to return to the main menu.')}"
        return response_text, vaccine_info['vaccines']

    except (ValueError, IndexError) as e:
        logging.error(f"Could not determine user age for vaccine reminders: {e}")
        return MESSAGES[lang].get('age_error', "Sorry, I couldn't retrieve your age from the database to suggest vaccines."), None


def find_nearby_centers(vaccine_name, user_district, lang, MESSAGES):
    """
    Uses Google Places API to find nearby vaccination centers.
    """
    if not GOOGLE_MAPS_API_KEY:
        logging.error("GOOGLE_MAPS_API_KEY is not set. Please add it to the .env file.")
        return MESSAGES[lang].get('api_key_error', "Sorry, the clinic finder service is not configured correctly.")

    query = f"hospitals or clinics with {vaccine_name} vaccine in {user_district}"
    params = {'query': query, 'key': GOOGLE_MAPS_API_KEY}
    
    try:
        response = requests.get(GOOGLE_PLACES_API_URL, params=params)
        response.raise_for_status()
        results = response.json().get('results', [])

        if not results:
            return MESSAGES[lang].get('no_clinics_found', "Sorry, I couldn't find any centers with that vaccine near you. Please check with local health authorities.")

        response_text = MESSAGES[lang].get('clinics_found_intro', "Here are some centers near you:") + "\n\n"
        for i, place in enumerate(results[:3], 1):
            name = place.get('name')
            address = place.get('formatted_address')
            maps_url = f"https://www.google.com/maps/search/?api=1&query={requests.utils.quote(address)}"
            response_text += f"{i}. *{name}*\n{MESSAGES[lang].get('address_label', 'Address')}: {address}\nGoogle Maps: {maps_url}\n\n"
        
        response_text += MESSAGES[lang].get('call_ahead_note', "Please call ahead to confirm vaccine availability.")
        return response_text

    except requests.exceptions.RequestException as e:
        logging.error(f"Google Maps API request failed: {e}")
        return MESSAGES[lang].get('api_request_error', "Sorry, I'm having trouble searching for clinics right now.")


# --- NEW: The Main Handler Function ---
def handle_vaccination_reminders(user, state_info, incoming_msg, lang, MESSAGES):
    """
    The main controller for the vaccination reminders feature.
    """
    # Check if this is the start of the conversation for this feature
    if incoming_msg == "start":
        response_text, vaccines = get_vaccine_list(user, lang, MESSAGES)
        if vaccines:
            # Store the list of vaccines in the user's state so we know what they can choose from
            state_info['available_vaccines'] = vaccines
        return response_text

    # If we are expecting a vaccine choice from the user
    else:
        try:
            choice = int(incoming_msg)
            vaccines = state_info.get('available_vaccines', [])
            
            if 1 <= choice <= len(vaccines):
                selected_vaccine = vaccines[choice - 1]
                user_district = user[6] # Assuming district is at index 6
                
                # Find clinics and clear the state
                response_text = find_nearby_centers(selected_vaccine, user_district, lang, MESSAGES)
                del state_info['state'] # Exit the vaccine flow
                return response_text
            else:
                return MESSAGES[lang].get('invalid_choice', "Invalid choice. Please pick a number from the list.")
        except (ValueError, TypeError):
             return MESSAGES[lang].get('invalid_input', "Please reply with a number from the list.")