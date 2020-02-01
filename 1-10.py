# # 1. Открыть файл на чтение
# # 2. создать пустой список
# # 3. итерировать rss-channel-items
# # 4. создать временные списки, выгрузить в них description и title, используя split()
# # 5. перебором элементов извлечь те, у кого длина >= 6 и приаппендить их в главный список
# # 6. использовать counter, провести сортировку по образцу
# # 7. вывести топ-10 вместе с количеством повторений

import json
import collections

def data_import():
  with open('newsafr.json') as json_file:
    json_contains = json.load(json_file)
    words_list = []
    for item in json_contains['rss']['channel']['items']:
      temp_title = item['title'].split()
      words_list.extend(extract(temp_title))
      temp_description = item['description'].split()
      words_list.extend(extract(temp_description))
    rating(words_list)

def data_import_2():
  import xml.etree.ElementTree as ET
  tree = ET.parse('newsafr.xml')
  root = tree.getroot()
  items = root.findall('channel/item')
  words_list = []
  for item in items:
    temp_title = item.find('title').text.split()
    words_list.extend(extract(temp_title))
    temp_description = item.find('description').text.split()
    words_list.extend(extract(temp_description))
  rating(words_list)

def extract(split):
  words = []
  for item in split:
    if len(item) >= 6:
     words.append(item)
  return words

def rating(words):
  counter = collections.Counter()
  for word in words:
    counter[word] += 1
  top_10 = counter.most_common(10)
  print('Топ-10 наиболее часто встречаемых слов с длиной более 6 символов:')
  for position in top_10:
    print(f'"{position[0]}": {position[1]} повторений;')

data_import()
print()
data_import_2()