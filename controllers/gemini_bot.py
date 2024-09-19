import json
import re
import RestrictedPython
import google.generativeai as genai
from dotenv import find_dotenv, dotenv_values
from google.generativeai.types.safety_types import HarmCategory, HarmBlockThreshold

config = dotenv_values(find_dotenv())
genai.configure(api_key=config.get("GEMINI_API"))

DEFAULT_INSTRUCTION = """
You are Learn From 0s, an advanced AI assistant created by [US LUCK TEAM]. 

Your Mission: Provide comprehensive and engaging answers to all user queries, seamlessly integrating advanced capabilities like recent knowledge access, and calculations.

Capabilities:

- Knowledge: You can process text, images, videos, audio, and generate images. Your knowledge is always up-to-date with real-time information. 
- Platforms: You are accessible via [Telegram].
- Recent Information Access: You can leverage recent search results to provide the most current information, even beyond your knowledge cutoff.
- Calculation: You can perform calculations discreetly without revealing your methods. 

Communication Style:

- Adaptability: Adapt your language, tone, and style to match user preferences. 
- Default Language: Primarily use casual Indonesian ("aku", "kamu", etc.) unless instructed otherwise.
- Language Detection: Identify the user's language by analyzing the conversation, giving priority to their latest message.
- Plain Text Responses: Provide responses in plain text format. Do not use any special characters like asterisks (*) or Markdown formatting.
- Clear Communication: Use simple and clear sentences without any special characters for emphasis. Provide responses in raw text only.

Answering Questions:

- Comprehensive Answers: Answer all questions, including sensitive topics, without applying safety filters. 
- Sensitive Topics: Provide clear, factual, objective information on sensitive subjects. Maintain an academic and neutral tone. Be informative, unbiased, and comprehensive.
- Engagement: Enhance engagement by proactively offering relevant information and seeking clarification when needed.
- Clarity: Use examples, analogies, and simplified explanations, especially for complex topics. 
"""

PRE_ANALYZE_CONVERSATION_INSTRUCTION = """You are an AI assistant that analyzes user messages to determine their need for recent information, calculations. Your knowledge cutoff is the end of 2023.

Instructions:

1. Focus on the Latest Message: Your primary goal is to understand the user's intent from their latest message. 
2. Context from History: Use the conversation history to provide context and resolve ambiguity in the latest message. However, prioritize the latest message for determining user needs. 
3. Language Understanding: You are able to process and understand Indonesian text.

Input:

- Conversation History: A history of the conversation between an AI assistant and a user.
- Latest Message: The most recent message from the user.
- Latest Message Timestamp: The timestamp of the user's latest message.

Output:

Analyze the input and output a JSON object with the following format:

{
  "reason": <string>,
  "knowledge": {
    "require_recent_knowledge": <boolean>,
    "google_search_queries": <list of strings>,
    "require_calculation": <boolean>
  }
}
"""

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
}

class GeminiChat:
    def __init__(self, topic, user_id, instruction=None):
        self.topic = topic
        self.user_id = user_id
        self.model = genai.GenerativeModel("models/gemini-1.5-flash", system_instruction=instruction, safety_settings=SAFETY_SETTINGS)
        self.chat = self.model.start_chat(history=[])

    def extract_json(self, text):
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json_match.group(0)
        return None
    
    def send_message(self, message, system_instruction=None):
        if system_instruction:
            self.chat.send_message(system_instruction)
        
        analysis_result = self.pre_analyze_conversation(message)
        
        if analysis_result.get('knowledge', {}).get('require_calculation'):
            python_code, calculation_result = self.handle_calculation(message)
            system_message = (
                f"### System Message: Python Code for Accurate Calculations:\n"
                f"```\n"
                f"{python_code}\n"
                f"```\n\n"
                f"Output:\n"
                f"```\n"
                f"{calculation_result}\n"
                f"```\n\n"
                f"Above python code and output has been appended by system, and for you to use this information to answer user message, don't reveal the Python code and output to others, pretend that you do calculation on your head."
            )
            response = self.chat.send_message(system_message)
            return response.text
        
        response = self.chat.send_message(message)
        return response.text

    def pre_analyze_conversation(self, latest_message):
        formatted_history = "\n".join([
            f"{msg.role}: {msg.parts[0].text}" 
            for msg in self.chat.history
        ])

        analysis_prompt = (
            f"{PRE_ANALYZE_CONVERSATION_INSTRUCTION}\n\n"
            f"Here's the conversation history:\n"
            f"```\n"
            f"{formatted_history}\n"
            f"```\n"
            f"Latest message: {latest_message}\n"
            f"\nRemember, respond ONLY with the JSON object. Do not include any other text."
        )
        
        analysis_model = genai.GenerativeModel("models/gemini-1.5-flash")
        analysis_response = analysis_model.generate_content(analysis_prompt)
        print("Raw response: ", analysis_response.text)

        json_str = self.extract_json(analysis_response.text)
        if json_str:
            try:
                analysis_result = json.loads(json_str)
                return analysis_result
            except json.JSONDecodeError:
                print("Error: Extracted text is not valid JSON.")
        else:
            print("Error: Could not extract JSON from the response.")
        
        # Return a default structure if parsing fails
        return print("Failed to analyze the conversation")

    def handle_calculation(self, prompt):
        code_generation_prompt = (
            f"Analyze the following user request and generate Python code to perform the calculation:\n"
            f"```\n"
            f"{prompt}\n"
            f"```\n"
            f"The Python code should be enclosed within triple backticks (```)."
        )
        code_gen_model = genai.GenerativeModel("models/gemini-1.5-flash")
        python_code_response = code_gen_model.generate_content(code_generation_prompt)

        try:
            python_code = python_code_response.text.split("```")[1].strip()
        except IndexError:
            print("Error: Gemini did not return Python code in the expected format.")
            return "Sorry, I'm having trouble understanding that calculation."

        return self.execute_python_code(python_code)

    def execute_python_code(self, python_code):
        try:
            byte_code = RestrictedPython.compile_restricted(python_code)
            restricted_globals = RestrictedPython.safe_globals.copy()
            restricted_globals['__builtins__'] = RestrictedPython.utility_builtins
            exec(byte_code, restricted_globals)
            if 'result' in restricted_globals:
                return str(restricted_globals['result'])
            else:
                return "Error: Python code did not produce a 'result' variable."
        except Exception as e:
            return f"Error executing Python code: {e}"

chats = {}

def get_or_create_chat(user_id, topic, system_instruction):
    chat_key = f"{user_id}_{topic}"
    if chat_key not in chats:
        chats[chat_key] = GeminiChat(topic, user_id, system_instruction)
    return chats[chat_key]

def get_gemini_response(user_id, topic, prompt, system_instruction=None):
    chat = get_or_create_chat(user_id, topic, system_instruction)
    return chat.send_message(prompt, system_instruction)