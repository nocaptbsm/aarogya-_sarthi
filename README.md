<p align="center">
  <img src="images/Aarogya.png" alt="Aarogya Sarthi Logo" width="150"/>
</p>

<h1 align="center">Aarogya Sarthi (आरोग्य सारथी) 🩺🤖</h1>

Aarogya Sarthi: AI-Powered Multilingual Health Assistant
A comprehensive AI health assistant delivered via WhatsApp and SMS, designed to bridge the healthcare accessibility gap for rural and tribal communities in Odisha.

Aarogya Sarthi is a sophisticated yet easy-to-use chatbot that provides instant, reliable, and localized health information. It was developed to tackle the critical challenge of limited access to healthcare professionals and information in remote areas, offering a vital first point of contact for health-related queries.

🌟 Core Features
🌐 True Multilingual Support: Fully operational in English, Hindi, Odia, Kui, and Santali, ensuring accessibility for diverse linguistic communities.

🤖 AI-Powered Symptom Checker: Utilizes Google's Gemini AI for a natural, conversational experience. The bot intelligently asks clarifying questions before providing safe, actionable advice, always reminding users to consult a doctor.

🚨 Proactive Outbreak Alerts: Connects to the World Health Organization (WHO) live feed to automatically push translated, location-relevant disease outbreak notifications to users when they start a conversation.

💉 Vaccination Reminders: Provides age-appropriate vaccination schedules (infant, child, adult) and uses the Google Maps API to find nearby clinics and hospitals that offer specific vaccines.

🌿 Personalized Health Tips: Delivers proactive, seasonal health tips (e.g., monsoon-specific advice for preventing dengue) based on the user's registered district.

👤 Smart Onboarding: A guided, multilingual registration process with validation to seamlessly onboard new users.

🛠️ Technology Stack & Architecture
This project leverages a modern, scalable backend architecture to deliver a robust user experience.

Backend: Python, Flask

Database: PostgreSQL on Google Cloud SQL

AI & NLP: Google Gemini 1.5 Flash

Messaging Platform: Twilio API for WhatsApp & SMS

Secure Connectivity:

Cloud SQL Auth Proxy: For secure, authenticated database connections without IP whitelisting.

Cloudflare Tunnel: To create a stable, permanent public URL for the local development server, replacing the need for ngrok.

Mapping: Google Maps Places API

Information Flow
User (WhatsApp/SMS) -> Twilio -> Cloudflare Tunnel -> Flask Backend (app.py) -> Feature Modules -> Gemini/Google Maps/Database -> Response to User

🚀 Getting Started
Follow these instructions to get the backend running on your local machine.

Prerequisites
Python 3.10+

A Google Cloud account (for Cloud SQL and Maps API)

A Twilio account

A Cloudflare account

Git

1. Clone the Repository
git clone [https://github.com/your-username/aarogya-_sarthi.git](https://github.com/your-username/aarogya-_sarthi.git)
cd aarogya-_sarthi/aarogya-sarthi-backend

2. Set Up the Environment
Create a virtual environment:

python -m venv venv

Activate it:

Windows: .\venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

3. Configure Environment Variables
Create a file named .env in the aarogya-sarthi-backend directory.

Copy the contents of .env.example into it and fill in your actual API keys and credentials.

4. Set Up the Database
Connect to your Google Cloud SQL instance.

Execute the SQL commands in the schema_v2.sql file to create all the necessary tables.

5. Run the Services
You need to run three services in three separate terminal windows:

Terminal 1: Start the Database Proxy

# Run the command from your start_proxy.bat file
cloud_sql_proxy -instances=...

Terminal 2: Start the Cloudflare Tunnel

# Run the command from your start_dns.bat file
cloudflared tunnel run your-tunnel-name

Terminal 3: Start the Flask Application

python app.py
