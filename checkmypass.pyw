import requests
import hashlib
import sys
import PySimpleGUI as sg

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check api and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0



def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)



def main(arg):
    for password in arg:
        count = pwned_api_check(password)
        if count:
           return (f'{password} was found {count} times :( Change your password')
        else:
            return(f'{password} was NOT found. This Password is good!')


sg.theme('dark grey 9')


layout = [[sg.Text("What password would you like to check?")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Quit')]]


window = sg.Window('Password Checker', layout)



if __name__ == '__main__':
    while True:
        event, values = window.read()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
        # Output a message to the window
        window['-OUTPUT-'].update( main([values['-INPUT-']]) )

# Finish up by removing from the screen
window.close()
