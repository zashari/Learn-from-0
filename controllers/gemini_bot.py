import google.generativeai as genai
from dotenv import find_dotenv, dotenv_values

config = dotenv_values(find_dotenv())
genai.configure(api_key=config.get("GEMINI_API"))

def get_gemini_response(prompt, previous_interactions=None, instruction=None):
    """
    Fungsi utama untuk mendapatkan response dari Gemini. 
    Melakukan pre-prompting jika ada previous_interactions.
    """
    model = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction=instruction) 
    response = None
    if previous_interactions:
        context_string = "Riwayat percakapan:\n"
        for interaction in previous_interactions:
            context_string += f"User: {interaction['prompt']}\n"
            context_string += f"Bot: {interaction['response']}\n"
        new_prompt = f"{context_string}"
        response = model.generate_content(new_prompt)
    else:
        response = model.generate_content(prompt)

    return response.text