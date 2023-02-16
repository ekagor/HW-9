import log_generate as lg

book = {1: {'surname': 'Петров', 'name': 'Иван', 'patronymic': 'Федорович', 'email': '13576@gmail.com',
            'telephone': '+7-905-047-40-25'},
        2: {'surname': 'Тырыжкин', 'name': 'Альяс', 'patronymic': 'Харитович', 'email': '3636@mail.ru',
            'telephone': '+7-905-123-57-70'}}

def find_in_book(text): 
    global book
    f_choice = text
    choice_list = list()
    for key in book:
        if f_choice in book[key].values():
            choice_list.append(' '.join(book[key].values()))
    if len(choice_list) == 0:
        return False
    else:
        return '\n'.join(choice_list)

def add_contact(surname, name, patronymic, email_address, telephone):  
    global book
    book[len(book) + 1] = dict(zip(['surname', 'name', 'patronymic', 'email', 'telephone'],
                                   [surname, name, patronymic, email_address, telephone]))
    lg.write_data('Запись внесена;')
    return True


def print_book(): 
    global book
    text = ''
    for key in book:
        text += str(key) + ' - ' + ' '.join(book[key].values()) + '\n'
    return text


def import_base(file): 
    with open(file, encoding='utf-8') as file_b:
        base = [str(el).split(';') for el in file_b.readlines()]
    lg.write_data('Справочник будет импортирован;')
    for i in range(len(base)):
        base[i][0] = int(base[i][0])
        base[i][-1] = base[i][-1].rstrip('\n')
        book[base[i][0]] = dict(zip(base[i][1::2], base[i][2::2]))
    lg.write_data('Импорт завершен;')

def ex_base(value):  
    lg.write_data('Начат экспорт;')
    if value == '1':
        with open('export.csv', 'w', encoding='windows-1251') as ex_file:
            for key in book.keys():
                ex_file.write(' '.join(list(map(str, book[key].values()))) + '\n')
        lg.write_data('Экспорт 1 завершен')
    elif value == '2':
        with open('export_2.csv', 'w', encoding='windows-1251') as ex_2_file:
            for key in book.keys():
                ex_2_file.write('\n'.join(list(map(str, book[key].values()))) + '\n\n')
        lg.write_data('Экспорт 2 завершен')