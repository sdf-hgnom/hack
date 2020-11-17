import json
from flask import Flask, request, Response

app = Flask(__name__)
stats = {
    'attempts': 0,
    'success': 0,
}


@app.route('/')
def hello():
    return f'Hello !! {stats["attempts"]} {stats["attempts"]}'


@app.route('/auth', methods=['POST'])
def auth():
    stats['attempts'] += 1
    data = request.json
    login = data['login']
    password = data['password']
    print(login, password)

    with open('user.json', 'rt', encoding='utf-8') as file_json:
        users = json.load(file_json)

    if login in users and users[login] == password:
        status_code = 200
        stats['success'] += 1
    else:
        status_code = 401

    return Response(status=status_code)


if __name__ == '__main__':
    app.run(debug=True)
