import os, platform


# загружает фикстуры в базу
system = platform.system()
if system == 'Windows':
    os.system('py backend/foodgram/manage.py loaddata new_ingredients.json tag.json')
elif system == 'Linux':
    os.system('python backend/foodgram/manage.py loaddata new_ingredients.json tag.json')
