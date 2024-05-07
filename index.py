import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv, find_dotenv
from ai import answer


# Load the .env file
_ = load_dotenv(find_dotenv()) # read local .env file

key = os.environ['BOT_API_KEY']

# Commands
async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, How may I help you today?")


async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help is coming soon")


# Responses
def handle_responses(text:str)->str:
    res = answer.qa(text) 
    print(f'AI response: {str(res["answer"])}')
    return f'{res["answer"]}'

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = handle_responses(text)
    await update.message.reply_text(response)

    
async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

  
if __name__ == "__main__":
    print("Starting Bot")
    app = Application.builder().token(key).build()
    
    # Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=2)
    
    
    
    """
        message_type = update.message.chat.type
    text = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}')
    if message_type == "group":
        if "BOT_USERNAME" in text:
            new_text = text.replace("BOT_USERNAME","").strip()
            response = handle_responses(new_text)
        else:
            return   
    else: 
        response = handle_responses(text)
    print('Bot: ',response)
    """