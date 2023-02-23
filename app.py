import telebot
from config import keys, TOKEN
from extentions import ConvertionException, Converter


bot = telebot.TeleBot(TOKEN)


#Output of the </start> and </help> commands and their description
@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message) -> None:
    text: str = ''' 
    Чтобы начать работу введите команду в следующем формате: 
    \n<рубль> <доллар>  <1>
    \nСписок всех доступных валют: /values
    '''
    bot.reply_to(message, text)


#Output of the </values> command and its description
@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message) -> None:
    text: str = 'Доступные валюты:'
    for key in keys.keys():
        text: str = '\n'.join((text, key, ))
    bot.reply_to(message, text)


#Output of currency conversion and a list of errors and their description
@bot.message_handler(content_types = ['text', ])
def convert(message: telebot.types.Message) -> None:
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Параметров больше, чем заявлено(/help).')

        if len(values) < 3:
            raise ConvertionException('Недостаточно папаметров.(/help).')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n{e}(/help)."
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n{e}(/help)."
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}."
        bot.send_message(message.chat.id, text)


bot.polling()
