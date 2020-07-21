import logging, json, requests
import face_recognition

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
 
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
 
logger = logging.getLogger(__name__)
 
REGISTRATION, NAME, LAST_NAME,PHONE_NUMBER, PHOTO, = range(5)
 
 
def start(update, context):
    reply_keyboard = [['Registration'], ['Cancel']]
 
    update.message.reply_text(
        "Let's start registration\n",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
 
    return REGISTRATION
 
 
def registration(update, context):
    user = update.message.text
    update.message.reply_text('Please tell me your name', reply_markup=ReplyKeyboardRemove())
    return NAME

def name(update, context):
    text = update.message.text
    context.user_data['first_name'] = text
    print(text)
    update.message.reply_text('Please tell me your last name')
    return LAST_NAME

def last_name(update, context):
    text = update.message.text
    print(text)
    context.user_data['last_name'] = text
    update.message.reply_text('What is your phone number?')
    return PHONE_NUMBER

def phone_number(update, context):
    text = update.message.text
    context.user_data['phone_number'] = text
    print(text)
    update.message.reply_text('Send me your photo')
    return PHOTO
 
def photo(update, context):
    user = update.message.text
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    img = face_recognition.load_image_file('user_photo.jpg')
    new_face_encodings = face_recognition.face_encodings(img)
    new_list = new_face_encodings[0].tolist()
    context.user_data['encoding'] = new_list
    print(context.user_data)
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')
    user_json = json.dumps(context.user_data, ensure_ascii=False).encode('utf-8')
    new_user = requests.post('http://127.0.0.1:5000/users/', data=user_json, headers={'Content-type':'application/json'})
    return ConversationHandler.END
 
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')
 
    return ConversationHandler.END
 
 
def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("998724587:AAELHoAk_Py_zus2a8m7L-fBOzU-YG6bqnA", use_context=True)
 
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
 
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
 
        states={
            REGISTRATION: [MessageHandler(Filters.regex('^(Registration)$'), registration)],

            NAME: [MessageHandler(Filters.text, name)],

            LAST_NAME: [MessageHandler(Filters.text, last_name)],

            PHONE_NUMBER: [MessageHandler(Filters.text, phone_number)],
 
            PHOTO: [MessageHandler(Filters.photo, photo)]
        },
 
        fallbacks=[MessageHandler(Filters.regex('^(Cancel)$'), cancel)],
    )
 
    dp.add_handler(conv_handler)
 
    # Start the Bot
    updater.start_polling()
 
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
 
 
if __name__ == '__main__':
    main()

