import os
import vertexai
from vertexai.generative_models import GenerativeModel
from google.auth import default, exceptions

# --- Check for Credentials First ---
# This is a new check to see if your login is being detected.
try:
    credentials, project_id = default()
    print("✅ Google Cloud credentials found successfully.")
except exceptions.DefaultCredentialsError:
    print("❌ ERROR: Google Cloud credentials not found.")
    print("Please run 'gcloud auth application-default login' in your terminal.")
    exit() # Exit the script if credentials are not found

# --- Initialize Vertex AI ---
try:
    vertexai.init(project="aarogya-sarthi-472706", location="asia-south1", credentials=credentials)
    print("✅ Vertex AI initialized successfully.")
except Exception as e:
    print(f"❌ ERROR: Could not initialize Vertex AI: {e}")
    exit()

# --- Load the Gemini Model ---
# We are trying a different model to see if it resolves the access issue.
try:
    gemini_model = GenerativeModel("gemini-1.5-flash-001")
    print("✅ Gemini 1.5 Flash model loaded successfully.")
except Exception as e:
    print(f"❌ ERROR: Could not load the Gemini model: {e}")
    exit()


def get_gemini_response(prompt_text):
    """
    Sends a prompt to the Gemini model and returns the text response.
    """
    try:
        response = gemini_model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        print(f"❌ ERROR generating content from Gemini: {e}")
        return "Sorry, I am having trouble connecting to the AI model right now."

# --- A quick test to see if it works ---
if __name__ == '__main__':
    test_prompt = "What are the common symptoms of the flu?"
    print(f"\nSending test prompt: '{test_prompt}'")
    
    ai_response = get_gemini_response(test_prompt)
    
    print("\n--- AI Response ---")
    print(ai_response)
    print("-------------------")