def cooking_book():
  cook_book = {}
  with open('recipes.txt', encoding='utf8') as recipes:
      while True:
          dish = recipes.readline().strip()
          if not dish:
              break
          else:
              counter = int(recipes.readline().strip())
              ingredients = []
              for n in range(counter):
                  temp_list = recipes.readline().strip().split(' | ')
                  temp_dict = {}
                  temp_dict['ingredient name'] = temp_list[0]
                  temp_dict['quantity'] = int(temp_list[1])
                  temp_dict['measure'] = temp_list[2]
                  ingredients.append(temp_dict)
              cook_book[dish] = ingredients
              recipes.readline()
  return cook_book


def shopping_list(dishes, person_count):
  products = {}
  cook_book = cooking_book()
  for dish in dishes:
    for product in cook_book[dish]:
      prod_name = product['ingredient name']
      prod_num = product['quantity']
      prod_mes = product['measure']
      if prod_name in products.keys():
        new_prod_num = prod_num * person_count + products[prod_name]['quantity']
        products[prod_name]['quantity'] = new_prod_num
      else:
        products[prod_name] = {'measure': prod_mes, 'quantity': (prod_num * person_count)}
  return products


def main():
  dishes = ['Омлет', 'Фахитос']
  person_count = 4

  dict1 = cooking_book()
  dict2 = shopping_list(dishes, person_count)

  for dish in dict1:
      print (dish)
      for product in dict1[dish]:
        print(product)
  print()
  for product in dict2:
    print(product, dict2[product])

    
main()
