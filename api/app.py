from flask import Flask, redirect, render_template, request, jsonify
import requests
from datetime import datetime

api_url = 'https://app.ylytic.com/ylytic/test'

response = requests.get(api_url, verify=False )

if response.status_code == 200:
    api_data = response.json()
    comments = api_data['comments']
else:
    print(f"Error: {response.status_code}")

app = Flask(__name__)


def returnNonNoneFilters(filters):
    new_dict = {}
    keys = list(filters.keys())
    values = list(filters.values())


    for i in range(len(values)):
        if values[i]['value'] is not None and values[i]['value'] != '':
            new_dict[keys[i]] = values[i]
    return new_dict


def filter_comments(comment, filters):
    all_conditions_met = True

    for key, value in filters.items():
        if key == 'search_text' and 'value' in value:
            if value['value'].lower() not in comment['text'].lower():
                all_conditions_met = False
                break
        elif key == 'search_author' and 'value' in value:
            if comment['author'].lower() != value['value'].lower():
                all_conditions_met = False
                break
        elif key == 'like_from' and 'value' in value:
            if comment['like'] < int(value['value']):
                all_conditions_met = False
                break
        elif key == 'like_to' and 'value' in value:
            if comment['like'] > int(value['value']):
                all_conditions_met = False
                break
        elif key == 'reply_from' and 'value' in value:
            if comment['reply'] < int(value['value']):
                all_conditions_met = False
                break
        elif key == 'reply_to' and 'value' in value:
            if comment['reply'] > int(value['value']):
                all_conditions_met = False
                break
        elif key == 'at_from' and 'value' in value:
            if datetime.strptime(comment['at'], '%a, %d %b %Y %H:%M:%S %Z') < datetime.strptime(value['value'], '%Y-%m-%d'):
                all_conditions_met = False
                break
        elif key == 'at_to' and 'value' in value:
            if datetime.strptime(comment['at'], '%a, %d %b %Y %H:%M:%S %Z') > datetime.strptime(value['value'], '%Y-%m-%d'):
                all_conditions_met = False
                break

    return all_conditions_met


@app.route('/', methods=['GET'])
def index():
    search_author = request.args.get('search_author')
    at_from = request.args.get('at_from')
    at_to = request.args.get('at_to')
    like_from = request.args.get('like_from')
    like_to = request.args.get('like_to')
    reply_from = request.args.get('reply_from')
    reply_to = request.args.get('reply_to')
    search_text = request.args.get('search_text')

    filters = {
        'search_author': {'value': search_author, 'usedIn': 'author'},
        'at_from': {'value': at_from, 'usedIn': 'at'},
        'at_to': {'value': at_to, 'usedIn': "at"},
        'like_from': {'value': like_from, 'usedIn': 'like'},
        'like_to': {'value': like_to, 'usedIn': 'like'},
        'reply_from': {'value': reply_from, 'usedIn': 'reply'},
        'reply_to': {'value': reply_to, 'usedIn': 'reply'},
        'search_text': {'value': search_text, 'usedIn': 'text'}
    }

    updated_filters = returnNonNoneFilters(filters)

    data_to_return = []
    if (search_author == None and at_from == None and at_to == None and like_from == None and like_to == None and reply_from == None and reply_to == None and search_text == None):
        return jsonify(comments)

    else:
        data_to_return = [comment for comment in comments if filter_comments(
            comment, updated_filters)]
        return jsonify(data_to_return)


if __name__ == "__main__":
    app.run(debug=True)
