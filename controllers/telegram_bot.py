import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import  ContextTypes
from controllers.gemini_bot import (
    get_gemini_response, 
    pre_analyze_conversation,
    gather_recent_knowledge, 
    DEFAULT_INSTRUCTION
)
from models.model import simpan_interaksi, get_previous_interactions, hapus_semua_interaksi

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    Menampilkan pesan bantuan tentang cara menggunakan bot.
    """

    help_text = """
    Learn from 0!
    
    To use this bot, simply follow these steps:
    1. Type /start to begin.
    2. Choose a topic.
    3. Ask any question about the topic that you choose.
    
    Feel free to ask any questions to us.
    """
    await update.message.reply_text(help_text)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    Menampilkan daftar topik yang tersedia.
    """
    topics = [['Bisnis', 'Hukum', 'Coding']]
    reply_markup = ReplyKeyboardMarkup(topics, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please choose a topic:", reply_markup=reply_markup)

async def set_topic(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str, prompt_text: str):
    """ Set topik dan menyiapkan prompt yang sesuai dengan topik yang dipilih """
    user_id = update.effective_user.id
    context.user_data['chosen_topic'] = topic
    context.user_data['default_prompt'] = prompt_text

    previous_interactions = get_previous_interactions(user_id, topic)

    if previous_interactions:
        keyboard = [
            [InlineKeyboardButton("Ya", callback_data='ya'),
             InlineKeyboardButton("Tidak", callback_data='tidak')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Apakah Anda ingin mengulang kembali pelajaran sebelumnya?",
                                        reply_markup=reply_markup)
        context.user_data['confirmation_sent'] = True
    else:
        await update.message.reply_text(f"Anda telah memilih topik {topic}. Silakan ajukan pertanyaan Anda.")
    
async def bisnis_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Mengirimkan informasi terkait topik 'Bisnis'. """
    prompt_text = """
    Kamu adalah asisten bisnis yang membantu dalam hal pemasaran, strategi, dan keuangan. 
    Jangan menjawab pertanyaan di luar topik bisnis.
    """
    await set_topic(update, context, 'Bisnis', prompt_text)

async def hukum_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Mengirimkan informasi terkait topik 'Hukum'. """
    prompt_text = """
    Kamu adalah asisten hukum yang ahli dalam hukum perusahaan dan peraturan pemerintah. 
    Berikan saran hukum dan fokuslah pada informasi umum.
    
    """
    await set_topic(update, context, 'Hukum', prompt_text)

async def coding_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Mengirimkan informasi terkait topik 'Coding'. """
    prompt_text = """
    Kamu adalah asisten coding yang membantu dalam dunia IT. Jadi bantulah User dengan baik.
    Berikan contoh kode jika diperlukan.
    """
    await set_topic(update, context, 'Coding', prompt_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    user_id = update.effective_user.id
    chosen_topic = context.user_data.get('chosen_topic')
    conversation_history = get_previous_interactions(user_id, chosen_topic) 

    if not chosen_topic:
        await update.message.reply_text("Pilih topik terlebih dahulu dengan menggunakan perintah /topics")
        return 

    conversation_history.append({
        "role": "user",
        "content": update.message.text 
    })

    response = get_gemini_response(update.message.text, conversation_history, DEFAULT_INSTRUCTION)  

    conversation_history.append({
        "role": "bot",
        "content": response
    })

    await update.message.reply_text(response) 

    # Store the complete conversation history
    for message in conversation_history:
        simpan_interaksi(user_id, chosen_topic, message)