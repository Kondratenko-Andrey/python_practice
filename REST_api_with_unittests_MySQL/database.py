from peewee import *
from datetime import datetime

db = MySQLDatabase('my_base', user='root', password='password', host='127.0.0.1', port=3306)


class Task(Model):
    created_at = DateTimeField(default=datetime.now().replace(microsecond=0))
    title = CharField(null=True, unique=True)
    description = CharField(null=True)
    updated_at = DateTimeField(default=datetime.now().replace(microsecond=0))

    class Meta:
        database = db
        db_table = "task"

    # Поиск строки в таблице по значению одного из столбцов
    @staticmethod
    def get_row_by_attr(attr, val):
        row = Task.get(getattr(Task, attr) == val)
        return row.__data__

    # Вывод таблицы в консоль
    @staticmethod
    def show_table():
        query = Task.select()
        for row in query:
            print(row.id, row.created_at, row.title, row.description, row.updated_at)

    # Запаковка в список словарей данных таблицы
    @staticmethod
    def get_info():
        info = []
        query = Task.select().dicts()
        for dct in query:
            info.append(dct)
        return info


with db:
    db.create_tables([Task])

if __name__ == '__main__':
    with db:
        new_task = Task.create(
            created_at=datetime.now().replace(microsecond=0),
            title='Задание1',
            description='Иди туда',
            updated_at=datetime.now().replace(microsecond=0)
        )

        new_task_2 = Task.create(
            created_at=datetime.now().replace(microsecond=0),
            title='Задание2',
            description='Иди обратно',
            updated_at=datetime.now().replace(microsecond=0)
        )

    with db:
        Task.show_table()
