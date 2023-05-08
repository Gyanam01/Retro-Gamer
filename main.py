from flask import Flask, render_template, request, flash, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
sess = Session()
login_manager = LoginManager()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.secret_key = 'super secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    login_manager.init_app(app)
    db.init_app(app)
    
    return app

class Users(UserMixin, db.Model):
    __tablename__ = "ID"
    id = db.Column(db.Integer,primary_key = True)
    identity = db.Column(db.String(250), unique = True,nullable = False)
    password = db.Column(db.String(250), nullable = False)
    question = db.Column(db.Integer ,nullable = False)
    
app = create_app()
app.config['SESSION_TYPE'] = 'filesystem'
with app.app_context():
    db.create_all()

sess.init_app(app)
    
    
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)
    

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        identity = request.form.get("PlayerID")
        pasword = request.form.get("password")
        
        user = Users.query.filter_by(identity = identity).first()
        if user==None:
            flash('PlayerID not found')
            return render_template("1.html")
        elif user.password == pasword:
            login_user(user)
            num = user.question
            if num == 1:
                return redirect(url_for('q1'))
            elif num == 2:
                return redirect(url_for('q2'))
            elif num == 3:
                return redirect(url_for('q3'))
            elif num == 4:
                return redirect(url_for('q4'))
            elif num == 5:
                return redirect(url_for('q5'))
            elif num == 6:
                return redirect(url_for('q6'))
            else:
                return redirect(url_for('complete'))
        else:
            flash('Password Incorrect')
            return render_template("1.html")
                
    return render_template("1.html")
    
@app.route("/register",  methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        identity = request.form.get("PlayerID")
        password = request.form.get("psw")
        if Users.query.filter_by(identity = identity).first():
            flash('PlayerID Already exists. Pick a New one')
            return render_template("2.html")
        user = Users(identity = identity,password = password,question = 1)
        db.session.add(user)
        db.session.commit()
        flash('Registration complete')
        return redirect(url_for('home'))
    return render_template("2.html")

@app.route("/q1",  methods=['GET', 'POST'])
def q1():
    if request.method == "POST":
        answer = request.form.get("Answer")
        if answer == 'A':
            current_user.question = 3
            db.session.commit()
            return redirect(url_for('q3'))
        else:
            flash('wrong answer')
            return render_template("q1.html")
    return render_template("q1.html")

@app.route("/q2",  methods=['GET', 'POST'])
def q2():
    if request.method == "POST":
        answer = request.form.get("Answer")
        if answer == 'C':
            current_user.question = 3
            db.session.commit()
            return redirect(url_for('q3'))
        else:
            flash('Wrong Answer')
            return render_template("q2.html")
    return render_template("q2.html")

@app.route("/q3",  methods=['GET', 'POST'])
def q3():
    if request.method == "POST":
        answer = request.form.get("Answer")
        if answer == 'B':
            current_user.question = 4
            db.session.commit()
            return redirect(url_for('q4'))
        else:
            flash('Wrong Answer')
            return render_template("q3.html")
    return render_template("q3.html")

@app.route("/q4",  methods=['GET', 'POST'])
def q4():
    if request.method == "POST":
        answer = request.form.get("Answer")
        if answer == 'B':
            current_user.question = 5
            db.session.commit()
            return redirect(url_for('q5'))
        else:
            current_user.question = 6
            db.session.commit()
            return redirect(url_for('q6'))
    return render_template("q4.html")

@app.route("/q5",  methods=['GET', 'POST'])
def q5():
    if request.method == "POST":
        answer = request.form.get("Answer")
        if answer == 'C':
            current_user.question = 0
            db.session.commit()
            return redirect(url_for('victory'))
        else:
            current_user.question = 0
            db.session.commit()
            return redirect(url_for('loose'))
    return render_template("q5.html")

@app.route("/q6",  methods=['GET', 'POST'])
def q6():
    if request.method == "POST":
        answer = request.form.get("Answer")
        if answer == 'C':
            current_user.question = 0
            db.session.commit()
            return redirect(url_for('lotse'))
        else:
            current_user.question = 0
            db.session.commit()
            return redirect(url_for('loss'))
    return render_template("q5.html")


@app.route("/victory",  methods=['GET', 'POST'])
def victory():
    return render_template("victory.html")

@app.route("/lotse",  methods=['GET', 'POST'])
def lotse():
    return render_template("lotse.html")
    
    
@app.route("/loss",  methods=['GET', 'POST'])
def loss():
    return render_template("loss.html")
    
@app.route("/loose",  methods=['GET', 'POST'])
def loose():
    return render_template("loose.html")
    
@app.route("/complete")
def complete():
    return render_template("complete.html")
    
@app.route("/AdminPanel",  methods=['GET', 'POST'])
def AdminPanel():
    if request.method == "POST":
        identity = request.form.get("Admin")
        password = request.form.get("psw")
        if identity=="Adminstrator@admi.com" and password=="12xa":
            return redirect(url_for('info'))
        else:
            flash("No Do not Attempt")
    return render_template("login.html")

@app.route("/info")
def info():
    return render_template("info.html", query = Users.query.all())
    

if __name__ == "__main__":
    app.run(debug=True)