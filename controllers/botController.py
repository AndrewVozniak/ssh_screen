import telebot

from config import bot_config, system_data

bot = telebot.TeleBot(bot_config['token'])
ssh_controller = None


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


def send_message_to_all_users(message):
    bot.send_message(bot_config['user_id'], message)


def start_bot():
    print('Bot started')
    bot.polling(none_stop=True)
