import config
import telebot
from telebot import types, TeleBot  # кнопки
from string import Template

bot: TeleBot = telebot.TeleBot(config.token)

user_dict = {}
STEP = 0


class User:
    def __init__(self, city):
        self.city = city



    keys = ['fullname', 'phone', 'city', 'data', 'address', 'things',]
    for key in keys:
        key = None

@bot.message_handler(content_types='text')
def work(message):
    print('def work')
    if message.text == '/start':
        send_welcome(message)
    elif message.text == 'about us':
        send_about(message)
    elif message.text == 'register':
        user_reg(message)
    elif message.text == 'phone':
        user_reg(message)
    elif message.text == 'data':
        user_reg(message)
    elif message.text == 'address':
        user_reg(message)
    elif message.text == 'things':
        user_reg(message)
    elif message.text == 'application':
        user_reg(message)

# если /help, /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
        print('def welcome')
        bot.send_message(message.chat.id, bot.send_photo(message.chat.id, "https://classpic.ru/blog/muravej-foto.html/chyornyj-sadovyj-muravej"))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('about us')
        itembtn2 = types.KeyboardButton('application')

        markup.add(itembtn1, itembtn2)

        bot.send_message(message.chat.id, "Приветствуем ! "
                         + message.from_user.first_name
                         + ", я бот-ассистент, чем могу помочь?", reply_markup=markup)


# /о компании
@bot.message_handler(content_types=["text"])
def send_about(message):
        print('def send_about')
        bot.send_message(message.chat.id, "Квартирный и офисные переезды под ключ, грузчики - виртуозы"
                         + " переезд без нервов в короткие сроки")
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Перейти на сайт", url="https://murawei.by/"))
        bot.send_message(message.chat.id,
                     "Нажмите на кнопку и узнайте о нас больше", parse_mode='html', reply_markup=markup)


# / регистрация
@bot.message_handler(content_types=["text"])
def user_reg(message):
    print('def user_reg')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Минск')
    itembtn2 = types.KeyboardButton('Брест')
    itembtn3 = types.KeyboardButton('Гомель')
    itembtn4 = types.KeyboardButton('Могилев')
    itembtn5 = types.KeyboardButton('Витебск')
    itembtn6 = types.KeyboardButton('Гродно')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

    msg = bot.send_message(message.chat.id, 'Ваш город?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    print('def process_city_step')
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Фамилия Имя Отчество', reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message, 'Ой!')


def process_fullname_step(message):
    print('def process_fullname_step')
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Ваш номер телефона в формате 029ххххххх', reply_markup=markup)
        bot.register_next_step_handler(msg, process_phone_number)

    except Exception as e:
        bot.reply_to(message, 'Ой!')

def process_phone_number(message):
    print('def process_phone_step')

    try:
        int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Когда планируете переезд? Дата переезда\nВ формате: день/месяц/год')
        bot.register_next_step_handler(msg, process_data_step)

    except Exception as e:
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        bot.register_next_step_handler(msg, process_data_step)




def process_data_step(message):
    print('def process_data_step')
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.data = message.text

        msg = bot.send_message(chat_id, 'От куда и куда перевозим?')
        bot.register_next_step_handler(msg, process_address_step)
    except Exception as e:
        bot.reply_to(message, 'Ой!')
        bot.register_next_step_handler(msg, process_address_step)


def process_address_step(message):
    print('def process_address_step')
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.data = message.text

        msg = bot.send_message(chat_id, 'Крупные вещи будут?')
        bot.register_next_step_handler(msg, process_things)

    except Exception as e:
        bot.reply_to(message, 'Ой!')
        bot.register_next_step_handler(msg, process_things)


# крупные вещи
@bot.message_handler(content_types=["text"])
def process_things(message):
    print('def process_things')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Холодильник стандартный')
    itembtn2 = types.KeyboardButton('Холодильник Сайд-Бай-Сайд')
    itembtn3 = types.KeyboardButton('Диван')
    itembtn4 = types.KeyboardButton('Кровать')
    itembtn5 = types.KeyboardButton('Стиральная машина')
    itembtn6 = types.KeyboardButton('Комод')
    itembtn7 = types.KeyboardButton('Дальше')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)



    msg = bot.send_message(message.chat.id, 'Будут такие вещи?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_application_step)


def process_application_step(message):
    print('def process_c')
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.application = message.text
    except Exception as e:
        bot.reply_to(message, 'Ой!')

    bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")
    # отправить в группу
    bot.send_message(config.chat_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")

    # формируем вид заявки


def getRegData(user, title, name):
    print('def getRegData')
    t = Template(
        '$title *$name* \n Город:*$userCity* \n ФИО:*$fullname* \n Телефон:*$phone_number* \n Дата переезда: *$data* \n От куда и куда: *$address* \n Крупные вещи:*$things*')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        'phone_number': user.phone,
        'data': user.data,
        'address': user.address,
        'things': user.things
    })


bot.polling(none_stop=True, interval=0)
