documents = [
  {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
  {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
  {"type": "insurance", "number": "10006"}
  ]

def get_names():
  try:
    for document in documents:
      print(document['name'])
  except KeyError:
    print(f'Документу № {document["number"]} не присвоено имя!')

get_names()
