def get_social_status(age: int) -> str:
    if not isinstance(age, (float, int)):
        raise ValueError('Please provide a number')

    if age < 0:
        raise ValueError('Check age')
    elif 0 <= age < 13:
        return 'ребёнок'
    elif 13 <= age < 18:
        return 'подросток'
    elif 18 <= age < 50:
        return 'взрослый'
    elif 50 <= age < 65:
        return 'пожилой'
    else:
        return 'пенсионер'


if __name__ == '__main__':
    get_social_status()
