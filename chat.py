from decouple import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Configuration
CHAT_ID = config('CHAT_ID')
TOKEN = config('TOKEN')


def start(update, context):
    text = 'Hello {}'.format(update.message.from_user.first_name)
    update.message.reply_text(text)
    return ConversationHandler.END


def contact(update, context):
    update.message.reply_text('Ok, send your question please.')
    return 1


def forward(update, context):
    update.message.forward(chat_id=CHAT_ID)


def answer(update, context):
    context.bot.send_message(
        chat_id=update.message.reply_to_message.forward_from.id,
        text=update.message.text
    )


def help_contact(update, context):
    update.message.reply_text('{} caso queria falar conosco favar use o comando /contact antes.'.format(
        update.message.from_user.first_name))


updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(ConversationHandler(
    entry_points=[CommandHandler('contact', contact)],
    states={1: [MessageHandler(Filters.text, forward)], },
    fallbacks=[CommandHandler('start', start)]))

dp.add_handler(CommandHandler(['hello', 'start'], start))

dp.add_handler(MessageHandler(Filters.reply, answer))
dp.add_handler(MessageHandler(Filters.update, help_contact))

updater.start_polling()
updater.idle()
