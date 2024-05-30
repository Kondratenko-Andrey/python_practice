import json
import unittest
from main import app
from database import Task


class TestRESTapi(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/tasks'

    # Отправляем запрос POST с данными для ввода в базу данных,
    # затем удаляем для исключения засорения базы
    def test_handle_post_request_1(self):
        # Данные для тестового запроса
        req_data = {
            "title": "test_1",
            "description": "send test_1"
        }

        data = json.dumps(req_data)
        response = self.app.post(self.base_url, data=data, content_type='application/json')
        json_response = response.get_json()

        # Проверка статус кода
        self.assertTrue(response.status_code == 201)

        # Проверка записанного значения
        self.assertEqual(
            Task.get_row_by_attr("id", json_response["id"])["title"],
            "test_1"
        )

        # Удаляем тестовую запись
        response = self.app.delete(f'{self.base_url}/{json_response["id"]}')
        self.assertEqual(response.status_code, 200)

        # Проверяем отсутствие данной строки в таблице
        self.assertFalse(
            json_response["title"] in [el.title for el in Task.select(Task.title)])

    # Отправляем запрос POST с заведомо неприемлимыми типами данных
    def test_handle_post_request_2(self):
        # Данные для тестового запроса
        req_data = {
            "title": 4,
            "description": 2
        }
        data = json.dumps(req_data)

        # Отправляем POST запрос
        response = self.app.post(self.base_url, data=data, content_type='application/json')
        # Проверяем статус кода с ошибкой
        self.assertEqual(response.status_code, 400)

    # Отправляем запрос GET
    def test_handle_get_request(self):
        response = self.app.get(self.base_url)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(
            len([el.id for el in Task.select(Task.id)]),
            len(response.get_json())
        )

    # Отправляем запрос PUT
    def test_handle_put_request(self):
        # Данные для тестового запроса
        req_data = {
            "title": "test_2",
            "description": "send test_2"
        }

        data = json.dumps(req_data)
        id_lst = [el.id for el in Task.select(Task.id)]
        response = self.app.put(
            f'{self.base_url}/{max(id_lst)}',
            data=data,
            content_type='application/json')
        self.assertTrue(response.status_code, 200)

        # Проверка обновлённого значения
        self.assertEqual(
            Task.get_row_by_attr("id", max(id_lst))["title"],
            "test_2"
        )

        # Оправляем запрос с ошибкой (данного индекса нет в базе данных)
        response = self.app.put(
            f'{self.base_url}/{max(id_lst) + 1}',
            data=data,
            content_type='application/json')
        self.assertTrue(response.status_code, 400)

    # Отправляем запрос DELETE
    def test_handle_delete_request(self):
        id_lst = [el.id for el in Task.select(Task.id)]
        response = self.app.delete(f'{self.base_url}/{max(id_lst)}')
        self.assertTrue(response.status_code, 200)

        # Проверяем отсутствие данного индекса в таблице
        self.assertFalse(
            max(id_lst) in [el.id for el in Task.select(Task.id)])

        # Оправляем запрос с ошибкой (данного индекса нет в базе данных)
        response = self.app.delete(f'{self.base_url}/{max(id_lst) + 1}')
        self.assertTrue(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
