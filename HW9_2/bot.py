import telebot
from tic_tac_toe import game
from calc import model_racional as mr
import log_generate as lg

bot = telebot.TeleBot('TOKEN')
chat_id = ''
dic = {}

@bot.message_handler(commands=['start'])
def start(message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'Я знаю 3 слова, 3 волшебных слова:\n'
                                      'поиграем\nпосчитаем\nпомощь')
    bot.send_message(message.chat.id, f'Прошу выбрать')

@bot.message_handler(commands=['help'])
def help(message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_message(chat_id, 'Выбери:\n'
                              '/start - команда приветствия\n'
                              'поиграем - игра в крестики-нолики;\n'
                              'посичитаем - посчитаю примеры в одну строку;\n'
                              '/help - вывод команд;')

@bot.message_handler()
def get_user_text(message):  
    lg.write_data(f'Бот получил команду "{message.text}"')
    mes = message
    global chat_id
    chat_id = mes.chat.id
    if mes.text.lower() == 'поиграем':
        bot.send_message(chat_id, 'Давай играть в крестики-нолики! Будешь ходить первым?')
        lg.write_data(f'Начинается игра')
        global dic
        dic = {'1': '.', '2': '.', '3': '.', '4': '.', '5': '.', '6': '.', '7': '.', '8': '.', '9': '.'}
        lg.write_data(f'Словарь заполнен точками')
        bot.register_next_step_handler(mes, start_game)
    elif mes.text.lower() == 'посчитаем':
        bot.send_message(chat_id, 'Хорошо! Вводи пример!')
        lg.write_data(f'Получаем пример для решения')
        bot.register_next_step_handler(mes, count_example)
    else:
        lg.write_data(f'Зафиксирована неизвестная команда')
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Воспользуйся командой "/help"!')

def start_game(message):  
    if message.text == 'да':
        lg.write_data(f'Пользователь принял решение ходить первым')
        bot.send_message(chat_id, 'Выбери клетку!')
        bot.register_next_step_handler(message, user_check)
    elif message.text == 'нет':
        lg.write_data(f'Бот ходит первым')
        bot.send_message(chat_id, 'Хорошо, я начинаю!')
        pc_check()
    else:
        lg.write_data(f'В функции определения хода зафиксирована неизвестная команда "{message.text}"')
        bot.send_message(chat_id, 'Я тебя не пониманию! Скажи еще раз!')
        bot.register_next_step_handler(message, start_game)

def user_check(message):  
    global dic
    lg.write_data(f'Начался ход пользователя')
    player_turn = message.text
    if player_turn in ('1', '2', '3', '4', '5', '6', '7', '8', '9') and dic.get(player_turn) == '.':
        dic[player_turn] = 'x'
        lg.write_data(f'Пользователь выбрал клетку: {player_turn}')
        if game.check_winner(dic):
            lg.write_data(f'Пользователь победил в игре')
            bot.send_message(chat_id, 'Ты выиграл!')
        elif '.' not in dic.values():
            lg.write_data(f'Игра завершилась ничьей')
            bot.send_message(chat_id, 'Ой у нас ничья!')
        else:
            bot.send_message(chat_id, game.print_dic(dic))
            pc_check()
    else:
        lg.write_data(f'На ходе пользователя зафиксирован не корректный ввод: {player_turn}')
        bot.send_message(chat_id, 'Ты что-то не то ввел! Попробуй еще раз!')
        bot.register_next_step_handler(message, user_check)

def pc_check():  
    global dic
    lg.write_data(f'Начался ход бота')
    bot.send_message(chat_id, 'Мой ход:')
    bot_choice = game.pc_choice(dic)
    lg.write_data(f'Бот выбирает клетку {bot_choice}')
    dic[bot_choice] = '0'
    bot.send_message(chat_id, game.print_dic(dic))
    if game.check_winner(dic):
        lg.write_data(f'Бот победил в игре')
        bot.send_message(chat_id, 'Я победил!')
    elif '.' not in dic.values():
        lg.write_data(f'Игра завершилась ничьей')
        bot.send_message(chat_id, 'Ой у нас ничья!')
    else:
        message = bot.send_message(chat_id, 'Твой ход!')
        bot.register_next_step_handler(message, user_check)

def count_example(message):  
    example, example_list = mr.get_nums(message.text)
    lg.write_data(f'Пользователь ввел пример: {example}')
    result = mr.get_result(example_list)
    lg.write_data(f'Получен ответ: {result}')
    bot.send_message(chat_id, f'{example} = {result}')

def start_bot():
    print('Сервер запущен')
    bot.polling(none_stop=True)