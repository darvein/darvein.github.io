# For loop :D
for i in range (2, 2):
    if i % 2 == 0:
        print('{}: even'.format(i))
    else:
        print('{}: odd'.format(i))

# Match/Case statement
from enum import Enum
class Color(Enum):
    RED = 'red'
    WHITE = 'white'
    GREEN = 'green'
try:
    color = Color(input('Enter something bro: '))
    match color:
        case Color.RED:
            print('Rojo de la nueva sangre!')
        case Color.WHITE:
            print('Blanca cocaina')
        case Color.GREEN:
            print('Verde marihuana')
        case _:
            print('Default?')
except ValueError:
    print('Lyrics by Santa Fe Klan!')

# Functions
def secret_ask(prompt, retries=3, tryagain="Please try again bro"):
    while True:
        rsp = input(prompt)
        if rsp in 'whiterabbit':
            print("You're the choosen one br0")
            return True
        retries = retries - 1
        if retries < 0:
            raise ValueError('Invalid Response DuD3')
        print(tryagain)
secret_ask("huh?: ")
