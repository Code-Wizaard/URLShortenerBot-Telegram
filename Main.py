import requests
import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'سلام، به ربات کوتاه کننده ی لینک خوش امدید \n شما میتونید با فرستادن دستور /short لینک مورد نظر خودتون رو کوتاه کنید')

@bot.message_handler(commands=['short'])
def get_link(message):
    bot.send_message(message.chat.id, 'لینک مورد نظر خودتون رو ارسال کنید')
    bot.register_next_step_handler(message, short_link)
def short_link(message):
    link = message.text
    bot.send_message(message.chat.id, 'در حال پردازش... لطفا صبر کنید')
    apiparams = {'api':'a36a01f0f9268f4ac5aa7232f661182d0cb6828c', 'url':link}
    apiurl = 'https://1da.ir/api'
    r = requests.get(url=apiurl, params=apiparams)
    res = r.json()
    if res['status'] == 'success':
        log = open('log.txt', 'a')
        log.write(f'user id : {message.chat.id}, shorted the link : {link} into {res['shortenedUrl']} \n')
        bot.send_message(message.chat.id, 'لینک کوتاه شده : '+res['shortenedUrl'])
        bot.send_message(message.chat.id, 'ساخته شده توسط گروه برنامه نویسی علاءالدین \n Site : sacgroup.ir \n Telegram : @AladdinBots \n Bale : [@AladdinBots](https://ble.ir/aladdinbots) \n UrlShortenerBot v1.2 created with ♥ by [SACGroup](https://sacgroup.ir)', parse_mode='Markdown', disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, 'خطا در کوتاه کردن لینک')

@bot.message_handler(commands=['helpme'])
def get_message(message):
    bot.reply_to(message, 'لطفا مشکل خودتون رو در قالب یک پیام ارسال کنید تا به گروه پشتیبانی فنی ربات ارسال شود')
    bot.register_next_step_handler(message, helpme)
def helpme(message):
    bot.send_message(message.chat.id, 'در حال ارسال پیام شما به تیم پشتیبانی... لطفا منتظر بمانید')
    bot.send_message((YOUR_CHAT_ID), f'سلام @(USERNAME) \n این پیام به عنوان مشکلی برای ربات URLShortenerBot به تو ارسال شده است \n User id : {message.chat.id}')
    bot.forward_message(chat_id=6326221369, from_chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id, 'پیام ارسال شد. تیم پشتیبانی بعد از پیگیری مشکل به شما اطلاع خواهند داد')

@bot.message_handler(commands=['donate'])
def donate(message):
    bot.send_message(message.chat.id, '(پیام برای دونیت، هر چیزی که خودتان میخواهید جایگزاری کنید)')


@bot.message_handler(commands=['notif'])
def notif(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('بله', request_contact=True)
    item2 = types.KeyboardButton('خیر')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'ایا میخواهید از تمامی اپدیت ها و اخبار ربات مطلع شوید؟ در صورتی که بر روی <بله> کلیک کنید پیامی حاوی یوزرنیم شما برای ارسال اخبار به ربات ارسال میشود', reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def adduser(message):
    markup = types.ReplyKeyboardRemove(selective=False)

    if message.contact:

        bot.send_message(message.chat.id, 'در حال ارسال یوزرنیم شما به ربات... لطفا منتظر بمانید')

        with open('users.txt') as file:
            users = file.readlines()

        if str(message.contact.user_id) in users:
            file = open('users.txt', 'a')
            file.write(f'{message.contact.user_id}\n')
            file.close()
            bot.send_message(message.chat.id, 'یوزرنیم شما در پایگاه داده ربات ثبت شد\n از الان به بعد تمامی اپدیت ها و اطلاعیه های ربات به شما هم ارسال خواهد شد', reply_markup=markup)
        
        else:
            bot.send_message(message.chat.id, 'یوزرنیم شما قبلا در ربات ذخیره شده\n در صورتی که میخواهید از لیست خبرنامه حذف شوید با پشتیبانی تماس بگیرید', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'خطا در ارسال یوزرنیم شما به ربات', reply_markup=markup)
    
@bot.message_handler(func=lambda message:True)
def getmessage(message):
    if message.text == 'خیر':
        bot.send_message(message.chat.id, 'در حال لغو ثبت یوزرنیم شما...')
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'فرآیند لغو ثبت یوزرنیم شما با موفقیت انجام شد', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'ببخشید ، متوجه منظورتان نشدم')

if  __name__ == '__main__':
    bot.polling(non_stop=True)
