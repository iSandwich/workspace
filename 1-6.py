class animal():
    name = 'A horse with no name'
    weight = 0 # kg
    voiceline = 'Howdy'
    hunger_state = 'hungry'

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def init_voiceline(self):
        print(f'{self.voiceline}!')

    def feed(self, food_weight):
        if food_weight <= 0:
            print('I see what you\'re doing here!')
        else:
            self.hunger_state = 'fed'
            self.init_voiceline()


class cow(animal):
    voiceline = 'mooo'

    def milk(self):
        if self.hunger_state == 'fed':
            print('You\'ve got some milk.')
            self.hunger_state = 'hungry'
        else:
            print('Feed the animal first!')


class goat(cow):
    voiceline = 'meeeh'


class sheep(animal):
    voiceline = 'baaa'

    def shear(self):
        if self.hunger_state == 'fed':
            print('You\'ve got some wool.')
            self.hunger_state = 'hungry'
        else:
            print('Feed the animal first!')


class chicken(animal):
    voiceline = 'cluck'

    def grab_eggs(self):
        if self.hunger_state == 'fed':
            print('You\'ve got some eggs.')
            self.hunger_state = 'hungry'
        else:
            print('Feed the animal first!')


class duck(chicken):
    voiceline = 'quack'


class goose(chicken):
    voiceline = 'HONK'


################################################################

goose1 = goose('Серый', 5)
goose2 = goose('Белый', 6)
cow1 = cow('Манька', 747)
sheep1 = sheep('Барашек', 120)
sheep2 = sheep('Кудрявый', 110)
chick1 = chicken('Кукареку', 3)
chick2 = chicken('Ко-Ко', 3)
goat1 = goat('Рога', 120)
goat2 = goat('Рога', 110)
duck1 = duck('Кряква', 5)
