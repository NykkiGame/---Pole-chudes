import telebot
import random
bot = telebot.TeleBot("Your_bot_toket") # Создание переменной для работы с ботом
with open('one.txt', mode = 'r', encoding = 'UTF-8') as file: #Слова для случайного угадывания
    words = file.read().split()
'''lives = 6
pods = 0
flag = False'''
markup = telebot.types.ReplyKeyboardMarkup()
byk = 'ёйцукенгшщзхъфывапролджэячсмитьбю'
users = {}
res = []
for i in byk: # Создание клавиатуры 
    res.append(telebot.types.KeyboardButton(i))
markup.row(*res[1:13])
markup.row(*res[13:24])
markup.row(*res[24:34], res[0])
       
def Update_progress(byk, id):  # Создание функции
    global users
    slovo = users[id][3]
    print(users[id][4])  # Выводит список вопросов
    for i in range(0, len(slovo)):  # Перебирает числа с нуля до количества букв в слове
        if slovo[i].lower() == byk:  # Проверка совподают ли буквы
            users[id][4][i] = byk #Заменяет вопрос на нужную букву который написал пользователь

@bot.message_handler(commands=['start']) #Добавление команды старт
def start(message): # создание функции 
            global users
            bot.send_message(message.chat.id, 'Здравствуй! Ты на игре в которой можеш получить А-а-автомобиль!')
            word = random.choice(words)
            progress = ["❔"] * len(word)
            print([word])
            bot.send_message(message.chat.id, 'Ваша буква ? ' + " ".join(progress), reply_markup=markup)  
            flag = True
            lives = 6
            pods = 0
            id = message.chat.id
            users[id] = [flag, pods, lives, word, progress]
@bot.message_handler(commands=['help'])
def help(message):
    rules = (
        "Правила игры 'Поле чудес с Некитом':\n"
        "1. Я читаю слово из словаря динозавров.\n"
        "4. У тебя 6 попыток.\n"
        "3. Если ты угадаешь все буквы в слове, ты получишь А-а-автомобиль!\n"
        "4. Если ты не угадал моё древнее слово, то тебя выганят из студии.\n"
        "5. Начнём игру?")
    bot.send_message(message.chat.id, rules)

@bot.message_handler(commands=['statistics'])
def stap(message):
    with open('Polewin.txt', 'r', encoding = 'UTF-8') as file:
        s = file.read().split('\n')
    win = 0
    defeat = 0
    id = message.chat.id
    for i in range(len(s)):        
        s[i] = s[i].split()
        print(s[i])
        try:
            if id == int(s[i][0]):
                if s[i][2] == 'defeat':
                    defeat += 1
                else:
                    win += 1  
        except:
            pass
    bot.send_message(id, f'Статистика {message.chat.username}\nПобед: {win}\nПоражений: {defeat}')

@bot.message_handler(content_types=['text', 'document', 'audio'])
def get(message):  
    global users
    id = message.chat.id  
    text = message.text   

    if id not in users or users[id][0] == False:
        if text == 'Начать' or text == 'Играть' or text == 'Старт' or text == 'начать' or text == 'играть' or text == 'старт':  
            '''bot.send_message(message.chat.id, 'Здравствуй! Ты на игре, в которой можешь получить А-а-автомобиль!')
            word = random.choice(words)
            print(word)
            progress = ["❔"] * len(word)
            bot.send_message(message.chat.id, 'Ваша буква ? ' + " ".join(progress))  
            flag = True'''
            start(message)
        elif text == 'мем' or text == 'Мем':
            bot.send_message(message.chat.id, 'Тито фредди фазбер? Ау Ау Ау АУ')
        else:  
            bot.send_message(message.chat.id, 'Введите Начать, Играть, Старт, чтобы выиграть Аавтомобиииииииииииииииииииииль ❕')  
    else:  
        if text.lower() in users[id][3].lower():  
            Update_progress(text.lower(), id)  
            bot.send_message(message.chat.id, 'Угадал! ' + " ".join(users[id][4]))  
            if "❔" not in users[id][4]:
                photo = open("terki.jpg",mode="rb")
                bot.send_photo(message.chat.id, photo)
                photo.close()
                bot.send_message(message.chat.id, 'Поздравляю! Якубович похлопал вам по плечю вам не выдал автомобиль и вы ушли только с тёркой от телеканала Leomax и потерянным временем !')  
                users[id][0] = False
                with open('two.txt', 'a', encoding = 'UTF-8') as file:
                    print(id, message.from_user.username, 'win', file = file)  
                users[id][2] = 6
                users[id][1] = 0  
        else:
            keb1 = telebot.types.InlineKeyboardMarkup()
            pod = telebot.types.InlineKeyboardButton('Раскрытие буквы ', callback_data='pod')# callback_data - сообщение которое передаёт обработчику нажатий
            keb1.add(pod)
            users[id][2] -= 1  
            bot.send_message(message.chat.id, 'Ты не угадал, осталось жизней: ' + str((users[id][2])), reply_markup = keb1)  
            if users[id][2] == 0:
                photo = open("param_param.jpg",mode="rb")
                bot.send_photo(message.chat.id, photo)
                photo.close()
                bot.send_message(message.chat.id, 'Ты проиграли! Слово, которое я прочитал из словаря динозавров, было: ' + users[id][3])  
                users[id][0] = False
                with open('two.txt', 'a', encoding = 'UTF-8') as file:
                    print(id, message.from_user.username, 'defeat', file = file)  
                users[id][2] = 6
                users[id][1] = 0  
@bot.callback_query_handler(func = lambda a: True)
def keypress(callback):
        global users
        id = callback.message.chat.id
        if callback.data == 'pod':    
            if users[id][1] < 3:  
                users[id][1] += 1
                index = 0
                while users[id][4][index] == users[id][3][index]:
                    index += 1
                users[id][4][index] = users[id][3][index]
                bot.send_message(callback.message.chat.id, ' '.join(users[id][4]))
            else:
                bot.send_message(callback.message.chat.id, 'Ну всё ! подсказки от ЕГЭ ОГЭ и ВПР закончились 😊.')
bot.polling(none_stop=True, interval=0)