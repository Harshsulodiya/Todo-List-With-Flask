from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        if title and desc:
            new_todo = Todo(title=title, desc=desc)
            db.session.add(new_todo)
            db.session.commit()
        # Optionally, you can redirect after POST to avoid resubmission:
        # return redirect(url_for('index'))
        
    # This query will run for both GET and POST requests
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)



# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         title = request.form['title']
#         desc = request.form['desc']
#         if title and desc:
#             new_todo = Todo(title=title, desc=desc)
#             db.session.add(new_todo)
#             db.session.commit()
#     # return redirect(url_for('index')) 
        
#         allTodo = Todo.query.all()
#     # print(allTodo)
#     # alltodo = Todo.query.order_by(Todo.date_created.desc()).all()
#     return render_template('index.html', allTodo=allTodo)

# @app.route("/update/<int:sno>")
# def update(sno):
#     todo = Todo.query.filter_by(sno=sno).first()
#     return render_template('update.html', todo=todo)


@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get(sno)
    if not todo:
        abort(404, description="Todo not found")

    if request.method == "POST":
        todo.title = request.form.get("title", todo.title)
        todo.desc = request.form.get("desc", todo.desc)
        db.session.commit()
        return redirect(url_for("index"))  # Correct endpoint name

    return render_template("update.html", todo=todo)

    # Always return the update form for GET requests
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))



# @app.route('/')
# def hello_world():
#     return render_template('index.html')

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         title = request.form['title']
#         desc = request.form['desc']
#         if title and desc:
#             new_todo = Todo(title=title, desc=desc)
#             db.session.add(new_todo)
#             db.session.commit()
#         return redirect(url_for('index'))
    
#     all_todos = Todo.query.order_by(Todo.date_created.desc()).all()
#     return render_template('index.html', all_todos=all_todos)



@app.route("/products")
def products():
    return 'this is products pages'

if __name__ == "__main__":
    app.run(debug=True, port=8000)