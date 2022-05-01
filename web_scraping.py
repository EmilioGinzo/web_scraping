import requests


r = requests.get('https://github.com/topics')


with open('test.txt', 'w', encoding = 'utf-8') as outfile:
    outfile.write(r.text)