import telebot
from config import bot_config, system_data

bot = None


def send_message_to_all_users(message):
    if bot_config['user_id'] is not None:
        bot.send_message(bot_config['user_id'], message)

    else:
        print('User id is None')


def start_bot():
    global bot
    bot = telebot.TeleBot(bot_config['token'])

    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        if message.from_user.id == bot_config['user_id']:
            bot.send_message(message.chat.id, 'You are already subscribed')
            bot.send_message(message.chat.id, system_data['last_message'])

        else:
            if message.text == bot_config['secret_phrase']:
                bot_config['user_id'] = message.from_user.id
                bot.send_message(message.chat.id, 'You have successfully subscribed')
                bot.send_message(message.chat.id, system_data['last_message'])

            else:
                bot.send_message(message.chat.id, 'Wrong secret phrase')

    print('Bot started')
    bot.polling(none_stop=True)
