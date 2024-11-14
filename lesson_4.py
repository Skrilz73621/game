from random import randint, choice

class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return f'{self.__name} health: {self.health} damage: {self.damage}'


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.__stunned = False

    def choose_defence(self, heroes):
        hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes):
        if self.stunned:
            print(f'Boss {self.name} is stunned and cannot attack.')
            self.stunned = False
            return

        for hero in heroes:
            if hero.health > 0:
                if type(hero) == Berserk and self.__defence != hero.ability:
                    hero.blocked_damage = choice([5, 10])
                    hero.health -= (self.damage - hero.blocked_damage)
                else:
                    hero.health -= self.damage

    @property
    def stunned(self):
        return self.__stunned

    @stunned.setter
    def stunned(self, value):
        self.__stunned = value

    @property
    def defence(self):
        return self.__defence

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' defence: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss):
        boss.health -= self.damage

    def apply_super_power(self, boss, heroes):
        pass


class Magic(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BOOST')

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            hero.damage += 5
        print(f'Magic {self.name} boosted damage to heroes')


class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, 0, 'REVIVE')

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health == 0:
                chance = randint(1, 5)
                if chance >= 2:
                    hero.health += 150
                    self.health = 0
                    print('Witcher sacrificed himself for', hero.name)
                    break


class Hacker(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'HACK')
        self.__stolen_hp = 10

    @property
    def lifesteal(self):
        return self.__stolen_hp

    def apply_super_power(self, boss, heroes):
        boss.health -= self.__stolen_hp
        choice(heroes).health += self.__stolen_hp
        print(f'Hacker {self.name} steals {self.__stolen_hp} health from boss.')


class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'STUN')

    def apply_super_power(self, boss, heroes):
        if self.health > 0:
            if not boss.stunned:
                boss.stunned = True
                print(f'Thor {self.name} stunned boss.')
            else:
                print(f'Boss {boss.name} is already stunned and cannot be stunned again.')


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'CRITICAL_DAMAGE')

    def apply_super_power(self, boss, heroes):
        crit = self.damage * randint(2, 5)
        boss.health -= crit
        print(f'Warrior {self.name} hit critically {crit} to boss.')


class Spitfire(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'SPITFIRE')

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health - boss.damage == 0 and self != hero:
                boss.health -= 80
                print(f'Spitfire {self.name} shows aggression and hits boss with 80 damage.')
                break
            else:
                boss.health -= self.damage


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, 'BLOCK_DAMAGE_AND_REVERT')
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss, heroes):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted {self.__blocked_damage} to boss.')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, 'HEAL')
        self.__heal_points = heal_points

    def apply_super_power(self, boss, heroes):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


round_number = 0


def show_statistics(boss, heroes):
    print(f'ROUND - {round_number} ----------')
    print(boss)
    for hero in heroes:
        print(hero)

def play_round(boss, heroes):
    global round_number

    round_number += 1
    if round_number == 1:
        show_statistics(boss, heroes)
        return

    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if hero.health > 0 and boss.health > 0 and boss.defence != hero.ability:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)


def is_game_over(boss, heroes):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
        return True
    return False


def start_game():
    thor = Thor(name='Grom', health=100, damage=10)
    spitfire = Spitfire(name='Cthulhu', health=200, damage=10)
    hacker = Hacker(name='Noob', health=100, damage=5)
    boss = Boss(name='Dragon', health=1000, damage=50)
    witcher = Witcher(name='Billy', health=230, damage=0)
    warrior_1 = Warrior(name='Mario', health=20, damage=10)
    warrior_2 = Warrior(name='Ben', health=20, damage=15)
    magic = Magic(name='Merlin', health=20, damage=10)
    berserk = Berserk(name='Guts', health=20, damage=5)
    doc = Medic(name='Aibolit', health=20, damage=5, heal_points=15)
    assistant = Medic(name='Kristin', health=130, damage=5, heal_points=5)
    heroes_list = [warrior_1, doc, warrior_2, magic, berserk, assistant, witcher, hacker, spitfire, thor]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
