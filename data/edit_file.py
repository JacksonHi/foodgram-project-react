import json

"Редактирует файл с ингредиентами"
with open('data/ingredients.json', 'r', encoding='utf-8') as f:
    text = json.load(f)
    pk = 0
    list = []
    
    for i in text:
        data = {
              "model":  "recipes.ingredients",
              "pk":  pk,
              "fields":  {}
           }
        data['pk'] = pk
        data['fields']['name'] = i['name']
        data['fields']['measurement_unit'] = i['measurement_unit']
        list.append(data)
        pk += 1
    with open('data/new_ingredients.json', 'w') as write_file:
        json.dump(list, write_file)
