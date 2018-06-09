import config
import telebot
import requests

# Создаём переменную с ботом
bot = telebot.TeleBot(config.token)

# Определяем, была ли введена команда Загуглить
is_google = False


@bot.message_handler(commands=["start"])
def handle_start(message):
    '''Выполняется при команде /start'''

    text = '''
        Добро пожаловать! Данный бот умеет выполнять различные операции. Выберите операцию из списка ниже.
    '''
    text_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    text_markup.row(*config.buttons)
    bot.send_message(message.from_user.id, text, reply_markup=text_markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    '''Выполняется при вводе любого текста'''

    global is_google

    # Если был введён запрос для поиска
    if is_google:
        is_google = False
        query = message.text.replace(" ", "+")
        href = '''https://www.google.com.ua/search?q={0}'''.format(query)
        link = '''<a href="{0}">Открыть в Google</a>'''.format(href)

        bot.send_message(message.from_user.id, link, parse_mode="HTML")

    # Если был выбран пункт Загуглить
    elif message.text == config.text_for_google:
        is_google = True
        text = "Введите запрос:"

        bot.send_message(message.from_user.id, text)

    # Если был выбран пункт Курсы валют
    elif message.text == config.text_for_currencies:
        coins = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0')
        global_data = requests.get('https://api.coinmarketcap.com/v1/global/')
        text = ""

        for coin in coins.json():
            if coin["id"] in config.currencies:
                if coin["id"] == "bitcoin":
                    btc_price = round(float(coin["price_usd"]))
                    text += "<b>{0}: {1}$ </b> \n".format(coin["name"], btc_price)
                else:
                    alt_price = round(float(coin["price_usd"]), 2)
                    text += "{0}: {1}$ - ₿ {2}\n".format(coin["name"], alt_price, coin["price_btc"])

        total_cap = global_data.json()["total_market_cap_usd"]
        text += "\nКапитализация: {0} млрд".format(str(total_cap)[:3])

        bot.send_message(message.from_user.id, text, parse_mode="HTML")

    # Если введена неизвестная команда
    else:
        bot.send_message(message.from_user.id, "Неизвестная команда!")


bot.polling(none_stop=True)
