import os
from telegram.ext import Application, CommandHandler
from handlers import add_admin, register, unregister, help


def main():
    app = Application.builder().token(token=os.getenv('BOT_TOKEN')).build()

    app.add_handler(CommandHandler('hoto', add_admin))
    app.add_handler(CommandHandler('register', register))
    app.add_handler(CommandHandler('unregister', unregister))
    app.add_handler(CommandHandler('help', help))


if __name__ == '__main__':
    main()
