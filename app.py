from flask import Flask,render_template,url_for,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SECRET_KEY'] = "yoursecret_key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self) -> str: 
        return f"{self.sno} - {self.title} - {self.description}"


@app.route('/',methods=['POST','GET'])
def hello_world():
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)

@app.route('/add',methods=['POST','GET'])
def add_todo():
    if request.method =='POST':
        title=request.form['title']
        description=request.form['description']
        todo=Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        flash("Todo added successfully")
        return redirect(url_for('hello_world'))
    return render_template('add_todo.html')

@app.route('/update/<int:sno>', methods=['POST','GET'])
def update(sno):
    if request.method == 'POST':
        title=request.form['title']
        description=request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.description=description
        db.session.add(todo)
        db.session.commit()
        flash("Todo updated successfully")
        return redirect(url_for('hello_world'))
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    flash("Todo deleted successfully")
    return redirect(url_for('hello_world'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__=="__main__":
    app.run(debug=True,port=8000)