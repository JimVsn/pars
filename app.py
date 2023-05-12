import requests
from datetime import datetime, timedelta
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
headers = {"x-fsign": "SW9D1eZo"}


def get_results(date):
    today = datetime.now().date()
    selected_date = date.date()
    days_diff = (selected_date - today).days

    if days_diff == 0:
        feed = 'f_1_0_3_ru_1'
    else:
        feed = f'f_1_{days_diff}_3_ru_1'

    url = f'https://d.flashscore.ru.com/x/feed/{feed}/{date.year}-{date.month:02d}-{date.day:02d}'
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
        if 'AA' in list(game.keys())[0]:
            game_date = datetime.fromtimestamp(int(game.get('AD'))).strftime('%d-%m-%Y %H:%M')
            team_1 = game.get("AE")
            team_2 = game.get("AF")
            score = f'{game.get("AG")} : {game.get("AH")}' if game.get("AG") is not None and game.get("AH") is not None else "Матч не сыгран"
            match_key = game.get("~AA")
            results.append({'date': game_date, 'team_1': team_1, 'team_2': team_2, 'score': score, 'match_key': match_key})

    sorted_results = sorted(results, key=lambda x: x['date'])

    return sorted_results


def get_match_results(match_key):
    feed = f'df_hh_1_{match_key}'
    url = f'https://d.flashscore.ru.com/x/feed/{feed}'
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
        if '~KC' in list(game.keys())[0]:
            game_date = datetime.fromtimestamp(int(game.get('~KC'))).strftime('%d-%m-%Y %H:%M')
            team_1 = game.get("KJ")
            team_2 = game.get("KK")
            score = f'{game.get("KU")} : {game.get("KT")}' if game.get("KU") is not None and game.get("KT") is not None else "Матч не сыгран"
            results.append({'date': game_date, 'team_1': team_1, 'team_2': team_2, 'score': score})

    # sorted_results = sorted(results, key=lambda x: x['date'])

    return results


def get_default_date():
    return datetime.now().date()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_date = datetime.strptime(request.form['date'], "%Y-%m-%d")
    else:
        selected_date = datetime.now()

    results_data = get_results(selected_date)
    return render_template('index.html', results=results_data, date=selected_date, default_date=get_default_date(), timedelta=timedelta)


@app.route('/results')
def results():
    date_param = request.args.get('date')
    if date_param:
        selected_date = datetime.strptime(date_param, "%Y-%m-%d")
    else:
        selected_date = datetime.now()

    results_data = get_results(selected_date)
    return render_template('results.html', results=results_data, timedelta=timedelta)


@app.route('/match')
def match():
    date = request.args.get('date')
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    match_key = request.args.get('match_key')
    match_results_data = get_match_results(match_key)

    return render_template('match.html', date=date, team1=team1, team2=team2, match_key=match_key, match_results=match_results_data)

@app.route('/match_results')
def match_results():
    match_key = request.args.get('match_key')
    match_results_data = get_match_results(match_key)
    return json.dumps(match_results_data)


if __name__ == '__main__':
    app.run()








# ниже работающий первоначальный образец

# app = Flask(__name__)
# headers = {"x-fsign": "SW9D1eZo"}

# def get_results(): 
#     feed = 'f_1_0_3_ru_1'
#     url = f'https://d.flashscore.ru.com/x/feed/{feed}'
#     response = requests.get(url=url, headers=headers)

#     data = response.text.split('¬')
#     data_list = [{}]

#     for item in data:
#         key = item.split('÷')[0]
#         value = item.split('÷')[-1]

#         if '~' in key:
#             data_list.append({key: value})
#         else: 
#             data_list[-1].update({key: value})
            

#     results = []
#     for game in data_list:
#         if 'AA' in list(game.keys())[0]:
#             date = datetime.fromtimestamp(int(game.get('AD'))).strftime('%d-%m-%Y %H:%M')
#             team_1 = game.get("AE")
#             team_2 = game.get("AF")
#             score = f'{game.get("AG")} : {game.get("AH")}' if game.get("AG") is not None and game.get("AH") is not None else "Матч не сыгран"
#             results.append({'date': date, 'team_1': team_1, 'team_2': team_2, 'score': score})

#             sorted_results = sorted(results, key=lambda x: x['date'])
    
#     return sorted_results

# @app.route('/')
# def index():
#     results_data = get_results()
#     return render_template('index.html', results=results_data)

# @app.route('/results')
# def results():
#     results_data = get_results()
#     return render_template('results.html', results=results_data)

# if __name__ == '__main__':
#     app.run()


# Ниже код бота для проверки ответа на запрос.

# headers = {"x-fsign": "SW9D1eZo"}
# feed = 'mop_1_1'
# url = f'https://d.flashscore.ru.com/x/feed/{feed}'

# response = requests.get(url, headers=headers)
# print(response.text)

# app = Flask(__name__)
# headers = {"x-fsign": "SW9D1eZo"}

# def get_results(): 
#     feed = 'df_hh_1_E7xPlIWq'
#     url = f'https://d.flashscore.ru.com/x/feed/{feed}'
#     response = requests.get(url=url, headers=headers)

#     data = response.text.split('¬')
#     data_list = [{}]

#     for item in data:
#         key = item.split('÷')[0]
#         value = item.split('÷')[-1]

#         if '~' in key:
#             data_list.append({key: value})
#         else: 
#             data_list[-1].update({key: value})
            

#     results = []
#     for game in data_list:
#         print(json.dumps(game, ensure_ascii=False, indent=2))


# if __name__ == '__main__':
#     get_results()

# Ниже код бота h2h

# app = Flask(__name__)
# headers = {"x-fsign": "SW9D1eZo"}

# def get_results(): 
#     feed = 'df_hh_1_6DkGCi44'
#     url = f'https://d.flashscore.ru.com/x/feed/{feed}'
#     response = requests.get(url=url, headers=headers)

#     data = response.text.split('¬')
#     data_list = [{}]

#     for item in data:
#         key = item.split('÷')[0]
#         value = item.split('÷')[-1]

#         if '~' in key:
#             data_list.append({key: value})
#         else: 
#             data_list[-1].update({key: value})

#     results = []
#     for game in data_list[:12]:
#         if 'KS' in game.keys() and game['KS'] == 'home' and list(game.keys()).index('KS') == len(game.keys()) - 1:
#             if game.get("KJ") and "Брайтон" in game.get("KJ"):
#               date = datetime.fromtimestamp(int(game.get('~KC'))).strftime('%d-%m-%Y %H:%M')
#               team_1 = game.get("KJ")
#               team_2 = game.get("KK")
#               score = f'{game.get("KU")} : {game.get("KT")}'
#               results.append({'date': date, 'team_1': team_1, 'team_2': team_2, 'score': score})
#     return results

# @app.route('/')
# def index():
#     results_data = get_results()
#     return render_template('index.html', results=results_data)

# @app.route('/results')
# def results():
#     results_data = get_results()
#     return render_template('results.html', results=results_data)

# if __name__ == '__main__':
#     app.run()

# Ниже код бота с датой


