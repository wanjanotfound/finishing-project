# model_setup.py

import google.generativeai as genai
from google.generativeai.types import SafetySettingDict

def setup_gemini():
    # Replace with your actual API key
    genai.configure(api_key='AIzaSyDb1pQJSNf3Zre8XbM_mcSKNsX9VYiBGdM')
    
    # For this example, we'll use the gemini-pro model
    model = genai.GenerativeModel('gemini-pro')
    
    return model

# Define safety settings
safety_settings = [
    SafetySettingDict(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    SafetySettingDict(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    SafetySettingDict(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
]

gemini_model = setup_gemini()