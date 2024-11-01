import telebot
import requests

bot = telebot.TeleBot('тут API tg бота')
API = 'API сайта openweathermap.org'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название города, чтобы узнать погоду.')


@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    if res.status_code == 200:
        data = res.json()
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']

        response = (f'Погода в {city.title()}:\nТемпература: {temp}°C\nОщущается как: {feels_like}°C')
        bot.reply_to(message, response)

        gif = None
        if temp <= 0:
            gif = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2x4NTkwZGRtaW5hcnpydm5ic3Z3MXB2NHRrMzh1aDdqdDRwMmpyeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/s4Bi420mMDRBK/giphy.gif'
        elif temp >= 25:
            gif = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzRpdmFyN2cycTB1czU3eHA5NmkwaTc5MjZvYW5sMHE0d3IzcTkzNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/B0yHMGZZLbBxS/giphy.gif'
        else:
            gif = 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExYzkwOXIwYTdmbmpnOGs1OXNpMWppOHp3OGhmOHNpYjM1b25jdDE5NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9dg/ItsDcVrtzYeBbiERKb/giphy.gif'

        if gif:
            bot.send_animation(message.chat.id, gif)
    else:
        bot.reply_to(message, 'Город указан неверно')


bot.polling(non_stop=True)