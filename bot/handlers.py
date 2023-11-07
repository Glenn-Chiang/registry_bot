import requests
from telegram import Update
from telegram.ext import CallbackContext
import os


# Add new clerk as admin: e.g. /add_admin 123
async def add_admin(update: Update, context: CallbackContext):
    # Check if user_id argument is provided
    if len(context.args != 1):
        await update.message.reply_text("Please provide the telegram user_id of the new registry clerk\ne.g. /hoto 123")
        return

    new_admin_id = context.args[0]

    try:
        await update.message.reply_text('Processing...')
        requests.post(
            f'https://add-admin-qbfqiotlpa-uc.a.run.app/?userId={new_admin_id}')
        await update.message.reply_text(f'Added user {new_admin_id} as admin')
    except Exception as error:
        await update.message.reply_text(f'Error handing over: {error}')


# Remove outgoing clerk's admin status
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
        await update.message.reply_text(f'Removed admin status from user {userId}')
    except Exception as error:
        await update.message.reply_text(f'Error handing over: {error}')


# Remove user by their callsign: /remove GLENN
async def remove(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide the callsign/name of the user to be removed")
        return

    # Handle names that contain spaces
    callsign = ('_').join(context.args)

    try:
        await update.message.reply_text('Processing...')
        requests.delete(
            f'https://remove-user-qbfqiotlpa-uc.a.run.app/?callsign={callsign}')
        await update.message.reply_text(f'{callsign} has been removed. They will no longer be sent notifications.')
    except Exception as error:
        await update.message.reply_text(f'Error removing user: {error}')


# Register yourself with your callsign
async def register(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide your callsign or name")
        return

    user_id = update.effective_user.id
    # Handle names that contain spaces
    callsign = (' ').join(context.args)

    try:
        await update.message.reply_text('Processing...')
        res = requests.post(
            f'https://register-qbfqiotlpa-uc.a.run.app/?userId={user_id}&callsign={callsign}')
        res.raise_for_status()
        await update.message.reply_text('Registered successfully')
    except Exception as error:
        # Send user-friendly error message
        await update.message.reply_text(f'Error registering: {error}')


# Unregister yourself
async def unregister(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    try:
        await update.message.reply_text('Processing...')
        requests.delete(
            f'https://unregister-qbfqiotlpa-uc.a.run.app/?userId={user_id}')
        await update.message.reply_text('Unregistered successfully. You will no longer receive notifications from this bot')
    except Exception as error:
        await update.message.reply_text(f'Error unregistering: {error}')


# Show list of commands
async def help(update: Update, context: CallbackContext):
    help_text = ""
    await update.message.reply_text(f"")
