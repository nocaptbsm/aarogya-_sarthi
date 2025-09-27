from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import logging
import os
from dotenv import load_dotenv

from database import get_user, add_user, delete_user
from location_data import STATES_AND_DISTRICTS
from symptom_checker import handle_symptom_checker
from vaccination_reminders import handle_vaccination_reminders
from outbreak_alerts import get_outbreak_alert
from preventive_healthcare_tips import get_preventive_tips

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


# --- Language & Message Data (remains the same) ---
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
        'ask_age': "Great. What is your age? Please enter a number (e.g., 25).",
        'invalid_age': "Sorry, that doesn't look like a valid age. Please enter a number between 1 and 120.",
        'ask_gender': "Thanks. What is your gender?\n\nReply with a number:\n1. Male\n2. Female\n3. Other",
        'invalid_gender': "Invalid selection. Please reply with 1, 2, or 3.",
        'ask_state': "Which state do you live in? Please reply with the number for your state.",
        'invalid_state': "Invalid selection. Please choose a number from the list.",
        'ask_district': "And which district? Please reply with the number for your district.",
        'invalid_district': "Invalid selection. Please choose a number from the list for your state.",
        'registered': "You are now registered! Thank you.",
        'welcome_back': "Welcome back to Aarogya Sarthi, {name}! How can I help you today?",
        'main_menu': ("Reply with a number:\n"
                      "1. Symptom Checker\n"
                      "2. Vaccination Reminders\n"
                      "3. Preventive Healthcare Tips\n"
                      "4. Outbreak Alerts (Manual Check)\n"
                      "5. Exit"),
        'symptom_checker_start': "You've selected the Symptom Checker. Please describe your symptoms. To exit at any time, just say 'exit'.",
        'exit_message': "Thank you for using Aarogya Sarthi. Have a healthy day!",
        'outbreak_alert_intro': "⚠️ Health Alert for your area:",
        'preventive_tips_intro': "🌿 Health Tip for your area:"
    },
     # ... (other languages remain the same) ...
    'hi': {
        'welcome': "आरोग्य सारथी में आपका स्वागत है! शुरू करने के लिए, आपका पूरा नाम क्या है?",
        'ask_age': "बढ़िया। आपकी उम्र क्या है? कृपया एक संख्या दर्ज करें (जैसे, 25)।",
        'invalid_age': "क्षमा करें, यह एक वैध उम्र नहीं लगती है। कृपया 1 और 120 के बीच एक संख्या दर्ज करें।",
        'ask_gender': "धन्यवाद। आपका लिंग क्या है?\n\nएक नंबर के साथ उत्तर दें:\n1. पुरुष\n2. महिला\n3. अन्य",
        'invalid_gender': "अमान्य चयन। कृपया 1, 2, या 3 के साथ उत्तर दें।",
        'ask_state': "आप किस राज्य में रहते हैं? कृपया अपने राज्य के लिए नंबर के साथ उत्तर दें।",
        'invalid_state': "अमान्य चयन। कृपया सूची से एक संख्या चुनें।",
        'ask_district': "और कौन सा जिला? कृपया अपने जिले के लिए नंबर के साथ उत्तर दें।",
        'invalid_district': "अमान्य चयन। कृपया अपने राज्य के लिए सूची से एक संख्या चुनें।",
        'registered': "अब आप पंजीकृत हो गए हैं! धन्यवाद।",
        'welcome_back': "आरोग्य सारथी में आपका वापस स्वागत है, {name}! मैं आज आपकी कैसे मदद कर सकता हूँ?",
        'main_menu': ("एक नंबर के साथ उत्तर दें:\n"
                      "1. लक्षण परीक्षक\n"
                      "2. टीकाकरण अनुस्मारक\n"
                      "3. निवारक स्वास्थ्य युक्तियाँ\n"
                      "4. प्रकोप अलर्ट (मैनुअल जांच)\n"
                      "5. बाहर निकलें"),
        'symptom_checker_start': "आपने लक्षण परीक्षक चुना है। कृपया अपने लक्षणों का वर्णन करें। किसी भी समय बाहर निकलने के लिए, बस 'exit' कहें।",
        'exit_message': "आरोग्य सारथी का उपयोग करने के लिए धन्यवाद। आपका दिन स्वस्थ रहे!",
        'outbreak_alert_intro': "⚠️ आपके क्षेत्र के लिए स्वास्थ्य चेतावनी:",
        'preventive_tips_intro': "🌿 आपके क्षेत्र के लिए स्वास्थ्य सुझाव:"
    },
    'od': {
        'welcome': "ଆରୋଗ୍ୟ ସାରଥିକୁ ସ୍ୱାଗତ! ଆରମ୍ଭ କରିବା ପାଇଁ, ଆପଣଙ୍କର ପୂରା ନାମ କ’ଣ?",
        'ask_age': "ବହୁତ ଭଲ। ଆପଣଙ୍କ ବୟସ କେତେ? ଦୟାକରି ଏକ ସଂଖ୍ୟା ଦିଅନ୍ତୁ (ଯେପରିକି, 25)।",
        'invalid_age': "କ୍ଷମା କରନ୍ତୁ, ଏହା ଏକ ବୈଧ ବୟସ ନୁହେଁ। ଦୟାକରି 1 ରୁ 120 ମଧ୍ୟରେ ଏକ ସଂଖ୍ୟା ଦିଅନ୍ତୁ।",
        'ask_gender': "ଧନ୍ୟବାଦ। ଆପଣଙ୍କ ଲିଙ୍ଗ କ’ଣ?\n\nଏକ ନମ୍ବର ସହିତ ଉତ୍ତର ଦିଅନ୍ତୁ:\n1. ପୁରୁଷ\n2. ମହିଳା\n3. ଅନ୍ୟ",
        'invalid_gender': "ଅବୈଧ ଚୟନ। ଦୟାକରି 1, 2, କିମ୍ବା 3 ସହିତ ଉତ୍ତର ଦିଅନ୍ତୁ।",
        'ask_state': "ଆପଣ କେଉଁ ରାଜ୍ୟରେ ରୁହନ୍ତି? ଦୟାକରି ଆପଣଙ୍କ ରାଜ୍ୟ ପାଇଁ ନମ୍ବର ସହିତ ଉତ୍ତର ଦିଅନ୍ତୁ।",
        'invalid_state': "ଅବୈଧ ଚୟନ। ଦୟାକରି ତାଲିକାରୁ ଏକ ସଂଖ୍ୟା ବାଛନ୍ତୁ।",
        'ask_district': "ଏବଂ କେଉଁ ଜିଲ୍ଲା? ଦୟାକରି ଆପଣଙ୍କ ଜିଲ୍ଲା ପାଇଁ ନମ୍ବର ସହିତ ଉତ୍ତର ଦିଅନ୍ତୁ।",
        'invalid_district': "ଅବୈଧ ଚୟନ। ଦୟାକରି ଆପଣଙ୍କ ରାଜ୍ୟ ପାଇଁ ତାଲିକାରୁ ଏକ ସଂଖ୍ୟା ବାଛନ୍ତୁ।",
        'registered': "ଆପଣ ବର୍ତ୍ତମାନ ପଞ୍ଜିକୃତ ହୋଇଛନ୍ତି! ଧନ୍ୟବାଦ।",
        'welcome_back': "ଆରୋଗ୍ୟ ସାରଥିକୁ ପୁନର୍ବାର ସ୍ୱାଗତ, {name}! ଆଜି ମୁଁ ଆପଣଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରେ?",
        'main_menu': ("ଏକ ନମ୍ବର ସହିତ ଉତ୍ତର ଦିଅନ୍ତୁ:\n"
                      "1. ଲକ୍ଷଣ ଯାଞ୍ଚକାରୀ\n"
                      "2. ଟୀକାକରଣ ସ୍ମାରକ\n"
                      "3. ନିରାକରଣ ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ\n"
                      "4. ପ୍ରକୋପ ସତର୍କତା (ମାନୁଆଲ ଯାଞ୍ଚ)\n"
                      "5. ବାହାରିଯାଆନ୍ତୁ"),
        'symptom_checker_start': "ଆପଣ ଲକ୍ଷଣ ଯାଞ୍ଚକାରୀ ବାଛିଛନ୍ତି। ଦୟାକରି ଆପଣଙ୍କର ଲକ୍ଷଣ ବର୍ଣ୍ଣନା କରନ୍ତୁ। ଯେକୌଣସି ସମୟରେ ବାହାରିବାକୁ, କେବଳ 'exit' କୁହନ୍ତୁ।",
        'exit_message': "ଆରୋଗ୍ୟ ସାରଥି ବ୍ୟବହାର କରିଥିବାରୁ ଧନ୍ୟବାଦ। ଆପଣଙ୍କ ଦିନ ସୁସ୍ଥ ରହୁ!",
        'outbreak_alert_intro': "⚠️ ଆପଣଙ୍କ ଅଞ୍ଚଳ ପାଇଁ ସ୍ୱାସ୍ଥ୍ୟ ସତର୍କତା:",
        'preventive_tips_intro': "🌿 ଆପଣଙ୍କ ଅଞ୍ଚଳ ପାଇଁ ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ:"
    },
    'kui': {
        'welcome': "ଆରୋଗ୍ୟ ସାରଥିକେ ସ୍ୱାଗତ୍! ଆରମ୍ଭ କରବାକେ, ଆପଣାର୍ ନାମ୍ କାଣା?",
        'ask_age': "ଭଲ୍। ଆପଣାର୍ ବୟସ କେତେ? ଦୟାକରି ଗୁଟେ ସଂଖ୍ୟା ଦିଅନ୍ତୁ (ଯେନ୍ତା, 25)।",
        'invalid_age': "ମାଫ୍ କରବେ, ଇଟା ଗୁଟେ ଠିକ୍ ବୟସ ନୁହେଁ। ଦୟାକରି 1 ରୁ 120 ଭିତରେ ଗୁଟେ ସଂଖ୍ୟା ଦିଅନ୍ତୁ।",
        'ask_gender': "ଧନ୍ୟବାଦ। ଆପଣାର୍ ଲିଙ୍ଗ କାଣା?\n\nଗୁଟେ ନମ୍ବର ସାଙ୍ଗେ ଉତ୍ତର ଦିଅନ୍ତୁ:\n1. ପୁରୁଷ୍\n2. ମହିଳା\n3. ଅନ୍ୟ",
        'invalid_gender': "ଭୁଲ୍ ଚୟନ୍। ଦୟାକରି 1, 2, କିମ୍ବା 3 ସାଙ୍ଗେ ଉତ୍ତର ଦିଅନ୍ତୁ।",
        'ask_state': "ଆପଣ୍ କେନ୍ ରାଜ୍ୟରେ ରହୁଛନ୍? ଦୟାକରି ଆପଣାର୍ ରାଜ୍ୟର୍ ଲାଗି ନମ୍ବର ସାଙ୍ଗେ ଉତ୍ତର ଦିଅନ୍ତୁ।",
        'invalid_state': "ଭୁଲ୍ ଚୟନ୍। ଦୟାକରି ତାଲିକାରୁ ଗୁଟେ ସଂଖ୍ୟା ବାଛନ୍ତୁ।",
        'ask_district': "ଆର୍ କେନ୍ ଜିଲ୍ଲା? ଦୟାକରି ଆପଣାର୍ ଜିଲ୍ଲା ଲାଗି ନମ୍ବର ସାଙ୍ଗେ ଉତ୍ତର ଦିଅନ୍ତୁ।",
        'invalid_district': "ଭୁଲ୍ ଚୟନ୍। ଦୟାକରି ଆପଣାର୍ ରାଜ୍ୟ ଲାଗି ତାଲିକାରୁ ଗୁଟେ ସଂଖ୍ୟା ବାଛନ୍ତୁ।",
        'registered': "ଆପଣ୍ ଏବେ ପଞ୍ଜିକୃତ ହେଇଗଲେ! ଧନ୍ୟବାଦ।",
        'welcome_back': "ଆରୋଗ୍ୟ ସାରଥିକେ ଫେର୍ ସ୍ୱାଗତ୍, {name}! ଆଜି ମୁଇଁ ଆପଣାର୍ କେନ୍ତା ସାହାଯ୍ୟ କର୍ମି?",
        'main_menu': ("ଗୁଟେ ନମ୍ବର ସାଙ୍ଗେ ଉତ୍ତର ଦିଅନ୍ତୁ:\n"
                      "1. ଲକ୍ଷଣ ଯାଞ୍ଚ୍\n"
                      "2. ଟୀକା ସ୍ମାରକ\n"
                      "3. ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ\n"
                      "4. ପ୍ରକୋପ ସତର୍କତା\n"
                      "5. ବାହାର୍"),
        'symptom_checker_start': "ଆପଣ୍ ଲକ୍ଷଣ ଯାଞ୍ଚ୍ ବାଛିଛନ୍। ଦୟାକରି ଆପଣାର୍ ଲକ୍ଷଣ ବିଷୟରେ କହନ୍ତୁ। ଯେକେନ୍ ସମୟରେ ବାହାର୍ବାକେ, 'exit' କହନ୍ତୁ।",
        'exit_message': "ଆରୋଗ୍ୟ ସାରଥି ବ୍ୟବହାର୍ କର୍ଥିବାରୁ ଧନ୍ୟବାଦ। ଆପଣାର୍ ଦିନ୍ ସୁସ୍ଥ ରହୁ!",
        'outbreak_alert_intro': "⚠️ ଆପଣାର୍ ଅଞ୍ଚଲ୍ ଲାଗି ସ୍ୱାସ୍ଥ୍ୟ ସତର୍କତା:",
        'preventive_tips_intro': "🌿 ଆପଣାର୍ ଅଞ୍ଚଲ୍ ଲାଗି ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ:"
    },
    'sa': {
        'welcome': "ᱟᱨᱚᱜᱭᱚ ᱥᱟᱨᱛᱷᱤ ᱨᱮ ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ! ᱮᱛᱚᱦᱚᱵᱽ ᱞᱟᱹᱜᱤᱫ, ᱟᱢᱟᱜ ᱯᱩᱨᱟᱹ ᱧᱩᱛᱩᱢ ᱫᱚ ᱪᱮᱫ?",
        'ask_age': "ᱵᱮᱥ། ᱟᱢᱟᱜ ᱵᱚᱭᱚᱥ ᱛᱤᱱᱟᱹᱜ? ᱫᱟᱭᱟᱠᱟᱛᱮ ᱢᱤᱫᱴᱟᱹᱝ ᱱᱚᱢᱵᱚᱨ ᱮᱢᱚᱜ ᱢᱮ (ᱡᱮᱞᱠᱟ, 25)᱾",
        'invalid_age': "ᱤᱠᱟᱹ ᱠᱟᱹᱧ ᱢᱮ, ᱱᱚᱣᱟ ᱫᱚ ճիշᱴ ᱵᱚᱭᱚᱥ ᱵᱟᱝ ᱠᱟᱱᱟ᱾ ᱫᱟᱭᱟᱠᱟᱛᱮ 1 ᱟᱨ 120 ᱛᱟᱞᱟ ᱨᱮ ᱢᱤᱫᱴᱟᱹᱝ ᱱᱚᱢᱵᱚᱨ ᱮᱢᱚᱜ ᱢᱮ᱾",
        'ask_gender': "ᱥᱟᱨᱦᱟᱣ། ᱟᱢᱟᱜ ᱡᱟᱹᱛᱤ ᱫᱚ ᱪᱮᱫ?\n\nᱢᱤᱫᱴᱟᱹᱝ ᱱᱚᱢᱵᱚᱨ ᱛᱮ ᱛᱮᱞᱟ ᱮᱢᱚᱜ ᱢᱮ:\n1. ᱠᱚᱲᱟ\n2. ᱠᱩᱲᱤ\n3. ᱮᱴᱟᱜ",
        'invalid_gender': "ᱵᱷᱩᱞ ᱵᱟᱪᱷᱱᱟᱣ། ᱫᱟᱭᱟᱠᱟᱛᱮ 1, 2, ᱥᱮ 3 ᱛᱮ ᱛᱮᱞᱟ ᱮᱢᱚᱜ ᱢᱮ᱾",
        'ask_state': "ᱟᱢ ᱚᱠᱟ ରାଜ୍ୟ ᱨᱮᱢ ᱛᱟᱦᱮᱱᱟ? ᱫᱟᱭᱟᱠᱟᱛᱮ ᱟᱢᱟᱜ ରାଜ୍ୟ ᱞᱟᱹᱜᱤᱫ ᱱᱚᱢᱵᱚᱨ ᱛᱮ ᱛᱮᱞᱟ ᱮᱢᱚᱜ ᱢᱮ᱾",
        'invalid_state': "ᱵᱷᱩᱞ ᱵᱟᱪᱷᱱᱟᱣ། ᱫᱟᱭᱟᱠᱟᱛᱮ ᱞᱤᱥᱴ ᱠᱷᱚᱱ ᱢᱤᱫᱴᱟᱹᱝ ᱱᱚᱢᱵᱚᱨ ᱵᱟᱪᱷᱟᱣ ᱢᱮ᱾",
        'ask_district': "ᱟᱨ ᱚᱠᱟ ᱡᱤᱞᱞᱟ? ᱫᱟᱭᱟᱠᱟᱛᱮ ᱟᱢᱟᱜ ᱡᱤᱞᱞᱟ ᱞᱟᱹଗᱤᱫ ᱱᱚᱢᱵᱚᱨ ᱛᱮ ᱛᱮᱞା ᱮᱢᱚᱜ ᱢᱮ᱾",
        'invalid_district': "ᱵᱷᱩᱞ ᱵᱟᱪᱷᱱᱟᱣ། ᱫᱟᱭାᱠᱟᱛᱮ ᱟᱢᱟᱜ ରାଜ୍ୟ ᱞᱟᱹᱜᱤᱫ ᱞᱤᱥᱴ ᱠᱷᱚᱱ ᱢᱤᱫᱴᱟᱹᱝ ᱱᱚᱢᱵᱚᱨ ᱵᱟᱪᱷᱟᱣ ᱢᱮ᱾",
        'registered': "ᱟᱢ ᱱᱤᱛᱚᱜ ᱯଞ୍ଜᱤᱠୃᱛ ᱮᱱᱟᱢ! ᱥᱟᱨᱦᱟᱣ།",
        'welcome_back': "ᱟᱨᱚᱜᱭᱚ ᱥᱟᱨᱛᱷᱤ ᱨᱮ ᱟᱨᱦᱚᱸ ᱥᱟᱹᱜᱩᱱ ᱫᱟᱨᱟᱢ, {name}! ᱛᱮᱦᱮᱧ ᱤᱧ ᱟᱢᱟᱜ ᱪᱮᱫ ᱜᱚᱲᱚ ᱫᱟᱲᱮᱭᱟᱢᱟ?",
        'main_menu': ("ᱢᱤᱫᱴᱟᱹᱝ ᱱᱚᱢᱵᱚᱨ ᱛᱮ ᱛᱮᱞᱟ ᱮᱢᱚᱜ ᱢᱮ:\n"
                      "1. ախտանիշների ստուգում\n"
                      "2. պատվաստումների հիշեցումներ\n"
                      "3. կանխարգելիչ առողջապահական խորհուրդներ\n"
                      "4. համաճարակային ահազանգեր\n"
                      "5. Ելք"),
        'symptom_checker_start': "ᱟᱢ ախտանիշների ստուգում ᱮᱢ ᱵᱟᱪᱷᱟᱣ ᱠᱮᱫᱟ᱾ ᱫᱟᱭᱟᱠᱟᱛᱮ ᱟᱢᱟᱜ ախտանիշները նկարագրիր։ Ցանկացած պահի դուրս գալու համար պարզապես ասա 'exit'։",
        'exit_message': "ᱟᱨᱚਗᱭᱚ ᱥᱟᱨᱛᱷᱤ ᱵ୍ୟବହାର ᱞᱟᱹᱜᱤᱫ ᱥᱟᱨᱦᱟᱣ། ᱟᱢᱟᱜ ᱫᱤᱱ ᱱᱟᱯᱟᱭ ᱛᱟᱦᱮᱱ!",
        'outbreak_alert_intro': "⚠️ ᱟᱢᱟᱜ ᱮᱞᱟᱠᱟ ᱞᱟᱹᱜᱤᱫ ᱥᱣᱟᱥᱛᱷᱚ  cảnh báo:",
        'preventive_tips_intro': "🌿 ᱟᱢᱟᱜ ᱮᱞᱟକା ᱞᱟᱹᱜᱤᱫ ᱥᱣᱟᱥᱛᱷᱚ পরামর্শ:"
    }
}
user_states = {}

@app.route("/")
def index():
    return "<h1>Aarogya Sarthi Backend is Running!</h1>"

def list_paginated(items, page_num=1, page_size=10):
    start = (page_num - 1) * page_size
    end = start + page_size
    paginated_items = items[start:end]
    response_text = ""
    for i, item in enumerate(paginated_items, start + 1):
        response_text += f"{i}. {item}\n"
    if end < len(items):
        response_text += f"\nReply with 'more' to see the next page."
    return response_text

@app.route("/message", methods=['POST'])
def reply():
    try:
        from_number = request.values.get('From', '')
        incoming_msg = request.values.get('Body', '').strip().lower()
        resp = MessagingResponse()
        
        user = get_user(from_number)
        state_info = user_states.get(from_number, {})
        current_state = state_info.get('state')
        
        lang = state_info.get('lang', 'en')
        if user:
            lang = user[7] if len(user) > 7 and user[7] else 'en'

        if incoming_msg == 'menu':
            if from_number in user_states: del user_states[from_number]
            if user:
                resp.message(MESSAGES[lang]['welcome_back'].format(name=user[2]))
                resp.message(MESSAGES[lang]['main_menu'])
                user_states[from_number] = {'state': 'awaiting_menu_choice', 'lang': lang}
            return str(resp)

        if current_state == 'awaiting_symptoms':
            response_text = handle_symptom_checker(user, state_info, incoming_msg, lang, MESSAGES)
            resp.message(response_text)
            if "exit" in incoming_msg:
                 if from_number in user_states: del user_states[from_number]
                 user_states[from_number] = {'state': 'awaiting_menu_choice', 'lang': lang}
            return str(resp)
        
        elif current_state == 'awaiting_vaccine_choice':
            response_text = handle_vaccination_reminders(user, state_info, incoming_msg, lang, MESSAGES)
            resp.message(response_text)
            if user_states.get(from_number, {}).get('state') != 'awaiting_vaccine_choice':
                 resp.message(MESSAGES[lang]['main_menu'])
                 user_states[from_number] = {'state': 'awaiting_menu_choice', 'lang': lang}
            return str(resp)

        elif user:
            if not current_state:
                alert_message = get_outbreak_alert(user, lang)
                if alert_message:
                    resp.message(alert_message)
                tips_message = get_preventive_tips(user, lang, MESSAGES)
                if tips_message:
                    resp.message(tips_message)
            
            if current_state in [None, 'awaiting_menu_choice']:
                if incoming_msg in ['1','2','3','4','5']:
                    user_states[from_number] = {'lang': lang}
                    if incoming_msg == '1':
                        user_states[from_number]['state'] = 'awaiting_symptoms'
                        resp.message(MESSAGES[lang]['symptom_checker_start'])
                    elif incoming_msg == '2':
                        user_states[from_number]['state'] = 'awaiting_vaccine_choice'
                        response_text = handle_vaccination_reminders(user, user_states[from_number], "start", lang, MESSAGES)
                        resp.message(response_text)
                    elif incoming_msg == '3':
                        tips_message = get_preventive_tips(user, lang, MESSAGES)
                        resp.message(tips_message or "No specific tips available at the moment.")
                        resp.message(MESSAGES[lang]['main_menu'])
                        user_states[from_number]['state'] = 'awaiting_menu_choice'
                    elif incoming_msg == '4':
                        alert_message = get_outbreak_alert(user, lang)
                        resp.message(alert_message or "No active alerts for your country at this time.")
                        resp.message(MESSAGES[lang]['main_menu'])
                        user_states[from_number]['state'] = 'awaiting_menu_choice'
                    elif incoming_msg == '5':
                        if from_number in user_states: del user_states[from_number]
                        resp.message(MESSAGES[lang]['exit_message'])
                else:
                    resp.message(MESSAGES[lang]['welcome_back'].format(name=user[2]))
                    resp.message(MESSAGES[lang]['main_menu'])
                    user_states[from_number] = {'state': 'awaiting_menu_choice', 'lang': lang}
        else:
            if current_state is None and incoming_msg == 'hi':
                resp.message(MESSAGES['language_select'])
                user_states[from_number] = {'state': 'awaiting_language'}
            elif current_state == 'awaiting_language':
                if incoming_msg in ['1','2','3','4','5']:
                    lang_map = {'1':'en', '2':'hi', '3':'od', '4':'kui', '5':'sa'}
                    lang = lang_map[incoming_msg]
                    user_states[from_number] = {'state': 'awaiting_name', 'lang': lang}
                    resp.message(MESSAGES[lang]['welcome'])
                else: resp.message("Invalid selection. " + MESSAGES['language_select'])
            elif current_state == 'awaiting_name':
                state_info['name'] = request.values.get('Body', '').strip()
                resp.message(MESSAGES[lang]['ask_age'])
                state_info['state'] = 'awaiting_age'
            elif current_state == 'awaiting_age':
                try:
                    age = int(incoming_msg)
                    if 1 <= age <= 120:
                        state_info['age'] = age
                        resp.message(MESSAGES[lang]['ask_gender'])
                        state_info['state'] = 'awaiting_gender'
                    else: resp.message(MESSAGES[lang]['invalid_age'])
                except ValueError: resp.message(MESSAGES[lang]['invalid_age'])
            
            # --- MODIFIED REGISTRATION FLOW ---
            elif current_state == 'awaiting_gender':
                gender_map = {'1': 'Male', '2': 'Female', '3': 'Other'}
                if incoming_msg in gender_map:
                    state_info['gender'] = gender_map[incoming_msg]
                    
                    # Set state to Odisha by default
                    selected_state = "Odisha"
                    state_info['selected_state'] = selected_state
                    
                    # Ask for district directly
                    district_list_text = f"{MESSAGES[lang]['ask_district']}\n\n"
                    districts = STATES_AND_DISTRICTS[selected_state]
                    district_list = list_paginated(districts)
                    
                    resp.message(district_list_text + district_list)
                    state_info['state'] = 'awaiting_district'
                    state_info['district_page'] = 1
                else:
                    resp.message(MESSAGES[lang]['invalid_gender'])
            
            # This block is now skipped
            # elif current_state == 'awaiting_state': ...

            elif current_state == 'awaiting_district':
                selected_state = state_info.get('selected_state')
                districts = STATES_AND_DISTRICTS.get(selected_state, [])
                page = state_info.get('district_page', 1)
                if incoming_msg == 'more':
                    page += 1
                    district_list = list_paginated(districts, page_num=page)
                    resp.message(district_list); state_info['district_page'] = page
                else:
                    try:
                        choice = int(incoming_msg)
                        if 1 <= choice <= len(districts):
                            selected_district = districts[choice - 1]
                            add_user(mobile=from_number, name=state_info['name'], age=state_info['age'], gender=state_info['gender'], state=selected_state, district=selected_district, language=lang)
                            newly_registered_user = get_user(from_number)
                            resp.message(MESSAGES[lang]['registered'])
                            resp.message(MESSAGES[lang]['welcome_back'].format(name=newly_registered_user[2]))
                            resp.message(MESSAGES[lang]['main_menu'])
                            user_states[from_number] = {'state': 'awaiting_menu_choice', 'lang': lang}
                        else: resp.message(MESSAGES[lang]['invalid_district'])
                    except (ValueError, TypeError): resp.message(MESSAGES[lang]['invalid_district'])
            else: resp.message("Welcome! Please say 'hi' to start.")
        return str(resp)

    except Exception as e:
        logging.error(f"FATAL ERROR for number {request.values.get('From', '')}: {e}", exc_info=True)
        debug_resp = MessagingResponse()
        error_message = f"An unexpected error occurred. Please show this to the developer: {e}"
        debug_resp.message(error_message)
        return str(debug_resp)

@app.route("/delete_me")
def delete_my_data():
    my_number = os.environ.get("MY_NUMBER")
    if not my_number: return "MY_NUMBER not set in .env"
    try:
        delete_user(my_number)
        if my_number in user_states: del user_states[my_number]
        return f"User data for {my_number} has been deleted."
    except Exception as e: return f"Error deleting user: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)