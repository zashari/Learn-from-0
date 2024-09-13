from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import find_dotenv, dotenv_values
from controllers.telegram_bot import start_command, help_command, topic_command, handle_message

config = dotenv_values(find_dotenv())

def main():
    print('Starting the Bot...')
    app = Application.builder().token(config.get('BOT_URI')).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('topics', topic_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print('Polling...')
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()