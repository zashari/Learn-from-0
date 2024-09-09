from dotenv import find_dotenv, dotenv_values
import google.generativeai as genai
import os

config = dotenv_values(find_dotenv())

genai.configure(api_key =config.get('GEMINI_API'))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)


