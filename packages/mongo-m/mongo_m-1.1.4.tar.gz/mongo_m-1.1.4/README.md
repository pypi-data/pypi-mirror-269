#  *Миграции MONGO_DB*

Сравнивает модели Pydantic с коллекциями и добовляет или удаляет поля

## Установка модуля

> pip install mongo-m

### Инициализация
> python -m mongo_m init

При выполнении команды создается директория ***migration*** и файл ***config.ini***

#### Config.ini
[MONGO]
- 'host': sting,
- 'port': int,
- 'user': string,
- 'password': string,
- 'database': string,
- - Имя базы данных в MongoDB `Так же тут будет происходить проверка коллекций`
- 'module_path': string 
- - Относительный путь к модели или пакету где содержаться данных
- - Пример app/src/schemas или путь к модулю app/src/schemas/module_name `без расширения .py`

### Создание миграций

> python -m mongo_m create-migration

Создается файл в папке ***migration***/***name.json***. Так же создается файл ***migration***/***upload.json*** который содержит stack миграций

#### Концепция работы

Для того чтобы считались классы. Нужно чтобы класс имел поле ***`__table_name__`*** или ***`__tablename__`***

Пример класса

```
from pydantic import BaseModel, Field

 class Test(BaseModel)
    __table_name__ = "collection_name"
    test1: int - 'по дефолту значение при добавлнении будет 0'
    test2: int = Field(dafult=10)
    
```

### Выполнение миграций

> python -m mongo_m update-migration
> 
> > key -a служит для добавления полей
> 
> > key -d служит для удаления полей
> 
> Пример: python -m mongo_m update-migration -a

В консоль выведит поля которые должны добавться или удалиться если таковые имеются

и выводится ошибка при добавлении

если будет **E11000** (то все в норме)