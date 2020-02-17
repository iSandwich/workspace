import requests

api_key = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

def lang_select():
    to_lang = 'ru'
    print('Доступные команды: ')
    print('1. Перевести текст с французского: ключ - "F"')
    print('2. Перевести текст с немецкого: ключ - "D"')
    print('3. Перевести текст с испанского: ключ - "E"')
    print('4. Сменить язык результата перевода (По умолчанию русский): ключ - "C"')
    print('5. Завершить работу: ключ - "Q"')
    print()

    while True:
        key = input('Введите ключ нужной команды: ')
        if key.lower() == 'f':
            with open ('FR.txt', encoding='utf8') as file:
                text_input = file.read()
            translate_it(text_input, 'fr', to_lang)
            break
        elif key.lower() == 'd':
            with open ('DE.txt', encoding='utf8') as file:
                text_input = file.read()
            translate_it(text_input, 'de', to_lang)
            break
        elif key.lower() == 'e':
            with open ('ES.txt', encoding='utf8') as file:
                text_input = file.read()
            translate_it(text_input, 'es', to_lang)
            break
        elif key.lower() == 'c':
            to_lang = target_lang()
        elif key.lower() == 'q':
            print('Завершение работы...')
            break
        else:
            print('Ключ не распознан. Пожалуйста, повторите попытку.')

def target_lang():
    language_pool = ['ru', 'en', 'de', 'fr', 'es']
    while True:
        language = input('Введите код одного из доступных языков (ru/en/de/fr/es): ').lower()
        if language not in language_pool:
            print('Код не распознан. Пожалуйста, повторите попытку.')
        else:
            print('Язык выбран.')
            return language

def translate_it(text, lang, to_lang):
    params = {
        'key': api_key,
        'text': text,
        'lang': f'{lang}-{to_lang}'
    }

    response = requests.get(url=url, params=params)
    json_ = response.json()
    with open('result.txt', 'w', encoding='utf8') as file:
        file.write(''.join(json_['text']))
    print('Переведённый текст находится в файле "result.txt".')


if __name__ == '__main__':
    lang_select()