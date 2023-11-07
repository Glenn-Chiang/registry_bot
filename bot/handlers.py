import requests
from telegram import Update
from telegram.ext import CallbackContext
import os

API_URL = os.getenv('API_URL')

# HOTO to new registry clerk by their user_id: /hoto [user_id]
async def hoto(update: Update, context: CallbackContext): 
    # Check if user_id argument is provided
    if len(context.args != 1): 
        await update.message.reply_text("Please provide the telegram user_id of the new registry clerk\ne.g. /hoto 123")

    new_admin_id = context.args[0]

# Usser registers themself: /register [callsign]
async def register(update: Update, context: CallbackContext):
    if len(context.args) == 0: # No argument provided
        await update.message.reply_text("Please provide your callsign or name")
        return

    user_id = update.effective_user.id
    callsign = context.args[0]
    payload = {"userId": user_id, "callsign": callsign}

    try:
        await update.message.reply_text('Processing...')
        requests.post(f'{API_URL}', data=payload)
        await update.message.reply_text('Registered successfully')
    except Exception as error:
        await update.message.reply_text(f'Error registering: {error}') # Send user-friendly error message

# User unregisters themself: /unregister 
# No arguments required
async def unregister(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    try:
        await update.message.reply_text('Processing...')
        requests.delete(f'{API_URL}/?userId={user_id}')
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
        requests.delete(f'{API_URL}/?callsign={callsign}')
        await update.message.reply_text(f'{callsign} has been removed. They will no longer be sent notifications.')
    except Exception as error:
        await update.message.reply_text(f'Error removing user: {error}')
        
# Show list of commands
async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(f"")

