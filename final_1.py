import requests
import pprint
import time
import json

# Входные данные:
api_ver = '5.103'
target_id = '171691064'
# target_profile = 'eshmargunov'
target_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
method_url = 'https://api.vk.com/method/'

def clrscr():
    print("\n" * 100)
    print('Дипломная работа по блоку "Основы языка программирования Python"')
    print('Автор: Лепихов А. / группа PY-28.1')
    print(f'ID пользователя для проверки: {target_id} (Е. Шмаргунов)')
    print('\nСписок операций:')
    print('"1" - Обновить список друзей')
    print('"2" - Обновить список групп')
    print('"3" - Выполнить анализ совпадений')
    print('"4" - Прервать работу программы\n')


def failcheck(arg):
    if arg == 'failed':
        return 'недоступен'
    else:
        return 'доступен'


def get_friendlist():
    # Получение списка друзей "цели" и преобразование оного в множество
    print('\nПолучение списка друзей пользователя:')
    params = {
        'v': api_ver,
        'access_token': target_token,
        'user_id': target_id
    }

    error_count = 0
    while error_count < 10:
        print(f'\rПопытка {error_count + 1}...', end='')
        response = requests.get(url=(method_url + 'friends.get?'), params=params)
        time.sleep(0.3)
        if 'execute_errors' in response.json():
            error_count += 1
        else:
            friends = set(response.json()['response']['items'])
            # type "set", множество айдишек друзей
            print(f'\nСписок друзей получен, количество - {len(friends)}.')
            break

    if error_count == 10:
        friends = 'failed'
        print('Истёк лимит попыток запроса. Повторите операцию позднее.')
    return friends


def get_grouplist():
    # Получение списка групп "цели" (интересуют только айди, имя и количество участников)
    print('\nПолучение списка групп пользователя:')
    params = {
        'v': api_ver,
        'access_token': target_token,
        'user_id': target_id,
        'extended': 1,
        'fields': 'members_count'
    }

    error_count = 0
    while error_count < 10:
        print(f'\rПопытка {error_count + 1}...', end='')
        response = requests.get(url=(method_url + 'groups.get?'), params=params)
        time.sleep(0.3)
        if 'execute_errors' in response.json():
            error_count += 1
        else:
            groups = response.json()['response']['items']
            # type "list", содержит словари по каждой группе
            print(f'\nСписок групп получен, количество - {len(groups)}.', end='')
            break

    if error_count == 10:
        groups = 'failed'
        print('Истёк лимит попыток запроса. Повторите операцию позднее.')
    else: groups = group_addmembers(groups)
    return groups


def group_addmembers(groups):
    # Получение перечня участников каждой группы, преобразование во множества
    vkscript = '''
    var group_id = parseInt(Args.group_id);
    var offset = parseInt(Args.offset);
    var members = [];
    var counter = 0;
    while(counter < 25)
    {
    members = members + API.groups.getMembers({"group_id": group_id, "offset": offset}).items;
    offset = offset + 1000;
    counter = counter + 1;
    }
    return {'items': members, 'offset': offset};
    '''

    for group in groups:
        error_count = 0
        members = []
        params = {
            'v': api_ver,
            'access_token': target_token,
            'code': vkscript,
            'group_id': group['id'],
            'offset': 0
        }

        print(f'\n\nСоздание списка для "{group["name"]}", участников- {group["members_count"]}:')
        while len(members) < group['members_count']:
            response = requests.get(url=(method_url + 'execute?'), params=params)
            time.sleep(0.3)

            if 'execute_errors' in response.json():
                error_count += 1
                print(f'\rУчастников пройдено - {len(members)}, ошибок - {error_count}...',
                      end='')

            else:
                new_members = response.json()['response']['items']
                new_offset = response.json()['response']['offset']
                if len(new_members) <= 25000:
                    members.extend(new_members)
                    params.update({'offset': new_offset})
                    print(f'\rУчастников пройдено - {len(members)}, ошибок - {error_count}...',
                          end='')

        group['members'] = set(members)
        # теперь у каждой группы в groups есть ключ members с множеством айдишек
    print('\n\nСоздание списков завершено.')
    return groups


def compare(friends, groups):
    limit = 5
    json_output = {'Нет совпадений': [],
                   f'Меньше {limit} совпадений': [],
                   f'Больше {limit} совпадений': []}
    print(f'\nЧисловое ограничение на совпадения равно {limit};')

    for group in groups:
        similarities = friends.intersection(group['members'])

        if len(similarities) == 0:
            json_output['Нет совпадений'].append(
                {'id': group['id'],
                 'name': group['name'],
                 'members_count': group['members_count']})
        elif 0 < len(similarities) <= 5:
            json_output[f'Меньше {limit} совпадений'].append(
                {'id': group['id'],
                 'name': group['name'],
                 'members_count': group['members_count']})
        else:
            json_output[f'Больше {limit} совпадений'].append(
                {'id': group['id'],
                 'name': group['name'],
                 'members_count': group['members_count']})

    print('Результаты анализа:')
    print(f'-Групп без друзей: {len(json_output["Нет совпадений"])}')
    print(f'-Групп, где менее {limit} друзей: {len(json_output[f"Меньше {limit} совпадений"])}')
    print(f'-Групп, где более {limit} друзей: {len(json_output[f"Больше {limit} совпадений"])}')
    with open('groups.json', 'w', encoding='utf8') as file:
        json.dump(json_output, file, indent=2, ensure_ascii=False)
    print('\nРезультаты  сохранены в файл "groups,json"')


def interface():
    friends = 'failed'
    groups = 'failed'

    while True:
        clrscr()
        print(f'Список друзей: {failcheck(friends)}.\nСписок групп: {failcheck(groups)}.')
        answer = input('Введите номер операции: ')

        if answer == '1':
            friends = get_friendlist()
            input('Нажмите Enter для продолжения...')
        elif answer == '2':
            groups = get_grouplist()
            input('Нажмите Enter для продолжения...')
        elif answer == '3':
            if friends == 'failed' or groups == 'failed':
                print('\nНедостаточно данных. Проверьте доступность списков.')
                input('Нажмите Enter для продолжения...')
            else:
                compare(friends, groups)
                input('Нажмите Enter для продолжения...')
        elif answer == '4':
            print('Завершение работы программы...')
            return
        else:
            print('Некорректный ответ. Необходимо повторить попытку.')


interface()