# content.py

from model_setup import gemini_model, safety_settings
from google.generativeai.types import GenerationConfig
from google.api_core import retry
import google.api_core.exceptions

@retry.Retry(predicate=retry.if_exception_type(
    google.api_core.exceptions.ResourceExhausted,
    google.api_core.exceptions.ServiceUnavailable
))
def generate_content(prompt, max_length=100, temperature=0.7, top_k=40, top_p=0.95):
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

        # Check if the response was blocked due to safety settings
        if response.prompt_feedback.block_reason:
            return f"Content was blocked due to {response.prompt_feedback.block_reason}"

        return [response.text]

    except google.api_core.exceptions.InvalidArgument as e:
        return [f"Invalid argument error: {str(e)}"]
    except google.api_core.exceptions.ResourceExhausted as e:
        return [f"Resource exhausted error: {str(e)}"]
    except google.api_core.exceptions.ServiceUnavailable as e:
        return [f"Service unavailable error: {str(e)}"]
    except Exception as e:
        return [f"An unexpected error occurred: {str(e)}"]

# Example usage
if __name__ == "__main__":
    user_prompt = ""
    generated_content = generate_content(
        user_prompt,
        max_length=150,
        temperature=0.8,
        top_k=50,
        top_p=0.9
    )
    print(generated_content)