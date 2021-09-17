import logging
import ephem
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
logging.basicConfig(filename='bot.log', level=logging.INFO)
PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}

today = '2021/08/30'
planets = {'Mars': ephem.Mars(today), 'Venus': ephem.Venus(today), 'Saturn': ephem.Saturn(today), 'Jupiter': ephem.Jupiter(today),
               'Neptune': ephem.Neptune(today), 'Uranus': ephem.Uranus(today), 'Mercury': ephem.Mercury(today)}

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь!')   

def planet_user(update, context):   
    user_planet=update.message.text.split()[1]
    planets_LP = planets.get(user_planet, None)
    if planets_LP != None:
        constellation = ephem.constellation(planets[user_planet])
        update.message.reply_text(constellation[1])
    else:
        update.message.reply_text('Ошибка ввода')
    
def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("Learn", greet_user))
    dp.add_handler(CommandHandler("Planet", planet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()



if __name__ == "__main__":
    main()