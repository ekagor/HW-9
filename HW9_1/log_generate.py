# Модуль записи логов

def write_data(data):
    with open('log.txt', 'a', encoding='utf=8') as log_file:
        log_file.write(data + '\n')
