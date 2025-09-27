import logging
import requests
import xml.etree.ElementTree as ET
from gemini_services import get_gemini_response
from database import has_user_seen_alert, mark_alert_as_seen

# --- BUG FIX: Use the new, correct URL for the WHO RSS feed ---
WHO_RSS_URL = "https://www.who.int/rss-feeds/emergencies-disease-outbreak-news-english.xml"

def fetch_live_alerts():
    """Fetches and parses the WHO RSS feed to find alerts relevant to India."""
    try:
        response = requests.get(WHO_RSS_URL, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        alerts = []
        for item in root.findall('.//channel/item'):
            title = item.find('title').text
            description = item.find('description').text
            alert_id = item.find('guid').text 
            
            if 'india' in title.lower() or 'india' in description.lower():
                alerts.append({'id': alert_id, 'title': title, 'summary': description})
        return alerts
    except Exception as e:
        logging.error(f"Failed to fetch or parse WHO RSS feed: {e}")
        return []

def get_outbreak_alert(user, lang):
    """Checks for new alerts the user hasn't seen and returns a translated message."""
    try:
        user_id = user[0]
        live_alerts = fetch_live_alerts()
        if not live_alerts:
            return None

        new_alert = None
        for alert in live_alerts:
            if not has_user_seen_alert(user_id, alert['id']):
                new_alert = alert
                break 
        if not new_alert:
            return None

        alert_title_en = new_alert['title']
        alert_summary_en = new_alert['summary']
        
        translated_title = alert_title_en
        translated_summary = alert_summary_en

        if lang != 'en':
            translation_prompt = (
                f"Translate the following health alert title and summary into the language with code '{lang}'. "
                f"Respond ONLY with the translation, formatted exactly like this:\n"
                f"Title: [translated title]\n"
                f"Summary: [translated summary]\n\n"
                f"---START---\n"
                f"Title: {alert_title_en}\n"
                f"Summary: {alert_summary_en}\n"
                f"---END---"
            )
            translation_system_prompt = "You are an expert translator specializing in public health announcements."
            chat_history = [{"role": "user", "parts": [{"text": translation_prompt}]}]
            translated_text = get_gemini_response(chat_history, translation_system_prompt)
            try:
                lines = translated_text.strip().split('\n')
                translated_title = lines[0].replace('Title: ', '').strip()
                translated_summary = lines[1].replace('Summary: ', '').strip()
            except IndexError:
                logging.error(f"Could not parse Gemini translation: {translated_text}")
        
        mark_alert_as_seen(user_id, new_alert['id'])
        
        intro = "⚠️ Health Alert:"
        if lang == 'hi': intro = "⚠️ स्वास्थ्य चेतावनी:"
        elif lang == 'od': intro = "⚠️ ସ୍ୱାସ୍ଥ୍ୟ ସତର୍କତା:"
        # Add intros for kui and sa
        
        return f"*{intro}*\n\n*{translated_title}*\n{translated_summary}"

    except Exception as e:
        logging.error(f"Could not check for outbreak alerts for user {user[0]}: {e}")
        return None

