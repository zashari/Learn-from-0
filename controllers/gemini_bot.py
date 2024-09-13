from google.generativeai import text
from dotenv import find_dotenv, dotenv_values

config = dotenv_values(find_dotenv())
text.api_key = config.get("GEMINI_API")

def generate_text(prompt,
                   temperature=0.7, 
                   top_k=40, 
                   top_p=0.95, 
                   max_output_tokens=512):
    """
    Fungsi untuk melakukan generate text dengan Gemini
    """
    response = text.generate_text(
        prompt=prompt,
        model='models/gemini-pro-vision',
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        max_output_tokens=max_output_tokens
    )
    return response.result

def get_gemini_response(prompt, previous_interactions=None):
    """
    Fungsi utama untuk mendapatkan response dari Gemini. 
    Melakukan pre-prompting jika ada previous_interactions.
    """
    if previous_interactions:
        context_string = "Riwayat percakapan:\n"
        for interaction in previous_interactions:
            context_string += f"User: {interaction['prompt']}\n"
            context_string += f"Bot: {interaction['response']}\n"
        prompt = f"{context_string}\nUser: {prompt}"
    
    response = generate_text(prompt)
    return response