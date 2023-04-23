import telebot

bot = telebot.TeleBot("6221500469:AAFIqA5fAn-iqVKd8vz0oPCXQ8CuKuP9Qek")
users = []
@bot.message_handler(commands=['start'])
def add_user(message):
    users.append(message.chat.id)
    print(users)
bot.polling()

def get_users():
    return users