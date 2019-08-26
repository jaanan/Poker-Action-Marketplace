from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from application import db, app
from application.auth.models import User
from application.auth.forms import LoginForm, registerForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())


    form = LoginForm(request.form)


    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form=form, error = "No such username or password")

    print("User:" + user.name + "was recognized")

    login_user(user)
    return redirect(url_for("tournaments_create"))

@app.route('/auth/logout')
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/auth/register', methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = registerForm())


    form = registerForm(request.form)

    user = User(form.name.data, form.username.data, form.password.data)

    db.session().add(user)
    db.session().commit()

    return redirect(url_for("tournaments_index"))
