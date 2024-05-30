from flask import Flask, request, jsonify
from marshmallow import ValidationError
from database import db, Task
from datetime import datetime

from json_validation import TaskSchemaPOST, TaskSchemaGET

with db:
    db.create_tables([Task])

app = Flask(__name__)


@app.route('/tasks', methods=['POST'])
def handle_post_request():
    '''
    1. Создание задачи:
    - Метод: POST
    - URL: /tasks
    - Параметры запроса: JSON-объект с полями title (строка) и description (строка, опционально).
    - Ответ: JSON-объект с полями id, title, description, created_at, updated_at.
    '''

    # Получение данных из запроса в формате JSON
    json_data = request.get_json()

    try:
        # Валидация входящих данных с помощью схемы TaskSchema
        task_schema = TaskSchemaPOST()
        task_data = task_schema.load(json_data)

        # Ввод данных в базу
        with db:
            Task.create(
                title=task_data['title'],
                description=task_data['description']
                if 'description' in task_data else None,
                created_at=datetime.now().replace(microsecond=0),
                updated_at=datetime.now().replace(microsecond=0)
            )

            # Получаем из базы данных через атрибут title сформированную новую строку таблицы в формате словаря
            response = Task.get_row_by_attr('title', task_data['title'])

        # Сериализуем в JSON и возвращаем
        return jsonify(response), 201

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400


@app.route('/tasks', methods=['GET'])
def handle_get_request():
    '''
    2. Получение списка задач:
    - Метод: GET
    - URL: /tasks
    - Ответ: JSON-список задач, где каждая задача представляет собой JSON-объект
    с полями id, title, description, created_at, updated_at.
    '''

    # Получаем из базы данных все строки (итоговый список), каждая из которых в формате словаря,
    response = Task.get_info()

    # Сериализуем в JSON и возвращаем
    return jsonify(response), 200


@app.route('/tasks/<int:item_id>', methods=['PUT'])
def handle_put_request(item_id: int):
    '''
    4. Обновление задачи:
    - Метод: PUT
    - URL: /tasks/<id>
    - Параметры запроса: JSON-объект с полями title (строка, опционально) и description (строка, опционально).
    - Ответ: JSON-объект с полями id, title, description, created_at, updated_at.
    '''

    # Получение данных из запроса в формате JSON
    json_data = request.get_json()

    try:
        # Проверка базы данных на наличие индекса строки для обновления
        if item_id not in [el.id for el in Task.select(Task.id)]:
            raise ValidationError('Данный индекс отсутствует!')

        # Валидация входящих данных с помощью схемы TaskSchema
        task_schema = TaskSchemaGET()
        task_data = task_schema.load(json_data)

        # Получаем из базы через данных атрибут id необходимую строку
        row = Task.get(getattr(Task, 'id') == item_id)

        # Заменяем данные, при этом id остаётся прежний и сохраняем
        Task(
            id=row.id,
            title=task_data['title']
            if 'title' in task_data else row.title,
            description=task_data['description']
            if 'description' in task_data else row.description,
            created_at=row.created_at,
            updated_at=datetime.now().replace(microsecond=0)
        ).save()

        # Формируем JSON ответ
        response = jsonify(
            Task.get(getattr(Task, 'id') == item_id).__data__)
        return response, 200

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400


@app.route('/tasks/<int:item_id>', methods=['DELETE'])
def handle_delete_request(item_id: int):
    '''
    5. Удаление задачи:
    - Метод: DELETE
    - URL: /tasks/<id>
    - Ответ: Сообщение об успешном удалении.
    '''

    try:

        # Проверка базы данных на наличие индекса строки для обновления
        if item_id not in [el.id for el in Task.select(Task.id)]:
            raise ValidationError('Данный индекс отсутствует!')

        query = Task.get_by_id(item_id)
        query.delete_instance()

        return f'Строка {item_id} успешно удалена!'

    except ValidationError as err:
        return jsonify({'error': err.messages}), 400


if __name__ == '__main__':
    app.run(debug=True)
