from handlers import add_admin, remove_admin, remove_user, register, unregister, help, get_id, get_users, get_admins
from telegram.ext import Application, CommandHandler
from telegram import Update
import json
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


async def main(event):
    app = Application.builder().token(token=os.getenv('BOT_TOKEN')).build()

    # Admin commands
    app.add_handler(CommandHandler('add_admin', add_admin))
    app.add_handler(CommandHandler('remove_admin', remove_admin))
    app.add_handler(CommandHandler('remove_user', remove_user))
    app.add_handler(CommandHandler('get_users', get_users))
    app.add_handler(CommandHandler('get_admins', get_admins))
    # User commands
    app.add_handler(CommandHandler('register', register))
    app.add_handler(CommandHandler('unregister', unregister))
    app.add_handler(CommandHandler('my_id', get_id))
    app.add_handler(CommandHandler('help', help))

    await app.initialize()
    update = Update.de_json(data=json.loads(event['body']), bot=app.bot)
    await app.process_update(update=update)


def lambda_handler(event, context):
    asyncio.run(main(event))


def test_main():
    app = Application.builder().token(token=os.getenv('BOT_TOKEN')).build()

    # Admin commands
    app.add_handler(CommandHandler('add_admin', add_admin))
    app.add_handler(CommandHandler('remove_admin', remove_admin))
    app.add_handler(CommandHandler('remove_user', remove_user))
    app.add_handler(CommandHandler('get_users', get_users))
    app.add_handler(CommandHandler('get_admins', get_admins))
    # User commands
    app.add_handler(CommandHandler('register', register))
    app.add_handler(CommandHandler('unregister', unregister))
    app.add_handler(CommandHandler('my_id', get_id))
    app.add_handler(CommandHandler('help', help))

    print("Bot running...")
    app.run_polling()


if __name__ == '__main__':
    test_main()
