from dotenv import find_dotenv, dotenv_values
import google.generativeai as genai
import os

config = dotenv_values(find_dotenv())

genai.configure(api_key =config.get('GEMINI_API'))

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def generate_gemini_response(prompt):
  """
  Menghasilkan respons dari model Gemini.

  Args:
      prompt: Pertanyaan pengguna (string).

  Returns:
      Respons dari Gemini (string) atau pesan error.
  """
  try:
    response = model.generate_content(prompt)
    return response.text
  except Exception as e:
    print(f"Error: {e}")
    return "Maaf, terjadi kesalahan saat memproses permintaan Anda."


