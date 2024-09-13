import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import  ContextTypes
from models.model import simpan_interaksi, get_previous_interactions

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    Menyimpan user ID ke variabel global dan menampilkan pesan selamat datang.
    """
    global_user_id = None
    simpan_metadata(global_user_id, "Topik Awal", datetime.datetime.now())
    
    start_text = """
    Welcome to Learn from 0! 

    To begin, please select one of the topics
    """
    await update.message.reply_text(start_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    Menampilkan pesan bantuan tentang cara menggunakan bot.
    """

    help_text = """
    Learn from 0!
    
    To use this bot, simply follow these steps:
    1. Type /start to begin.
    2. Choose topic.
    3. Ask any question about the topic that you choosed
    
    Feel free to ask any questions to us.
    """
    await update.message.reply_text(help_text)

async def topic_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    Menampilkan daftar topik yang tersedia.
    """
    topics = [['Bisnis', 'Hukum', 'Coding']]

    reply_markup = ReplyKeyboardMarkup(topics, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Please choose a topic:", reply_markup=reply_markup)

async def bisnis_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mengirimkan informasi terkait topik 'Bisnis'.
    """
    bisnis_info = """
    Welcome to the Bisnis topic!
    
    Here you can ask anything related to business, such as:
    - How to start a business
    - Marketing strategies
    - Managing finances
    
    Feel free to ask your questions!
    """
    await update.message.reply_text(bisnis_info)

async def hukum_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mengirimkan informasi terkait topik 'Hukum'.
    """
    hukum_info = """
    Welcome to the Hukum topic!
    
    Here you can ask about legal matters, such as:
    - Corporate law
    - Personal legal issues
    - Government regulations
    
    Ask away!
    """
    await update.message.reply_text(hukum_info)

async def coding_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mengirimkan informasi terkait topik 'Coding'.
    """
    coding_info = """
    Welcome to the Coding topic!
    
    You can ask questions related to programming, including:
    - Web development
    - Python, JavaScript, etc.
    - Blockchain and more!
    
    Feel free to ask your coding questions!
    """
    await update.message.reply_text(coding_info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani pesan dan berinteraksi dengan Gemini."""
    user_message = update.message.text
    user_id = update.effective_user.id
    chosen_topic = None

    if user_message == 'bisnis':
        await bisnis_topic(update, context)
        chosen_topic = 'bisnis'
    elif user_message == 'hukum':
        await hukum_topic(update, context)
        chosen_topic = 'hukum'
    elif user_message == 'coding':
        await coding_topic(update, context)
        chosen_topic = 'coding'
    else:
        await update.message.reply_text("Please choose a valid topic.")
        return

    if chosen_topic:
        previous_interactions = get_previous_interactions(user_id, chosen_topic)
        if previous_interactions:
            context_string = "Riwayat percakapan:\n"
            for interaction in previous_interactions:
                context_string += f"User: {interaction['prompt']}\n"
                context_string += f"Bot: {interaction['response']}\n"
            prompt = f"{context_string}\nUser: {user_message}"
        else:
            prompt = user_message

        response = get_gemini_response(prompt)

        simpan_interaksi(user_id, chosen_topic, user_message, response)

        await update.message.reply_text(response)

    context.user_data['chosen_topic'] = chosen_topic