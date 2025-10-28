import sqlite3
from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm, CSRFProtect
from flask_login import login_required, current_user, LoginManager, UserMixin, logout_user
from wtforms import StringField, SubmitField, PasswordField, DateField, TelField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "xoLBbyGovMe0Z1CiCKqWODomAtpeRSLj" #gen random key 
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class SignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    DoB = DateField("Date of Birth", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = TelField("Mobile Number", validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField("Create Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Sign up")


# --------------------- Database ---------------------
def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

connect = sqlite3.connect('instance/database.db')
connect.execute(
    "CREATE TABLE IF NOT EXISTS users (first_name TEXT, \
        last_name TEXT, DoB TEXT, email TEXT NOT NULL UNIQUE, phone TEXT, password TEXT)")



# ----------------- User Model and User loader ----------------
class User(UserMixin):
    def __init__(self, id, first_name, last_name, DoB, email, phone, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.DoB = DoB
        self.email = email
        self.phone = phone
        self.password = password

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

# ----- callbacks ---- 
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():

    return redirect(url_for("index"))


# --------------------- Routes ---------------------
@app.route("/")
def home():
    return index()


@app.route("/index", methods=["GET", "POST"])
def index():
    form = LoginForm()
    message = None

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            #flash("✅ Welcome, {user['first_name']}!") 
            return render_template("dashboard.html", user=user)
        else:
            flash("Invalid email or password.", category = "wrong")

    return render_template("index.html", form=form, error=message)


@app.route("/Signup", methods=["GET", "POST"])
def Signup():
    form = SignupForm()
    message = None

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        DoB = form.DoB.data
        email = form.email.data
        phone = form.phone.data
        password = form.password.data

        hashed_password = generate_password_hash(password)


        with sqlite3.connect("instance/database.db") as users:
            cur = users.cursor()
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))

            existing_user = cur.fetchone()
            if existing_user:
                flash("Email already registered. Please use another email.", "wrong")
                return render_template("Signup.html", form=form, error=message)

            cur.execute("""
                INSERT INTO users (
                                    first_name,
                                    last_name,
                                    DoB ,
                                    email ,
                                    phone ,
                                    password 
                                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (first_name, last_name, DoB, email, phone, hashed_password))
            users.commit()
        flash( "Sign up successful! Please sign in.", "success")
        return render_template("index.html", form=LoginForm(), error=message)


    return render_template("Signup.html", form=form, error=message)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


if __name__ == "__main__":
    app.run(debug=True)