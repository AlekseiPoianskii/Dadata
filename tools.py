import sys

WELCOME_HEADER = "Добрый день, уважаемый пользователь!\n" \
                 "Вы уже пользовались этой программой?\n" \
                 "1 - Да\n2 - Нет"
REGISTRATION_HEADER = "Для получения координат дома, участка или просто города,\n" \
                      "Вам необходимо зарегистрироваться и получить токен на сайте \n" \
                      "https://dadata.ru/profile/#info"
AUTHORIZATION_HEADER = "В предложенном списке выберите себя и укажите Вашу цифру."
END_MESSAGE = "Всего наилучшего! Вы всегда можете вернуться!"
INFORMATION_MESSAGE = "При помощи это программы у Вас есть возможность узнать координаты дома, квартиры, участка.\n" \
                      "Для получения данной информации Вам необходимо зарегистрироваться на сайте \n" \
                      "https://dadata.ru/profile/#info\n" \
                      "и полученный после регистрации токен указать при регистрации на данной платформе.\n" \
                      "Для выхода из программы Вам необходимо написать 'выход', "


def check_exit(string):
    if string.lower() == "выход":
        return True
    return False


def create_db(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    name TEXT NOT NULL,
    key TEXT NOT NULL,
    language TEXT NOT NULL
    );""")


def registration_user(connection, cursor):
    name_user = input("Введите ваше имя: ")
    if check_exit(name_user):
        print(END_MESSAGE)
        sys.exit(-1)
    token_user = input("Введите Ваш токен: ")
    if check_exit(token_user):
        print(END_MESSAGE)
        sys.exit(-1)
    print("На каком языке показывать список адресов")
    language_user = input("1 - русский 2 - английский\n")
    check_exit(language_user)
    if language_user == "1":
        language_user = "ru"
    else:
        language_user = "en"
    cursor.execute(f"INSERT INTO users VALUES ('{name_user}', '{token_user}', '{language_user}');")
    connection.commit()
    user = (name_user, token_user, language_user)
    return user


def get_list_users(cursor):
    cursor.execute(f"SELECT * FROM users;")
    i = 1
    answer = cursor.fetchall()
    for row in answer:
        print(f"{i} - {row[0]}")
        i += 1
    user = input("Введите номер вашего аккаунта: ")
    if check_exit(user):
        print(END_MESSAGE)
        sys.exit(-1)
    return answer[int(user) - 1]


def start_program(connection, cursor):
    print(WELCOME_HEADER)
    first_start = input()
    if check_exit(first_start):
        print(END_MESSAGE)
        sys.exit(-1)
    if first_start == "2":
        create_db(cursor)
        print(REGISTRATION_HEADER)
        user = registration_user(connection, cursor)
    else:
        print(AUTHORIZATION_HEADER)
        user = get_list_users(cursor)
    return user


def search_geo(session, user):
    while True:
        test_request = input("Введите адрес: ")
        if check_exit(test_request):
            break
        result = session.suggest("address", test_request, language=user[2])
        list_of_address = list()
        i = 0
        for element in result:
            address = element["value"]
            list_of_address.append(address)
            print(f"{i + 1} - {address}")
            i += 1
        number_address = input("Укажите точный адрес (введите номер): ")
        if check_exit(number_address):
            break
        accurate_address = result[int(number_address) - 1]
        print(f"Координаты выбранного места:\nШирота {accurate_address['data']['geo_lat']}"
              f"\nДолгота {accurate_address['data']['geo_lon']}")
