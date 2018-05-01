#!/usr/bin/python2.7

# Third-party imports.
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, LoginManager, UserMixin
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.exc import IntegrityError

# Local imports.

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////mnt/c/Users/Amanda/Desktop/spring-2018/is211/"
    "IS211_Assignment13/hw13.db")
app.config["SECRET_KEY"] = "thisissecret"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/signin"

@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    @classmethod
    def get_user(cls, username, password):
        return cls.query.filter_by(username=username, password=password).first()

        
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    
class Quizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String)
    num_questions = db.Column(db.Integer)
    date = db.Column(db.String)

    
class QuizScores(db.Model):
    __table_args__ = (
        PrimaryKeyConstraint("student_id", "quiz_id"),
    )

    student_id = db.Column(db.Integer, ForeignKey("students.id"))
    quiz_id = db.Column(db.Integer, ForeignKey("quizzes.id"))
    score = db.Column(db.Integer)


@app.route("/")
def index():
    return redirect(url_for("signin"))


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Validate the log-in and direct to the dashboard after logging in.
        form = request.form
        user = User.get_user(form["username"], form["password"])
        print user
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))
        # The user was invalid, so simply re-direct to the form.
        else:
            return redirect(url_for("signin"))
    else:
        return render_template("signin.html")


@app.route("/dashboard")
def dashboard():
    # Create the page with the contents of the database.
    return render_template("dashboard.html",
                           students=Students.query.all(),
                           quizzes=Quizzes.query.all())


@app.route("/student/add", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        if all(request.form.to_dict().values()):
            # Add in the user.
            db.session.add(Students(**request.form.to_dict()))
            db.session.commit()
            # Return to the dashboard.
            return redirect(url_for("dashboard"))
        # A field was missing.
        else:
            return render_template("student.html", error=True)
    else:
        return render_template("student.html")


@app.route("/quiz/add", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        # Add in the user.
        if all(request.form.to_dict().values()):
            db.session.add(Quizzes(**request.form.to_dict()))
            db.session.commit()
            # Return to the dashboard.
            return redirect(url_for("dashboard"))
        # A field was missing.
        else:
            return render_template("quiz.html", error=True)
    else:
        return render_template("quiz.html")


@app.route("/student/<id>")
def scores(id):
    scores = QuizScores.query.filter_by(student_id=id).all()
    return render_template("scores.html", scores=scores)


@app.route("/results/add", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        # Add in the user.
        print request.form.to_dict()
        if all(request.form.to_dict().values()):
            try:
                db.session.add(QuizScores(**request.form.to_dict()))
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return render_template("result.html", failed=True,
                                       students=Students.query.all(),
                                       quizzes=Quizzes.query.all())
            # Return to the dashboard.
            return redirect(url_for("dashboard"))
        # A field was missing.
        else:
            return render_template("result.html", error=True,
                                   students=Students.query.all(),
                                    quizzes=Quizzes.query.all())
    else:
        # Create the page with the contents of the database.
        return render_template("result.html",
                               students=Students.query.all(),
                               quizzes=Quizzes.query.all())


if __name__ == "__main__":
    app.run(debug=True)
