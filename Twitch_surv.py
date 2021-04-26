import requests
import winsound
import time
import os
os.system('color')  # Enables ANSI


def is_live(username):
    HEADERS = {'client-id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
    GQL_QUERY = """
    query($login: String) {
        user(login: $login) {
            stream {
                id
            }
        }
    }
    """
    QUERY = {
        'query': GQL_QUERY,
        'variables': {
            'login': username
        }
    }

    response = requests.post('https://gql.twitch.tv/gql',
                             json=QUERY, headers=HEADERS)
    dict_response = response.json()
    return True if dict_response['data']['user']['stream'] else False


def alarm(t='inf'):
    if t == 'inf':
        while True:
            winsound.Beep(500, 500)
            time.sleep(0.5)
    else:
        for _ in range(t):
            winsound.Beep(500, 500)
            time.sleep(0.5)


N_users = input('How many users do you want to check? ')
while not N_users.isnumeric():
    N_users = input('\33[33m' + 'Please input an integer. ' + '\33[39m')
N_users = int(N_users)

USERS = []
for u in range(N_users):
    USERS.append(input(f'User {u+1}:\t'))

n, error_user = -1, None
accepted = False
try:
    for n, user in enumerate(USERS):
        error_user = user
        is_live(user)
except BaseException as e:
    print('\33[31m' +
          f'Input not accepted. Check if the user \"{error_user}\" is valid or check the internet connection')
    print('Error code:', e, '\33[39m')
    while not accepted:
        USERS[n] = (input(f'User {n + 1}:\t'))
        try:
            for n, user in enumerate(USERS):
                error_user = user
                is_live(user)
            accepted = True
        except BaseException as e:
            print('\33[31m' +
                  f'Input not accepted. Check if the user \"{error_user}\" is valid or check the internet connection')
            print('Error code:', e, '\33[39m')


check_kind = input('\nChoose what kind of check you want to do:\n'
                   '1) Single check\n'
                   '2) Continuous check\n')

accepted = False
while not accepted:
    if not check_kind.isnumeric():
        check_kind = input('\33[33m' + 'Please input an integer. ' + '\33[39m')
    else:
        if not (0 < int(check_kind) < 3):
            check_kind = input('\33[33m' + 'Please choose one of the options. ' + '\33[39m')
        else:
            accepted = True
            check_kind = int(check_kind)

Alarm = False
Alarming = False
if check_kind == 2:
    Alarm = ('y' in input('\nDo you want an alarm? ').lower())
    if Alarm:
        print('Alarm enabled')
    else:
        print('Alarm disabled')

counter = 1
checkInterval = 120
if check_kind == 2:
    print('\nChecking if user' +
          's are ' * (len(USERS) > 1) + ' is ' * (len(USERS) == 1) +
          f'live every {checkInterval} seconds\n\n')
elif check_kind == 1:
    print('\nChecking if user' +
          's are ' * (len(USERS) > 1) + ' is ' * (len(USERS) == 1) + f'live\n\n')

while True:
    if counter > 1:
        for _ in USERS:
            print('\033[A\033[K', end='')  # Moves cursor up one line and clears that line
    print(f'\033[A\033[KCheck number: {counter}')
    for n, user in enumerate(USERS):
        try:
            IS_LIVE = is_live(user)
        except BaseException as e:
            print('\33[33m' + f'Possible error at check {counter}:', e)
            print('Will retry in 300 seconds' + '\33[39m')
            time.sleep(300)
            try:
                IS_LIVE = is_live(user)
            except BaseException as e:
                print('\33[31m' + 'Uncorrectable error:', e, '\33[39m')
                if Alarm:
                    alarm()
                else:
                    exit()
                IS_LIVE = False
        print(f'{n + 1}\t' + user + '.'*(20 - len(user)), end='')
        if IS_LIVE:
            print('\33[32m' + f'{IS_LIVE}' + '\33[39m')
        else:
            print('\33[31m' + f'{IS_LIVE}' + '\33[39m')
        if IS_LIVE & Alarm:
            Alarming = True
    counter += 1
    if check_kind == 1:
        input()
        exit()
    if Alarming:
        alarm(checkInterval)
    else:
        time.sleep(checkInterval)
    Alarming = False
