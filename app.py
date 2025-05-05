
from flask import Flask, render_template, request
from models import db, Operation
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        expression = request.form.get("expression")
        try:
            result = str(eval(expression))
            new_op = Operation(expression=expression, result=result)
            db.session.add(new_op)
            db.session.commit()
        except Exception as e:
            result = f"Ошибка: {e}"
    return render_template("index.html", result=result)

@app.route("/history")
def history():
    operations = Operation.query.order_by(Operation.timestamp.desc()).all()
    return render_template("history.html", operations=operations)

if __name__ == "__main__":
    app.run(debug=True)
