# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
# from telegram.ext import  ContextTypes
# from controllers.gemini_bot import get_gemini_response
# from models.model import simpan_interaksi, get_previous_interactions, hapus_riwayat_topik

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """ 
#     Menampilkan pesan bantuan tentang cara menggunakan bot.
#     """

#     help_text = """
#     Learn from 0!
    
#     To use this bot, simply follow these steps:
#     1. Type /start to begin.
#     2. Choose topic.
#     3. Ask any question about the topic that you choosed
    
#     Feel free to ask any questions to us.
#     """
#     await update.message.reply_text(help_text)

# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """ 
#     Menampilkan daftar topik yang tersedia.
#     """
#     topics = [['Bisnis', 'Hukum', 'Coding']]

#     reply_markup = ReplyKeyboardMarkup(topics, one_time_keyboard=True, resize_keyboard=True)

#     await update.message.reply_text("Please choose a topic:", reply_markup=reply_markup)

# async def bisnis_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Mengirimkan informasi terkait topik 'Bisnis'."""

#     default_prompt = """
#     Kamu adalah asisten bisnis yang membantu dalam hal pemasaran, strategi dan keuangan. 
#     Jangan menjawab pertanyaan di luar topik bisnis. 

#     User: {user_message}
#     """
#     context.user_data['default_prompt'] = default_prompt

#     await update.message.reply_text("Anda telah memilih topik Bisnis. Silakan ajukan pertanyaan Anda.")

# async def hukum_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Mengirimkan informasi terkait topik 'Hukum'."""

#     default_prompt = """
#     Kamu adalah asisten hukum yang ahli dalam hukum perusahaan dan peraturan pemerintah. 
#     Jangan memberikan saran hukum dan fokuslah pada informasi umum. 

#     User: {user_message}
#     """
#     context.user_data['default_prompt'] = default_prompt

#     await update.message.reply_text("Anda telah memilih topik Hukum. Silakan ajukan pertanyaan Anda.")

# async def coding_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Mengirimkan informasi terkait topik 'Coding'."""

#     default_prompt = """
#     Kamu adalah asisten coding yang membantu dalam dunia IT. Jadi bantulah User dengan baik
#     Berikan contoh kode jika diperlukan.

#     User: {user_message}
#     """
#     context.user_data['default_prompt'] = default_prompt

#     await update.message.reply_text("Anda telah memilih topik Coding. Silakan ajukan pertanyaan Anda.")

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     user_message = update.message.text.lower()
#     chosen_topic = None

#     if chosen_topic is None:
#         await update.message.reply_text("Pilih topik terlebih dahulu dengan menggunakan perintah /topics")
#         return
    
#     if user_message in ['bisnis', 'hukum', 'coding']:
#         if user_message == 'bisnis':
#             await bisnis_topic(update, context)
#         elif user_message == 'hukum':
#             await hukum_topic(update, context)
#         elif user_message == 'coding':
#             await coding_topic(update, context)
#     else:
#         previous_interactions = get_previous_interactions(user_id, chosen_topic)

#         if previous_interactions and not context.user_data.get('confirmation_sent'):
#             keyboard = [
#                 [InlineKeyboardButton("Ya", callback_data='ya'),
#                  InlineKeyboardButton("Tidak", callback_data='tidak')]
#             ]
#             reply_markup = InlineKeyboardMarkup(keyboard)
#             await update.message.reply_text("Apakah Anda ingin mengulang kembali pelajaran sebelumnya?",
#                                             reply_markup=reply_markup)
            
#             context.user_data['confirmation_sent'] = True
#             context.user_data['last_topic'] = chosen_topic
#             return

#         elif context.user_data.get('confirmation_sent'):
#             query = update.callback_query
#             answer = query.data
#             context.user_data['confirmation_sent'] = False

#             if answer == 'ya':
#                 context.user_data['use_pre_prompt'] = True
#                 await query.edit_message_text(text="Pre-prompting sudah dilakukan. Silahkan tanyakan apapun mengenai pembahasan sebelumnya.")
#                 return 

#             elif answer == 'tidak':
#                 hapus_riwayat_topik(user_id, chosen_topic)
#                 await query.edit_message_text(text="Riwayat percakapan dihapus. Silahkan ajukan pertanyaan baru.")

#             else:
#                 await query.edit_message_text(text="Pilihan tidak valid.")
#                 return
            
#         if context.user_data.get('use_pre_prompt'):
#             previous_interactions = get_previous_interactions(user_id, chosen_topic)
#             context.user_data['use_pre_prompt'] = False
        
#         system_instruction = context.user_data.get('system_instruction')
#         response = get_gemini_response(update.message.text, previous_interactions, system_instruction)
#         await update.message.reply_text(response)
#         simpan_interaksi(user_id, chosen_topic, update.message.text, response)


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import  ContextTypes
from controllers.gemini_bot import get_gemini_response
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

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id

#     # Ambil last topic dari user data (menggunakan topik terakhir yang dipilih)
#     chosen_topic = context.user_data.get('chosen_topic')

#     # Jika belum ada topik yang dipilih dan pesan bukan salah satu topik yang ada
#     if not chosen_topic:
#         await update.message.reply_text("Pilih topik terlebih dahulu dengan menggunakan perintah /topics")
#         return

#     # Cek apakah user telah memilih untuk mengulang pembahasan sebelumnya
#     if update.callback_query:
#         print("Callback Query Received")  # Debugging output
#         query = update.callback_query
#         answer = query.data
#         print(f"Answer: {answer}")  # Debugging output
        
#         # Reset flag confirmation setelah user merespon
#         context.user_data['confirmation_sent'] = False

#         if answer == 'ya':
#             # Ambil interaksi sebelumnya dari database
#             previous_interactions = get_previous_interactions(user_id, context.user_data.get('chosen_topic'))
#             system_instruction = context.user_data.get('system_instruction')
#             response = get_gemini_response(update.message.text, previous_interactions, system_instruction)
#             print("Response Pre-prompting: ", response)  # Debugging output

#             # Simpan interaksi baru
#             simpan_interaksi(user_id, context.user_data.get('chosen_topic'), update.message.text, response)
#             await query.edit_message_text(text="Pre-prompting sudah dilakukan. Silahkan tanyakan apapun mengenai pembahasan sebelumnya.")
#         elif answer == 'tidak':
#             # Hapus riwayat topik jika user memilih "Tidak"
#             hapus_semua_interaksi(user_id, context.user_data.get('chosen_topic'))
#             await query.edit_message_text(text="Riwayat percakapan dihapus. Silakan ajukan pertanyaan baru.")
#         else:
#             await query.edit_message_text(text="Pilihan tidak valid.")
#         return

#     # Jika tidak sedang pre-prompt, lanjutkan logika normal
#     system_instruction = context.user_data.get('system_instruction')
#     response = get_gemini_response(update.message.text, [], system_instruction)

#     await update.message.reply_text(response)
#     simpan_interaksi(user_id, context.user_data.get('chosen_topic'), update.message.text, response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tangani pesan teks biasa
    if update.message:
        user_id = update.effective_user.id
        chosen_topic = context.user_data.get('chosen_topic')

        if not chosen_topic:
            await update.message.reply_text("Pilih topik terlebih dahulu dengan menggunakan perintah /topics")
            return

        system_instruction = context.user_data.get('system_instruction')
        response = get_gemini_response(update.message.text, [], system_instruction)

        await update.message.reply_text(response)
        simpan_interaksi(user_id, chosen_topic, update.message.text, response)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    answer = query.data
    user_id = update.effective_user.id
    chosen_topic = context.user_data.get('chosen_topic')

    # Reset flag confirmation setelah user merespon
    context.user_data['confirmation_sent'] = False

    if answer == 'ya':
        # Ambil interaksi sebelumnya dari database
        previous_interactions = get_previous_interactions(user_id, chosen_topic)
        system_instruction = context.user_data.get('system_instruction')
        
        # Kirim prompt ke Gemini
        response = get_gemini_response("", previous_interactions, system_instruction)  # update.message.text di sini adalah string kosong
        
        await query.edit_message_text(text="Pre-prompting sudah dilakukan. Silahkan tanyakan apapun mengenai pembahasan sebelumnya.")
    elif answer == 'tidak':
        # Hapus riwayat topik jika user memilih "Tidak"
        hapus_semua_interaksi(user_id, chosen_topic)
        await query.edit_message_text(text="Riwayat percakapan dihapus. Silakan ajukan pertanyaan baru.")
    else:
        await query.edit_message_text(text="Pilihan tidak valid.")
