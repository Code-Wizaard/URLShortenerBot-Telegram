import telebot

file = open('users.txt')
bot = telebot.TeleBot('7139867598:AAHKYg6teWZroRFPvoDhwGJ8fuxm6lEKYfA')

users = file.read().splitlines()
def send_message():
    for user in users:
        bot.send_message(user, 'اطلاعیه شماره ی دو برای تست بعدی')

if __name__ == '__main__':
    bot.polling()
    send_message()