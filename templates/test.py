import requests
from datetime import datetime, timedelta
import json
from flask import Flask, render_template, request

headers = {"x-fsign": "SW9D1eZo"}
feed = 'mop_1_1'
url = f'https://d.flashscore.ru.com/x/feed/{feed}'

response = requests.get(url, headers=headers)
print(response.text)

app = Flask(__name__)
headers = {"x-fsign": "SW9D1eZo"}

def get_results(): 
    feed = 'E7xPlIWq'
    url = f'https://d.flashscore.ru.com/x/feed/df_hh_1_{feed}'
    # url = f'https://static.criteo.net/js/ld/publishertag.js'
    response = requests.get(url=url, headers=headers)

    data = response.text.split('¬')
    data_list = [{}]

    for item in data:
        key = item.split('÷')[0]
        value = item.split('÷')[-1]

        if '~' in key:
            data_list.append({key: value})
        else: 
            data_list[-1].update({key: value})
            

    results = []
    for game in data_list:
        print(json.dumps(game, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    get_results()