import requests
from telegram import Update
from telegram.ext import CallbackContext
import os

API_URL = os.getenv('API_URL')

# HOTO to new registry clerk by their user_id: /hoto [user_id]


async def add_admin(update: Update, context: CallbackContext):
    # Check if user_id argument is provided
    if len(context.args != 1):
        await update.message.reply_text("Please provide the telegram user_id of the new registry clerk\ne.g. /hoto 123")
        return

    new_admin_id = context.args[0]

    try:
        await update.message.reply_text('Processing...')
        requests.post(
            f' https://add-admin-qbfqiotlpa-uc.a.run.app/?userId={new_admin_id}')
        await update.message.reply_text(f'Handed over to user {new_admin_id}')
    except Exception as error:
        await update.message.reply_text(f'Error handing over: {error}')


async def remove_admin(update: Update, context: CallbackContext):
    # Check if user_id argument is provided
    if len(context.args != 1):
        await update.message.reply_text("Please provide the telegram user_id of the outgoing registry clerk\ne.g. /hoto 123")
        return

    userId = context.args[0]

    try:
        await update.message.reply_text('Processing...')
        requests.post(
            f'https://remove-admin-qbfqiotlpa-uc.a.run.app/?userId={userId}')
        await update.message.reply_text(f'Handed over to user {userId}')
    except Exception as error:
        await update.message.reply_text(f'Error handing over: {error}')


async def register(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide your callsign or name")
        return

    user_id = update.effective_user.id
    callsign = context.args[0]
    payload = {"userId": user_id, "callsign": callsign}

    try:
        await update.message.reply_text('Processing...')
        requests.post(
            f'https://register-qbfqiotlpa-uc.a.run.app', data=payload)
        await update.message.reply_text('Registered successfully')
    except Exception as error:
        # Send user-friendly error message
        await update.message.reply_text(f'Error registering: {error}')

# User unregisters themself: /unregister
# No arguments required


async def unregister(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    try:
        await update.message.reply_text('Processing...')
        requests.delete(
            f'https://unregister-qbfqiotlpa-uc.a.run.app/?userId={user_id}')
        await update.message.reply_text('Unregistered successfully. You will no longer receive notifications from this bot')
    except Exception as error:
        await update.message.reply_text(f'Error unregistering: {error}')

# Remove user by their callsign: /remove GLENN


async def remove(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide the callsign/name of the user to be removed")
        return

    callsign = context.args[0]

    try:
        await update.message.reply_text('Processing...')
        requests.delete(
            f'https://remove-user-qbfqiotlpa-uc.a.run.app/?callsign={callsign}')
        await update.message.reply_text(f'{callsign} has been removed. They will no longer be sent notifications.')
    except Exception as error:
        await update.message.reply_text(f'Error removing user: {error}')

# Show list of commands


async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(f"")
