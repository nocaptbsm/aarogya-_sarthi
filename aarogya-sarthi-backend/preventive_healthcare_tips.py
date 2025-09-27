import datetime
import logging

TIPS_BY_SEASON = {
    'summer': {
        'title_en': "Summer Health Tips", 'title_hi': "गर्मी के स्वास्थ्य सुझाव", 'title_od': "ଗ୍ରୀଷ୍ମ ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ", 'title_kui': "ଗ୍ରୀଷ୍ମ ଦିନର ସ୍ୱାସ୍ଥ୍ୟ କଥା", 'title_sa': "ᱥᱤᱛᱩᱝ ᱫᱤᱱ ᱨᱮᱭᱟᱜ ᱦᱚᱲᱢᱚ ᱥᱟᱵᱽଧାନ",
        'tip_en': "Stay hydrated by drinking plenty of water. Avoid direct sun between 12 PM and 4 PM. Eat light, seasonal fruits.",
        'tip_hi': "खूब पानी पीकर हाइड्रेटेड रहें। दोपहर 12 बजे से 4 बजे के बीच सीधी धूप से बचें। हल्के, मौसमी फल खाएं।",
        'tip_od': "ପର୍ଯ୍ୟାପ୍ତ ପାଣି ପିଇ ହାଇଡ୍ରେଟେଡ୍ ରୁହନ୍ତୁ। ଦିନ 12ଟାରୁ 4ଟା ମଧ୍ୟରେ ସିଧାସଳଖ ସୂର୍ଯ୍ୟ କିରଣରୁ ଦୂରେଇ ରୁହନ୍ତୁ। ହାଲୁକା, ଋତୁକାଳୀନ ଫଳ ଖାଆନ୍ତୁ।",
        'tip_kui': "ବେଶୀ ପାଣି ପିଅନ୍ତୁ। ଦିନ 12ଟାରୁ 4ଟା ଭିତରେ ଖରାକୁ ଯାଆନ୍ତୁ ନାହିଁ। ହାଲୁକା ଫଳ ଖାଆନ୍ତୁ।",
        'tip_sa': "ᱟᱹᱰᱤ ᱜᱟᱱ ᱫᱟᱜ ᱧᱩᱭ ᱯᱮ᱾ ᱑᱒ ᱵᱟᱡᱟ ᱠᱷᱚᱱ ᱔ ᱵᱟᱡᱟ ᱫᱷᱟᱹବᱤᱡ ᱥᱤଧା ᱥᱤᱛᱩᱝ ᱨᱮ ᱟᱞᱚᱯᱮ ᱚḍੋᱠ-ᱟ᱾ ᱦᱟᱞᱠᱟ,  मौसम ᱨᱮᱭᱟᱜ ᱯᱷᱚળ ᱡᱚᱢ ᱯᱮ।"
    },
    'monsoon': {
        'title_en': "Monsoon Health Tips", 'title_hi': "मानसून के स्वास्थ्य सुझाव", 'title_od': "ମୌସୁମୀ ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ", 'title_kui': "ବର୍ଷା ଦିନର ସ୍ୱାସ୍ଥ୍ୟ କଥା", 'title_sa': "ᱡᱟᱹᱯᱩᱫ ᱫᱤᱱ ᱨᱮᱭᱟᱜ ᱦᱚᱲᱢᱚ ᱥᱟᱵᱽଧାନ",
        'tip_en': "Protect yourself from mosquitoes to prevent Dengue and Malaria. Drink boiled water and avoid street food to prevent water-borne diseases.",
        'tip_hi': "डेंगू और मलेरिया से बचने के लिए खुद को मच्छरों से बचाएं। पानी से होने वाली बीमारियों से बचने के लिए उबला हुआ पानी पिएं और स्ट्रीट फूड से बचें।",
        'tip_od': "ଡେଙ୍ଗୁ ଓ ମ୍ୟାଲେରିଆରୁ ରକ୍ଷା ପାଇବା ପାଇଁ ନିଜକୁ ମଶାଙ୍କଠାରୁ ଦୂରେଇ ରଖନ୍ତୁ। ପାଣିଜନିତ ରୋଗରୁ ବଞ୍ଚିବା ପାଇଁ ଫୁଟା ପାଣି ପିଅନ୍ତୁ ଏବଂ ରାସ୍ତା କଡ଼ ଖାଦ୍ୟରୁ ଦୂରେଇ ରୁହନ୍ତୁ।",
        'tip_kui': "ମଶାଙ୍କଠାରୁ ନିଜକୁ ବଞ୍ଚାନ୍ତୁ। ଫୁଟା ପାଣି ପିଅନ୍ତୁ ଏବଂ ବାହାର ଖାଦ୍ୟ ଖାଆନ୍ତୁ ନାହିଁ।",
        'tip_sa': "ᱥᱤᱠᱤᱲᱤ ᱠᱷᱚᱱ ᱵᱟᱧ୍ଚᱟᱣ ᱞᱟᱹᱜᱤᱫ নিজেকে বাঁচান। 끓ানো পানি পান করুন এবং রাস্তার খাবার এড়িয়ে চলুন।"
    },
    'winter': {
        'title_en': "Winter Health Tips", 'title_hi': "सर्दियों के स्वास्थ्य सुझाव", 'title_od': "ଶୀତଦିନର ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ", 'title_kui': "ଶୀତ ଦିନର ସ୍ୱାସ୍ଥ୍ୟ କଥା", 'title_sa': "ᱨᱟᱵᱟᱝ ᱫᱤᱱ ᱨᱮᱭᱟᱜ ᱦᱚᱲᱢᱚ ᱥᱟᱵᱽଧାନ",
        'tip_en': "Keep warm to avoid colds and flu. Eat foods rich in Vitamin C like oranges to boost your immunity. Keep your skin moisturized.",
        'tip_hi': "सर्दी और फ्लू से बचने के लिए गर्म रहें। अपनी रोग प्रतिरोधक क्षमता को बढ़ाने के लिए संतरे जैसे विटामिन सी से भरपूर खाद्य पदार्थ खाएं। अपनी त्वचा को नमीयुक्त रखें।",
        'tip_od': "ଥଣ୍ଡା ଏବଂ ଫ୍ଲୁରୁ ରକ୍ଷା ପାଇବା ପାଇଁ ନିଜକୁ ଉଷୁମ ରଖନ୍ତୁ। ଆପଣଙ୍କ ରୋଗ ପ୍ରତିରୋଧକ ଶକ୍ତି ବଢ଼ାଇବା ପାଇଁ କମଳା ପରି ଭିଟାମିନ୍ ସିରେ ଭରପୂର ଖାଦ୍ୟ ଖାଆନ୍ତୁ। ଆପଣଙ୍କ ତ୍ୱଚାକୁ ଆର୍ଦ୍ର ରଖନ୍ତୁ।",
        'tip_kui': "ଥଣ୍ଡାରୁ ବଞ୍ଚିବା ପାଇଁ ଗରମରେ ରୁହନ୍ତୁ। କମଳା ପରି ଭିଟାମିନ୍ ସି ଥିବା ଖାଦ୍ୟ ଖାଆନ୍ତୁ। ଚମକୁ ଶୁଖିଲା ରଖନ୍ତୁ ନାହିଁ।",
        'tip_sa': "춥 ও ফ্লু থেকে বাঁচতে গরম থাকুন। কমলালেবুর মতো ভিটামিন সি সমৃদ্ধ খাবার খেয়ে আপনার রোগ প্রতিরোধ ক্ষমতা বাড়ান। আপনার ত্বককে ময়েশ্চারাইজড রাখুন।"
    }
}

def get_current_season():
    """Determines the current season in India based on the month."""
    month = datetime.datetime.now().month
    if month in [3, 4, 5]: return 'summer'
    elif month in [6, 7, 8, 9]: return 'monsoon'
    else: return 'winter'

def get_preventive_tips(user, lang, MESSAGES):
    """Generates a personalized preventive healthcare tip message."""
    try:
        season = get_current_season()
        # --- BUG FIX: Use correct index for district ---
        user_district = user[6]  # id=0, mobile=1, name=2, age=3, gender=4, state=5, district=6
        
        seasonal_tips = TIPS_BY_SEASON.get(season)
        if not seasonal_tips:
            return None

        title = seasonal_tips.get(f'title_{lang}', seasonal_tips['title_en'])
        tip = seasonal_tips.get(f'tip_{lang}', seasonal_tips['tip_en'])
        
        intro = MESSAGES[lang].get('preventive_tips_intro', "Here's a health tip for your area:")
        
        message = f"*{intro}*\n\n*{title} for {user_district}*\n- {tip}"
        return message

    except (IndexError, KeyError) as e:
        logging.error(f"Could not generate preventive tips for user: {e}")
        return None

