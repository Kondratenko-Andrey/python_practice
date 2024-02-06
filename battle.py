from random import choice
from time import sleep


def str_spd(string, spd):
    for el in string:
        print(el, end='', flush=True)
        sleep(spd)


class Knight:

    def __init__(self, name):
        self.name = name
        self.health_points = 200
        self.type_damage = [('мечом в корпус!', 20),
                            ('ногой!', 10),
                            ('мечом и отрубает голову Амазонке О_О !!!', 200),
                            ('и промахивается....', 0),
                            ('мимо, отпрыгивает в сторону и стреляет из арбалета!', 30),
                            ('мечом и разрубает руку Амазонке!', 50)]


class Amazon:

    def __init__(self, name):
        self.name = name
        self.health_points = 200
        self.type_damage = [('копьём в корпус!', 20),
                            ('ногой!', 10),
                            ('копьём и протыкает Рыцаря насквозь О_О !!!', 200),
                            ('и промахивается....', 0),
                            ('в щит Рыцаря, убегает в сторону и стреляет из лука!', 30),
                            ('кинжалом в колено Рыцаря!', 50)]


warriors = (Knight('Рыцарь'), Amazon('Амазонка'))

s = (f'Добро пожаловать на битву Амазонки против Рыцаря!\n'
     f'Каждый из них избран своими собратьями и сёстрами в целях избежания массового кровавого столкновения.\n'
     f'Рыцари прибыли на остров, где проживают амазонки, чтобы захватить его и обзавестись рабами!\n'
     f'У обоих по 200 очков жизней. Приготовьтесь к битве! А за кого болеете Вы......\n\n')

str_spd(s, 0.04)

while (warriors[0].health_points > 0 and warriors[1].health_points > 0):
    attacker = choice(warriors)
    defender = warriors[1 - warriors.index(attacker)]
    attack = choice(attacker.type_damage)
    str_spd(f'{attacker.name} наносит удар {attack[0]}\n', 0.02)

    defender.health_points -= attack[1]

    if defender.health_points <= 0:
        print(f'{attacker.name} убивает', end=' ')
        if defender.name == 'Амазонка':
            print('Амазонку!')
        else:
            print('Рыцаря!')
        sleep(5)
    else:
        str_spd(f'{defender.name} очки здоровья: {defender.health_points}\n\n', 0.02)
        sleep(1.5)
