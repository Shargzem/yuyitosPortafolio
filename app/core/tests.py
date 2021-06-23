from config.wsgi import *
from core.models import *
import random

data = ['Leche y derivados', 'Carnes, pescados y huevos', 'Patatas, legumbres, frutos secos',
        'Verduras y Hortalizas', 'Frutas', 'Cereales y derivados, azúcar y dulces',
        'Grasas, aceite y mantequilla']

#insertar data
# for i in data:
#     cat = Category(name=i)
#     cat.save()
#     print('Guardado registro N°{}'.format(cat.id))


letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t',
           'u','v','w','x','y','z']

#crear registros random
for i in range(1, 1000):
    name = ''.join(random.choices(letters, k=5))
    while Category.objects.filter(name=name).exists():
        name = ''.join(random.choices(letters, k=5))
    Category(name=name).save()
    print('Guardado registro {}'.format(i))


