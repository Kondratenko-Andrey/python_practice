def log_print(func):
    def wrapper(*args, sep=' ', end='\n'):
        with open('log_out.txt', 'a', encoding='UTF-8') as f_out:
            f_out.write(sep.join(map(str, args)) + end)
    return wrapper

print = log_print(print)

import random
from monsters import MonsterBerserk, MonsterHunter


class Hero:

    max_hp = 150
    start_power = 10

    def __init__(self, name):
        self.name = name
        self.__hp = self.max_hp
        self.__power = self.start_power
        self.__is_alive = True

    def get_hp(self):
        return self.__hp

    def set_hp(self, new_value):
        self.__hp = max(new_value, 0)

    def get_power(self):
        return self.__power

    def set_power(self, new_power):
        self.__power = new_power

    def is_alive(self):
        return self.__is_alive

    # Метод make_a_move базового класса могут вызывать только герои, не монстры.
    def attack(self, target):
        # Каждый наследник будет наносить урон согласно правилам своего класса
        raise NotImplementedError("Вы забыли переопределить метод Attack!")

    def take_damage(self, damage):
        # Каждый наследник будет получать урон согласно правилам своего класса
        # При этом у всех наследников есть общая логика, которая определяет жив ли объект.
        print("\t", self.name, "Получил удар с силой равной = ", round(damage), ". Осталось здоровья - ", round(self.get_hp()))
       
        if self.get_hp() <= 0:
            self.__is_alive = False

    def make_a_move(self, friends, enemies):
        # С каждым днём герои становятся всё сильнее.
        self.set_power(self.get_power() + 0.1)

    def __str__(self):
        # Каждый наследник должен выводить информацию о своём состоянии
        raise NotImplementedError("Вы забыли переопределить метод __str__!")


class Healer(Hero):
    '''Целитель'''

    # Атрибуты:
    # - магическая сила - равна значению НАЧАЛЬНОГО показателя силы умноженному на 3 
    def __init__(self, name):
        super().__init__(name)
        self.magic_power = self.get_power() * 3
        
    # Методы:
    
    # - атака - может атаковать врага, но атакует только в половину силы 
    def attack(self, target):
        target.take_damage(self.get_power() * 0.5)

    # - получение урона - т.к. защита целителя слаба - он получает на 20% больше урона
    def take_damage(self, power):
        self.set_hp(self.get_hp() - power * 1.2)
        super().take_damage(power * 1.2)

    # - исцеление - увеличивает здоровье цели на величину равную своей магической силе
    def healing(self, target):
        target.set_hp(target.get_hp() + self.magic_power)
        if target.get_hp() > target.max_hp:
            target.set_hp(target.max_hp)
        
    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии 
    # выполняет ОДНО из действий (атака, исцеление) на выбранную им цель
    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')
        
        #Исцелять будем персонажа с минимальным неполным hp
        #Определяем, есть ли персонажи с неполным hp
        friends_low_hp = list(filter(lambda x: not x.get_hp() == x.max_hp, friends))
        if friends_low_hp:
            #Определяем персонажа с минимальным неполным hp и исцеляем
            target_of_healing = min(friends_low_hp, key=lambda x: x.get_hp())
            self.healing(target_of_healing)
            print("Исцеляю", target_of_healing.name)

        #Проверка наличия врагов
        elif not enemies:
            return

        else:
            #Атакуем ближнего врага
            print("Атакую ближнего -", enemies[0].name)
            self.attack(enemies[0])

    def __str__(self):
        if self.is_alive:
            return f'Имя: {self.name}. HP: {self.get_hp()}'
        else:
            return f'Имя: {self.name} - мёртв...'


class Tank(Hero):
    '''Танк'''
    
    # Атрибуты:
    # - показатель защиты - изначально равен 1, может увеличиваться и уменьшаться
    # - поднят ли щит - танк может поднимать щит, этот атрибут должен показывать поднят ли щит в данный момент

    def __init__(self, name):
        super().__init__(name)
        self.def_points = 1
        self.shield_ready = False

    # Методы:

    # - атака - атакует, но т.к. доспехи очень тяжелые - наносит половину урона 
    def attack(self, target):
        target.take_damage(self.get_power() * 0.5)

    # - получение урона - весь входящий урон делится на показатель защиты  и только потом отнимается от здоровья
    def take_damage(self, power):
        self.set_hp(self.get_hp() - power / self.def_points)
        super().take_damage(power / self.def_points)

    # - поднять щит - если щит не поднят - поднимает щит. Это увеличивает показатель брони в 2 раза, но уменьшает показатель силы в 2 раза.
    def shield_up(self):
        if self.shield_ready:
            raise Exception('Щит уже поднят, второй раз нельзя поднять щит!')
        else:
            self.shield_ready = True
            self.def_points = 2
            self.set_power(self.get_power() / 2)
            print(f'{self.name} поднял щит!')
            
    # - опустить щит - если щит поднят - опускает щит. Это уменьшает показатель брони в 2 раза, но увеличивает показатель силы в 2 раза.
    def shield_down(self):
        if not self.shield_ready:
            raise Exception('Щит уже опущен, второй раз нельзя опускать щит!')
        else:
            self.shield_ready = False
            self.def_points = 1
            self.set_power(self.get_power() * 2)
            print(f'{self.name} опустил щит!')

    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # поднять щит/опустить щит) на выбранную им цель
    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')
        
        #Проверка HP для понимания целесообразности поднятия щита
        if self.get_hp() == self.max_hp and self.shield_ready:
            #Полные HP щит опустим
            self.shield_down()
            #Неполные HP щит поднимем
        elif self.get_hp() != self.max_hp and not self.shield_ready:
            self.shield_up()
            
        #Проверка наличия врагов
        elif not enemies:
            return

        else:
            #Определяем перечень берсерков в команде врага с бешенством > 2
            berserks = list(filter(lambda x: x.madness > 2,
                            filter(lambda x: isinstance(x, MonsterBerserk), enemies)))
        
            if berserks:
                print("Атакую опасного берсерка -", berserks[0].name)
                self.attack(berserks[0])
            else:
            #Атакуем ближнего врага
                print("Атакую ближнего -", enemies[0].name)
                self.attack(enemies[0])

    def __str__(self):
        if self.is_alive:
            return f'Имя: {self.name}. HP: {self.get_hp()}'
        else:
            return f'Имя: {self.name} - мёртв...'

        
class Attacker(Hero):
    '''Убийца'''
    # Атрибуты:
    # - коэффициент усиления урона (входящего и исходящего)
    def __init__(self, name):
        super().__init__(name)
        self.crit_coef = 2
    
    # Методы:

    # - усиление (power_up) - увеличивает коэффициента усиления урона в 2 раза
    def power_up(self):
        self.crit_coef *= 2
        print(f'У {self.name} происходит усиление! Коэфициент усиления урона равен {self.crit_coef}')

    # - ослабление (power_down) - уменьшает коэффициента усиления урона в 2 раза
    def power_down(self):
        self.crit_coef /= 2
        print(f'У {self.name} происходит ослабление! Коэфициент усиления урона равен {self.crit_coef}')

    # - атака - наносит урон равный показателю силы (self.__power) умноженному на коэффициент усиления урона 
    # после нанесения урона - вызывается метод ослабления power_down.
    def attack(self, target):
        target.take_damage(self.get_power() * self.crit_coef)
        self.power_down()

    # - получение урона - получает урон равный входящему урона умноженному на половину коэффициента усиления урона 
    def take_damage(self, power):
        self.set_hp(self.get_hp() - power * (self.crit_coef / 2))

    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # усиление, ослабление) на выбранную им цель
    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')

        #Определяем перечень берсерков в команде врага с бешенством > 1
        berserks = list(filter(lambda x: x.madness > 1,
                          filter(lambda x: isinstance(x, MonsterBerserk), enemies)))
        
        if berserks:
            print("Атакую опасного берсерка -", berserks[0].name)
            self.attack(berserks[0])
            
        elif self.crit_coef < 4:
            self.power_up()

        #Проверка наличия врагов
        elif not enemies:
            return

        else:
            #Атакуем врага у которого больше всего жизней
            target = min(enemies, key=lambda x: x.get_hp())
            print("Атакую врага с наименьшем количеством НР -", target.name)
            self.attack(target)

        
    def __str__(self):
        if self.is_alive:
            return f'Имя: {self.name}. HP: {self.get_hp()}'
        else:
            return f'Имя: {self.name} - мёртв...'

