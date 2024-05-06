from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Путь к файлу с логинами и паролями
USERS_FILE = 'users.txt'


# Функция для проверки авторизации
def check_auth(username, password):
    with open(USERS_FILE, 'r') as file:
        users = file.readlines()

    for user in users:
        user_data = user.strip().split(':')
        if len(user_data) == 2:
            stored_username, stored_password = user_data
            if stored_username == username and stored_password == password:
                return True
    return False


# Страница авторизации
@app.route('/')
def login():
    return render_template('login.html')


# Обработка отправки формы на авторизацию
@app.route('/', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if check_auth(username, password):
        return 'Вы успешно авторизовались!'
    else:
        return 'Неверный логин или пароль.'


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        with open(USERS_FILE, 'a') as file:
            file.write(f'{username}:{password}\n')

        return 'Вы успешно зарегистрировались!'

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)