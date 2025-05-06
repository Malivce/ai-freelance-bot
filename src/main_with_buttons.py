
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Temporary variable to hold user state (for code input)
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Generate Unit Tests", callback_data="generate_tests")],
        [InlineKeyboardButton("Explain Code", callback_data="explain_code")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("What would you like to do?", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "generate_tests":
        user_state[query.from_user.id] = "awaiting_code_for_tests"
        await query.edit_message_text("Please send me the code you want to generate unit tests for.")
    elif query.data == "explain_code":
        user_state[query.from_user.id] = "awaiting_code_for_explanation"
        await query.edit_message_text("Please send me the code you want me to explain.")

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    code = update.message.text

    if user_id not in user_state:
        await update.message.reply_text("Please choose an action using /start.")
        return

    task = user_state.pop(user_id)

    if task == "awaiting_code_for_tests":
        # Placeholder logic, replace with GPT integration
        await update.message.reply_text("Generating unit tests for your code...

(Example response)")
    elif task == "awaiting_code_for_explanation":
        await update.message.reply_text("Explaining your code...

(Example explanation)")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    print("Bot is running...")
    app.run_polling()
