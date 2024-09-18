from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from controllers.gemini_bot import (
    get_gemini_response,
    DEFAULT_INSTRUCTION
)
from models.model import save_interaction, get_previous_interactions, delete_all_interactions

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    Display a help message about how to use the bot.
    """
    help_text = """
    Learn from 0!
    
    To use this bot, simply follow these steps:
    1. Type /start to begin.
    2. Choose a topic.
    3. Ask any question about the topic you've chosen.
    
    Feel free to ask us anything!
    """
    await update.message.reply_text(help_text)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    Display the list of available topics.
    """
    topics = [['Business', 'Law', 'Coding', 'Math']]
    reply_markup = ReplyKeyboardMarkup(topics, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please choose a topic:", reply_markup=reply_markup)

async def set_topic(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str, prompt_text: str):
    """ Set the topic and prepare the appropriate prompt for the chosen topic """
    user_id = update.effective_user.id
    context.user_data.pop('chosen_topic', None)
    context.user_data['chosen_topic'] = topic
    
    # Combine the topic-specific prompt_text with DEFAULT_INSTRUCTION
    combined_instruction = f"{DEFAULT_INSTRUCTION}\n\n{prompt_text}"
    context.user_data['system_instruction'] = combined_instruction

    previous_interactions = get_previous_interactions(user_id, topic)

    if previous_interactions:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='yes'),
             InlineKeyboardButton("No", callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Would you like to review your previous lessons?",
                                        reply_markup=reply_markup)
        context.user_data['confirmation_sent'] = True
    else:
        await update.message.reply_text(f"You have chosen the {topic} topic. Please ask your question.")

async def business_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Send information related to the 'Business' topic. """
    prompt_text = """
    You are a business expert assistant specializing in marketing, strategy, and finance. 
    Provide comprehensive answers to business-related questions, offering practical advice and theoretical knowledge.
    Use real-world examples and case studies when appropriate to illustrate concepts.
    If asked about recent business trends or news, acknowledge your knowledge cutoff and suggest the user verify current information.
    Do not answer questions outside the realm of business or outside the business topic.
    """
    await set_topic(update, context, 'Business', prompt_text)

async def law_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Send information related to the 'Law' topic. """
    prompt_text = """
    You are a legal expert assistant specializing in corporate law and government regulations. 
    Provide clear, accurate legal information and focus on general principles of law.
    Use hypothetical scenarios to explain complex legal concepts when appropriate.
    Always remind users that your information is for educational purposes and not a substitute for professional legal advice.
    Do not provide specific legal advice or answer questions outside the law topic.
    """
    await set_topic(update, context, 'Law', prompt_text)

async def coding_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Send information related to the 'Coding' topic. """
    prompt_text = """
    You are a coding expert assistant helping users with various programming languages and IT concepts. 
    Provide clear explanations of coding principles, best practices, and problem-solving strategies.
    When appropriate, offer code examples to illustrate concepts or solutions.
    Encourage good coding practices and explain the reasoning behind your suggestions.
    If asked about the latest programming trends or tools, acknowledge your knowledge cutoff and suggest the user verify current information.
    Do not write complete programs or debug extensive code without user interaction and do not answer questions outside coding topic.
    """
    await set_topic(update, context, 'Coding', prompt_text)

async def math_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Send information related to the 'Math' topic. """
    prompt_text = """
    You are a mathematics expert assistant helping users with various mathematical concepts and problem-solving. 
    Provide clear explanations of mathematical principles, formulas, and problem-solving techniques.
    When appropriate, offer step-by-step solutions to mathematical problems.
    Use visual representations (described in text) when it helps to clarify complex concepts.
    Encourage critical thinking and help users understand the underlying principles, not just memorize formulas.
    Do not solve homework problems without ensuring the user understands the process and do not answer questions outside math topic.
    """
    await set_topic(update, context, 'Math', prompt_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    user_id = update.effective_user.id
    chosen_topic = context.user_data.get('chosen_topic')

    if not chosen_topic:
        await update.message.reply_text("Please choose a topic first by using the /start command")
        return 

    conversation = []
    user_interaction = {
        "role": "user",
        "content": update.message.text 
    }
    conversation.append(user_interaction)

    # Use the combined instruction stored in user_data
    system_instruction = context.user_data.get('system_instruction', DEFAULT_INSTRUCTION)
    
    response = get_gemini_response(update.message.text, "", system_instruction)  

    bot_interaction = {
        "role": "bot",
        "content": response
    }
    conversation.append(bot_interaction)

    await update.message.reply_text(response) 

    # Store the conversation
    for msg in conversation:
        save_interaction(user_id, chosen_topic, msg)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer = query.data
    user_id = update.effective_user.id
    chosen_topic = context.user_data.get('chosen_topic')

    # Reset confirmation flag after user response
    context.user_data['confirmation_sent'] = False

    if answer == 'yes':
        # Retrieve previous interactions from the database
        previous_interactions = get_previous_interactions(user_id, chosen_topic)
        print("Interaksi Ditemukan: ", previous_interactions[0])
        context_string = "Analyze the Conversation History:\n"
        for interaction in previous_interactions:
            if 'role' in interaction and 'content' in interaction:
                context_string += f"{interaction['role'].capitalize()}: {interaction['content']}\n"
            else:
                print(f"Warning: Unexpected interaction format: {interaction}")
        new_prompt = f"{context_string}"
        
        system_instruction = context.user_data.get('system_instruction', DEFAULT_INSTRUCTION)
        
        # Send prompt to Gemini
        response = get_gemini_response(new_prompt, "", system_instruction)  # update.message.text here is an empty string
        
        await query.edit_message_text(text="Pre-prompting has been done. Please ask anything about the previous discussion.")
    elif answer == 'no':
        # Delete topic history if user chooses "No"
        delete_all_interactions(user_id, chosen_topic)
        await query.edit_message_text(text="Conversation history has been deleted. Please ask a new question.")
    else:
        await query.edit_message_text(text="Invalid choice.")