import functools
from datetime import datetime
from typing import Callable, Any
import time


def logger(str_date: str, cls) -> Callable:
    str_date_with_marks = ''.join(['%' + el if el.isalpha() else el for el in str_date])

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            print(f"- Запускается '{cls.__name__}.{func.__name__}'. "
                  f"Дата и время запуска: {datetime.now().strftime(str_date_with_marks)} ")
            start_time = time.perf_counter()
            func_res = func(*args, **kwargs)
            print(f'- Завершение {cls.__name__}.{func.__name__}, '
                  f'время работы = {round(time.perf_counter() - start_time, 3)}s')
            return func_res

        return wrapper

    return decorator


def log_methods(str_date: str) -> Callable:
    def decorate(cls):
        for name_method in dir(cls):
            if name_method.startswith('__') is False:
                method = getattr(cls, name_method)
                setattr(cls, name_method, logger(str_date, cls)(method))
        return cls

    return decorate


@log_methods("b d Y - H:M:S")
class A:
    def test_sum_1(self) -> int:
        print('test sum 1')
        number = 100
        result = 0
        for _ in range(number + 1):
            result += sum([i_num ** 2 for i_num in range(10000)])

        return result


@log_methods("b d Y - H:M:S")
class B(A):
    def test_sum_1(self):
        super().test_sum_1()
        print("Наследник test sum 1")

    def test_sum_2(self):
        print("test sum 2")
        number = 200
        result = 0
        for _ in range(number + 1):
            result += sum([i_num ** 2 for i_num in range(10000)])

        return result


my_obj = B()
print(dir(my_obj))
my_obj.test_sum_1()
my_obj.test_sum_2()
