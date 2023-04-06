from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

# Enable logging
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Function to start the bot and display the main menu
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Coffee-to-Water Ratios", callback_data="ratios")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to the Coffee Recipe Bot! Choose an option:", reply_markup=reply_markup)

# Function to handle button callbacks
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "ratios":
        ratios_menu(update, context)

# Function to display the ratios menu
def ratios_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.edit_message_text("Please enter the brewing method and the amount of coffee (in grams) or water (in milliliters) you have, separated by a space (e.g., 'v60 15'):")
    context.user_data["awaiting_amount"] = True

# Function to handle user input for brewing method and amount
def handle_amount(update: Update, context: CallbackContext):
    # Define coffee-to-water ratios for different brewing methods
    ratios = {
        "aeropress": 6,
        "french_press": 12,
        "v60": 50/3,
        "chemex": 17,
        "moka_pot": 10,
        "cold_brew": 40/9,
        "siphon": 50/3,
        "espresso": 2
    }

    # Split user input into brewing method and amount
    method, amount = update.message.text.split()
    amount = float(amount)

    # Check if the provided brewing method is valid
    if method not in ratios:
        update.message.reply_text("Invalid brewing method. Please choose from aeropress, french_press, v60, chemex, moka_pot, cold_brew, siphon, or espresso.")
        return

    # Retrieve the corresponding coffee-to-water ratio from the dictionary
    ratio = ratios[method]

    # Calculate the required coffee or water amount based on the user's input
    if amount > 0:
        if amount <= 100:  # Assume the input is coffee amount (in grams)
            water_amount = amount * ratio
            update.message.reply_text(
                f"With {amount}g of coffee using the {method} method, you need {water_amount}ml of water. (Ratio: 1:{ratio})"
            )
        else:  # Assume the input is water amount (in milliliters)
            coffee_amount = amount / ratio
            update.message.reply_text(
                f"With {amount}ml of water using the {method} method, you need {coffee_amount}g of coffee. (Ratio: 1:{ratio})"
            )
    else:
        update.message.reply_text("Invalid amount. Please enter a positive number.")

    context.user_data["awaiting_amount"] = False

# Main function to
def main():
    # Create the Updater and pass it your bot's token
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers for start and button callbacks
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Register handler for user input
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_amount))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()