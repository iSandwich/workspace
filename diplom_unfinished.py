import requests
import pprint
import time

# Входные данные:
api_ver = '5.103'
target_id = '171691064'
target_profile = 'eshmargunov'
target_token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
method_url = 'https://api.vk.com/method/'

# Получение списка друзей "цели" и преобразование оного в множество
params = {
    'v': api_ver,
    'access_token': target_token,
    'user_id': target_id
}
response = requests.get(url=(method_url + 'friends.get?'), params=params)
friends = set(response.json()['response']['items']) # type "set", множество айдишек друзей
time.sleep(0.3)

# Получение списка групп "цели" (интересуют только айди, имя и количество участников)
params = {
    'v': api_ver,
    'access_token': target_token,
    'user_id': target_id,
    'extended': 1,
    'fields': 'members_count'
}
response = requests.get(url=(method_url + 'groups.get?'), params=params)
groups = response.json()['response']['items'] # type "list", содержит словари по каждой группе
time.sleep(0.3)

# Проход по списку групп с получением перечня участников каждой группы, преобразование во множества
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
    members = []
    params = {
        'v': api_ver,
        'access_token': target_token,
        'code': vkscript,
        'group_id': group['id'],
        'offset': 0
    }
    print(f'Starting group "{group["name"]}" with {group["members_count"]} members:')
    while len(members) < group['members_count']:
        response = requests.get(url=(method_url + 'execute?'), params=params)
        time.sleep(0.3)
        members.extend(response.json()['response']['items'])
        params.update({'offset': response.json()['response']['offset']})
        # print(f'\r{len(members)} members parced...', end='')
        print(f'{len(members)} members parced...')
    print(f'Ended with {len(members)} users.\n')
    group['members'] = set(members) # теперь у каждой группы в groups есть ключ members с множеством айдишек

# Проход по groups с использованием intersection. Если результат нулевой, то поля из group переносятся в json_output
json_output = []
for group in groups:
    similarities = friends.intersection(group['members'])
    print(f'Group "{group["id"]}": {len(similarities)} friends found.')
    if len(similarities) == 0:
        json_output.append({'id': group['id'],'name': group['name'],'members_count': group['members_count']})
pprint.pprint(json_output)