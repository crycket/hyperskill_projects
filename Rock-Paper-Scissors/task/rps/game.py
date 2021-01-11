import random


def get_rating():
    name = input('Enter your name:')
    print(f'Hello, {name}')
    with open('rating.txt', 'r') as f:
        for line in f.readlines():
            if name in line:
                return int(line.split()[1])
        else:
            return 0


def get_win_dict(options):
    win_dict = dict()
    length = len(options)
    for i in range(length // 2):
        start = i + 1
        stop = i + length // 2 + 1
        win_dict[options[i]] = options[start:stop]
    for i in range(length // 2, length):
        start = i + 1
        stop = i - length // 2
        win_dict[options[i]] = options[start:] + options[:stop]
    return win_dict


rating = get_rating()
option_list = input()

if option_list:
    option_list = option_list.split(',')
    win = get_win_dict(option_list)
else:
    win = {'paper': 'scissors', 'scissors': 'rock', 'rock': 'paper'}
    option_list = list(win.values())

print("Okay, let's start")
while True:
    option = input()
    if option not in ('!exit', '!rating') and option not in option_list:
        print('Invalid input')
        continue
    if option == '!rating':
        print(f'Your rating: {rating}')
        continue
    if option == '!exit':
        print('Bye!')
        break

    choice = random.choice(option_list)
    if option == choice:
        print(f'There is a draw {choice}')
        rating += 50
    elif option in win[choice]:
        print(f'Well done. Computer chose {choice} and failed')
        rating += 100
    else:
        print(f'Sorry, but computer chose {choice}')
