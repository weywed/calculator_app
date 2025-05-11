from flask import Flask, render_template, request
from models import db, Operation
import os

app = Flask(__name__)

# Настройки для подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db.init_app(app)

# Создание всех таблиц, если их нет
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    expression = ""  # Начальное значение для выражения
    if request.method == "POST":
        expression = request.form.get("expression")  # Получаем выражение с формы
        try:
            # Выполняем вычисления
            result = str(eval(expression))  
            # Сохраняем операцию в БД
            new_op = Operation(expression=expression, result=result)
            db.session.add(new_op)
            db.session.commit()
        except Exception as e:
            result = f"Ошибка: {e}"  # В случае ошибки выводим сообщение
    return render_template("index.html", result=result, expression=expression)  # Передаем выражение и результат

@app.route("/history")
def history():
    # Загружаем операции из БД, отсортированные по времени
    operations = Operation.query.order_by(Operation.timestamp.desc()).all()
    return render_template("history.html", operations=operations)  # Передаем операции для отображения

if __name__ == "__main__":
    app.run(debug=True)  # Запуск приложения
