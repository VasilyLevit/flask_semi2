'''Семинар 2'''

from flask import Flask, abort, flash, make_response, redirect, render_template, request, url_for
from pathlib import PurePath, Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def main():    
    return render_template('index.html')

'''Задание No1
Создать страницу, на которой будет кнопка "Нажми меня", при нажатии на которую будет переход на другую страницу с приветствием пользователя по имени.'''

@app.route('/hello_friend')
def hello(name = "Друг"):
    return render_template('hello.html', name=name)

'''Задание No2
Создать страницу, на которой будет изображение и ссылка на другую страницу, на которой будет отображаться форма для загрузки изображений.'''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # проверка на метод запроса POST
    if request.method == 'POST':
        file = request.files.get('file') #  Получив post с файлом, сохраняем его в переменной file 
        file_name = secure_filename(file.filename) # экранирование для исключения проблем с плохими именами используем функцию secure_filename
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        # сохранение файла в операционной системе в папку uploads с именем file_name
        return f"Файл {file_name} загружен на сервер"
    return render_template('upload.html')

'''Задание No3
Создать страницу, на которой будет форма для ввода логина и пароля
При нажатии на кнопку "Отправить" будет произведена проверка соответствия логина и пароля и переход на страницу приветствия пользователя или страницу с ошибкой.'''

#Создадим некое подобие базы данных в виде словаря
user = {
    'login': 'Vasia',
    'pass': '1234'
}
@app.route('/autorisation', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login') #  Получив post с логином, сохраняем его в переменной login
        password = request.form.get('password')
        if login == user['login'] and password == user['pass']:
            return f"Приветствую {login}, вход разрешен"        
    return render_template('credentials.html') # эта строка сработает на GET и вызовет шаблон ввода учетных данных

'''Задание No4
Создать страницу, на которой будет форма для ввода текста и кнопка "Отправить"
При нажатии кнопки будет произведен подсчет количества слов в тексте и переход на страницу с результатом.'''

@app.route('/task4', methods=['GET', 'POST'])
def text_input():
    if request.method == 'POST':
        text = request.form.get('note')
        return f"Количество слов = {len(text.split())}"        
    return render_template('input_txt.html')


'''Задание No5
Создать страницу, на которой будет форма для ввода двух чисел и выбор операции (сложение, вычитание, умножение или деление) и кнопка "Вычислить".
При нажатии на кнопку будет произведено вычисление результата выбранной операции и переход на страницу с результатом.'''

@app.route('/task5', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        a = int(request.form.get('num1'))
        b = int(request.form.get('num2'))
        operat = request.form.get('operation')
        if operat == 'add':
            return f"Результат = {a + b}"
        if operat == 'subtract':
            return f"Результат = {a - b}"
        if operat == 'multiplay':
            return f"Результат = {a * b}"
        if operat == 'divide' and b !=0:
            return f"Результат = {a / b}"
        
    return render_template('calc.html')

'''Задание No6
Создать страницу, на которой будет форма для ввода имени и возраста пользователя и кнопка "Отправить"
При нажатии на кнопку будет произведена проверка возраста и переход на страницу с результатом или на страницу с ошибкой в случае некорректного возраста.'''

@app.route('/person', methods=['GET', 'POST'])
def person_age():
    if request.method == 'POST':
        name = request.form.get('name')
        age = int(request.form.get('age'))
        if age < 18:
            abort(403)
        return f"Приветствую {name}"        
    return render_template('person.html')

@app.errorhandler(403)
def page_not_found(e):
    #функция для обработки ошибок
    context = {
        'title': 'Доступ запрещен',
        'url': request.base_url,
    }
    return render_template('403.html', **context), 403

'''Задание No7
Создать страницу, на которой будет форма для ввода числа и кнопка "Отправить". При нажатии на кнопку будет произведено перенаправление (redirect) на страницу с результатом, где будет выведено введенное число и его квадрат.'''

@app.route('/redirect/')
def redirect_to_index():
    # redirect перенаправляет на другой роутер. При входе на страницу redirect срабатывает 303 код о перенаправлении на другую страницу.
    return redirect(url_for('main'))

@app.route('/square')
def square_num():
    return

'''Задание No8
Создать страницу, на которой будет форма для ввода имени и кнопка "Отправить". При нажатии на кнопку будет произведено перенаправление на страницу с flash сообщением, где будет выведено "Привет, {имя}!".'''

app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Проверка данных формы
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('form'))
        # Обработка данных формы
        flash('Форма успешно отправлена!', 'success') 
        return redirect(url_for('form'))
    return render_template('flash_form.html')

'''Задание No9
Создать страницу, на которой будет форма для ввода имени и электронной почты. При отправке которой будет создан cookie файл с данными пользователя.
Также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя. На странице приветствия должна быть кнопка "Выйти".
При нажатии на кнопку будет удален cookie файл с данными пользователя и произведено перенаправление на страницу ввода имени и электронной почты.'''

@app.route('/home_task', methods=['GET', 'POST'])
def my_login():
    if request.method == 'POST':
        # Получим значения имени и почты из формы
        name = request.form.get['name']
        email = request.form.get['email']
        # перенаправление на страницу приветствия
        response = make_response(redirect('/greeting'))
        response.set_cookie('user_name', name)
        response.set_cookie('user_email', email)

        return response

        # return redirect(url_for('hello', name=name))        
    return render_template('person2.html')

@app.route('/greeting')
def greet():
    user_name = request.cookies.get('user_name')
    # проверка на наличие данных в куках
    if user_name:
        return render_template('hello.html', name=user_name)
    return redirect('/')

@app.route('/logout')
def logout():    
    response = make_response(redirect('/'))
    response.delete_cookie('user_name')
    response.delete_cookie('user_email')
    return response

if __name__ == '__main__':
    app.run(debug=True)