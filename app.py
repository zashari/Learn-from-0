from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import find_dotenv, dotenv_values
from controllers.telegram_bot import start_command, help_command, handle_message, bisnis_topic, hukum_topic, coding_topic, handle_callback_query

config = dotenv_values(find_dotenv())

def main():
    print('Starting the Bot...')
    app = Application.builder().token(config.get('BOT_URI')).build()

    app.add_handler(CommandHandler(['start', 'topics'], start_command)) 
    app.add_handler(CommandHandler('help', help_command))

    # Tambahkan handler untuk topik Bisnis, Hukum, dan Coding
    app.add_handler(MessageHandler(filters.Regex('(?i)^bisnis$'), bisnis_topic))
    app.add_handler(MessageHandler(filters.Regex('(?i)^hukum$'), hukum_topic))
    app.add_handler(MessageHandler(filters.Regex('(?i)^coding$'), coding_topic))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback_query, pattern='^(ya|tidak)$'))

    print('Polling...')
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()