import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import GenerationConfig, SafetySettingDict
from google.api_core import retry
import google.api_core.exceptions
from vector_db import add_user_interest, get_user_interests

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-pro')

# Safety settings
safety_settings = [
    SafetySettingDict(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    SafetySettingDict(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    SafetySettingDict(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_MEDIUM_AND_ABOVE"),
]

@retry.Retry(predicate=retry.if_exception_type(
    google.api_core.exceptions.ResourceExhausted,
    google.api_core.exceptions.ServiceUnavailable
))
def generate_ai_content(prompt, max_length=1000, temperature=1.0, top_k=40, top_p=0.95):
    try:
        generation_config = GenerationConfig(
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            max_output_tokens=max_length,
        )
        response = gemini_model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        if response.prompt_feedback.block_reason:
            return f"Content was blocked due to {response.prompt_feedback.block_reason}"
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_welcome_message():
    return "Content Generator: Hello! What would you like to do?"

def moderate_content(text):
    prompt = f"""
    Analyze the following content for:
    1. Coherence
    2. Contextual relevance
    3. Engagement
    4. Compliance with community guidelines (no hate speech, explicit content, or dangerous information)
    
    Only respond with 'PASS' if it meets all criteria, otherwise respond with 'FAIL':

    Content: {text}
    """
    try:
        response = gemini_model.generate_content(prompt, safety_settings=safety_settings)
        result = response.text.strip().upper()
        return "appropriate" if result == "PASS" else "inappropriate"
    except Exception as e:
        print(f"Moderation error: {str(e)}")
        return "inappropriate"  # Default to inappropriate if moderation fails

def generate_content(user_id, content_type, user_input=None):
    interests = get_user_interests(user_id)
    
    if content_type == "post":
        prompt = f"Generate an engaging social media post about one of these topics: {', '.join(interests)}. Do not use any special formatting or symbols for emphasis. Write in plain text."
    elif content_type == "comment":
        prompt = f"Generate a thoughtful comment on the following post, considering interests in {', '.join(interests)}: {user_input}. Respond in plain text without any special formatting."
    elif content_type == "response":
        prompt = f"Given the user's interests in {', '.join(interests)}, generate a response to: {user_input}. Use plain text only, without any special formatting."
    else:
        return "Invalid content type specified."
    
    content = generate_ai_content(prompt, max_length=1000, temperature=1.0)  # Increased max_length
    
    if moderate_content(content) == "inappropriate":
        return "Content generation failed due to potential guideline violation. Please try again."
    
    return content.strip()  # Remove any leading/trailing whitespace
    
   

def main():
    user_id = 1
    
    print("Content Generator: Hello! What would you like to do? (add_interest/generate/quit)")
    while True:
        action = input("Action: ").lower()
        if action == "quit":
            print("Content Generator: Goodbye!")
            break
        
        if action == "add_interest":
            interest = input("Enter your new interest: ")
            add_user_interest(user_id, interest)
            print(f"Interest '{interest}' added successfully.")
        elif action == "generate":
            content_type = input("Content type (post/comment/response): ").lower()
            if content_type not in ["post", "comment", "response"]:
                print("Invalid content type. Please choose post, comment, or response.")
                continue
            
            user_input = input("Input (for comment/response): ") if content_type in ["comment", "response"] else None
            generated_content = generate_content(user_id, content_type, user_input)
            print(f"Generated {content_type}:\n{generated_content}\n")
        else:
            print("Invalid action. Please choose add_interest, generate, or quit.")

if __name__ == "__main__":
    main()