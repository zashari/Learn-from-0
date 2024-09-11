import os, sys
import pymongo
from urllib.request import urlopen
sys.path.insert(0, '../')
from dotenv import find_dotenv, dotenv_values
from devs import generate_gemini_response
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

config = dotenv_values(find_dotenv())

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    YANG INI TIDAK USAH DISENTUH
    YANG INI TIDAK USAH DISENTUH
    YANG INI TIDAK USAH DISENTUH
    YANG INI TIDAK USAH DISENTUH 
    """
    start_text = """
    Welcome to Learn from 0! 
    
    To begin, please select one of the topics
    
    """
    await update.message.reply_text(start_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ 
    YANG INI TIDAK USAH DISENTUH
    YANG INI TIDAK USAH DISENTUH
    YANG INI TIDAK USAH DISENTUH
    YANG INI TIDAK USAH DISENTUH
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
    Kalo mau tambah topic, tinggal tambah di samping 'Coding' yang line 50
    """
    topics = [['Bisnis', 'Hukum', 'Coding']]

    reply_markup = ReplyKeyboardMarkup(topics, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text("Please choose a topic:", reply_markup=reply_markup)

async def bisnis_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mengirimkan informasi terkait topik 'Bisnis'.
    
    Fungsi ini menangani pertanyaan pengguna seputar bisnis, seperti memulai bisnis,
    strategi pemasaran, atau manajemen keuangan.
    
    Args:
        update: Mewakili pembaruan yang diterima dari Telegram, berisi data pesan dan pengguna.
        context: Menyediakan informasi tentang status percakapan dan konteks bot.
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
    
    Fungsi ini menangani pertanyaan pengguna terkait masalah hukum, seperti hukum perusahaan,
    masalah hukum pribadi, atau regulasi pemerintah.
    
    Args:
        update: Mewakili pembaruan yang diterima dari Telegram, berisi data pesan dan pengguna.
        context: Menyediakan informasi tentang status percakapan dan konteks bot.
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
    
    Fungsi ini memberikan jawaban terkait pemrograman, termasuk pengembangan web,
    bahasa pemrograman seperti Python dan JavaScript, serta teknologi seperti blockchain.
    
    Args:
        update: Mewakili pembaruan yang diterima dari Telegram, berisi data pesan dan pengguna.
        context: Menyediakan informasi tentang status percakapan dan konteks bot.
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
    user_message = update.message.text.lower()
    """
    Menangani pesan teks yang dikirim pengguna.
    
    Fungsi ini memproses pesan yang dikirim pengguna setelah memilih topik. 
    Jika pengguna memilih topik 'Bisnis', 'Hukum', atau 'Coding', fungsi yang sesuai akan dijalankan.
    
    Args:
        update: Mewakili pembaruan yang diterima dari Telegram, berisi data pesan dan pengguna.
        context: Menyediakan informasi tentang status percakapan dan konteks bot.
    """
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    if user_message == 'bisnis':
        await bisnis_topic(update, context)
    elif user_message == 'hukum':
        await hukum_topic(update, context)
    elif user_message == 'coding':
        await coding_topic(update, context)
    elif 'web development' in user_message:  # Pencocokan fleksibel
        materi_webdev = """
        ## Materi Web Development:
        
        **Pengenalan:**
        - Apa itu web development?
        - Front-end, Back-end, dan Full-stack
        
        **Teknologi Dasar:**
        - HTML
        - CSS
        - JavaScript
        
        **Framework Populer:**
        - React
        - Angular
        - Vue.js

        **Dan banyak lagi!**
        
        **Sumber Belajar:**
        - [freeCodeCamp](https://www.freecodecamp.org/)
        - [Codecademy](https://www.codecademy.com/)
        - [Mozilla Developer Network (MDN)](https://developer.mozilla.org/en-US/)
        """
        await update.message.reply_text(materi_webdev, parse_mode='Markdown')
        
    elif 'corporate law' in user_message.lower():
        materi_corporate_law = """
        ## Corporate Law:

        Mengenai hukum yang mengatur perusahaan & bisnis, termasuk:
        - **Pembentukan Perusahaan:**  PT, CV, dll.
        - **Merger & Akuisisi:**  Penggabungan & pengambilalihan perusahaan.
        - **Good Corporate Governance (GCG):**  Tata Kelola Perusahaan yang baik.
        
        **Info Lebih Lanjut:** [Website Resmi OJK](https://www.ojk.go.id/)
        """
        await update.message.reply_text(materi_corporate_law, parse_mode='Markdown')

    elif 'personal legal issues' in user_message.lower():
        materi_personal_legal = """
        ## Personal Legal Issues:

        Meliputi masalah hukum yang dihadapi individu, seperti:
        - **Perkawinan & Perceraian:**  Hak & kewajiban dalam rumah tangga.
        - **Warisan:**  Pembagian harta warisan.
        - **Konsumen:**  Perlindungan konsumen, sengketa transaksi.

        **Info Lebih Lanjut:** [Kementerian Hukum dan HAM](https://www.kemenkumham.go.id/) 
        """
        await update.message.reply_text(materi_personal_legal, parse_mode='Markdown')

    elif 'government regulation' in user_message.lower():
        materi_gov_regulation = """
        ## Government Regulation:

        Aturan & regulasi yang dikeluarkan pemerintah, meliputi:
        - **Peraturan Pemerintah (PP)**
        - **Peraturan Presiden (Perpres)**
        - **Peraturan Menteri**

        **Info Lebih Lanjut:** [JDIH - Jaringan Dokumentasi dan Informasi Hukum](https://jdih.go.id/) 
        """
        await update.message.reply_text(materi_gov_regulation, parse_mode='Markdown') 
    else:
        # Jika tidak ada kata kunci topik, teruskan ke Gemini
        gemini_response = generate_gemini_response(user_message) 
        await update.message.reply_text(gemini_response)
        if not gemini_response or gemini_response.strip() == "": 
            await update.message.reply_text("Please choose a valid topic.")
    

def main():
    """
    Fungsi utama yang menginisialisasi dan menjalankan bot.

    Fungsi ini mengatur bot dengan menambahkan command handler dan message handler, 
    kemudian menjalankan polling untuk menerima pesan dari pengguna.
    """
    print('Starting the Bot...')
    app = Application.builder().token(config.get('BOT_URI')).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('topics', topic_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('Polling...')
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    # mongodb_client = initialize()
    # setup_llm()
    # connect_llm(mongodb_client)
    main()