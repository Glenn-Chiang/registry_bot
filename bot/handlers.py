import requests
from telegram import Update
from telegram.ext import CallbackContext
import os


# Add new admin by theier user_id: e.g. /add_admin 123
async def add_admin(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide the callsign/name of the user to be promoted to admin\n\ne.g. /add_admin GLENN")
        return

    callsign = ('_').join(context.args)  # Handle names that contain spaces

    try:
        await update.message.reply_text('Processing...')
        res = requests.post(
            f'https://add-admin-qbfqiotlpa-uc.a.run.app/?callsign={callsign}')
        res.raise_for_status()
        await update.message.reply_text(f'Added user {callsign} as admin')
    except Exception as error:
        await update.message.reply_text(f'Error adding admin: {error}')


# Remove admin by their callsign
async def remove_admin(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide the callsign/name of the admin to be demoted\n\ne.g. /remove_admin GLENN")
        return

    callsign = ('_').join(context.args)  # Handle names that contain spaces

    try:
        await update.message.reply_text('Processing...')
        res = requests.delete(
            f'https://remove-admin-qbfqiotlpa-uc.a.run.app/?callsign={callsign}')
        res.raise_for_status()
        await update.message.reply_text('Removed admin')

    except requests.exceptions.HTTPError as error:
        await update.message.reply_text(f'Error removing admin: {error.response.text}')
    except Exception as error:
        await update.message.reply_text(f'Error removing admin: {error}')


# Remove user by their callsign: /remove_user GLENN
async def remove_user(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide the callsign or name of the user to be removed\n\ne.g. /remove_user GLENN")
        return

    callsign = ('_').join(context.args)  # Handle names that contain spaces

    try:
        await update.message.reply_text('Processing...')
        res = requests.delete(
            f'https://remove-user-qbfqiotlpa-uc.a.run.app/?callsign={callsign}')
        res.raise_for_status()
        await update.message.reply_text(f"Removed {res.json()['callsign']}. They will no longer receive notifications from this bot.")

    except requests.exceptions.HTTPError as error:
        await update.message.reply_text(f'Error removing user: {error.response.text}')
    except Exception as error:
        await update.message.reply_text(f'Error removing user: {error}')


# Register self with callsign
async def register(update: Update, context: CallbackContext):
    if len(context.args) == 0:  # No argument provided
        await update.message.reply_text("Please provide your callsign or name\n\ne.g. /register GLENN")
        return

    user_id = update.effective_user.id
    # Handle names that contain spaces
    callsign = (' ').join(context.args)

    try:
        await update.message.reply_text('Processing...')
        res = requests.post(
            f'https://register-qbfqiotlpa-uc.a.run.app/?userId={user_id}&callsign={callsign}')
        res.raise_for_status()
        await update.message.reply_text(f"Successfully registered! You will begin receiving notifications from this bot.")

    except requests.exceptions.HTTPError as error:
        await update.message.reply_text(f'Error registering: {error.response.text}')
    except Exception as error:
        # Send user-friendly error message
        await update.message.reply_text(f'Error registering: {error}')


# Unregister self
async def unregister(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    try:
        await update.message.reply_text('Processing...')
        res = requests.delete(
            f'https://unregister-qbfqiotlpa-uc.a.run.app/?userId={user_id}')
        res.raise_for_status()
        await update.message.reply_text('Successfully unregistered. You will no longer receive notifications from this bot.')

    except requests.exceptions.HTTPError as error:
        await update.message.reply_text(f'Error unregistering: {error.response.text}')
    except Exception as error:
        await update.message.reply_text(f'Error unregistering: {error}')


# Get list of users
async def get_users(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text('Fetching data...')
        res = requests.get('https://get-users-qbfqiotlpa-uc.a.run.app')
        users = res.json()
        formatted_users = ('\n').join([user['callsign'] for user in users])
        await update.message.reply_text(formatted_users)
    except Exception as error:
        await update.message.reply_text(f'Error getting users: {error}')


# Get list of admins
async def get_admins(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text('Fetching data...')
        res = requests.get('https://get-admins-qbfqiotlpa-uc.a.run.app')
        admins = res.json()
        formatted_admins = ('\n').join([admin['userId'] for admin in admins])
        await update.message.reply_text(formatted_admins)
    except Exception as error:
        await update.message.reply_text(f'Error getting admins: {error}')

# Get own user_id


async def get_id(update: Update, context: CallbackContext):
    await update.message.reply_text(update.effective_user.id)

# Show list of commands


async def help(update: Update, context: CallbackContext):
    help_text = ""
    await update.message.reply_text(f"")
