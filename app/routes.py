from flask import render_template,flash,redirect,url_for,request
from app import app
from app.forms import Loginform
from app.models import  User,Post
from flask_login import current_user, login_user,logout_user,login_required
from app import db
import sqlalchemy as sa
from urllib.parse import urlsplit
@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html",title="Home",posts=Post.body)

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = Loginform()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username==form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for("login"))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc!="":
            next_page = url_for("index")
        return redirect(url_for(next_page))
    return render_template("login.html",title="Sign In",form=form)

@app.route("/logout")
def logout():
    logout_user()
    redirect(url_for("index"))