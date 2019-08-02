from application import app, db
from flask import render_template, request, redirect, url_for
from application.tournamentPackages.models import TournamentPackage
from flask_login import login_required, current_user
from application.tournamentPackages.forms import TournamentPackageForm

@app.route('/tournaments/', methods=['GET'])
def tournaments_index():
    return render_template('tournaments/list.html', tournaments = TournamentPackage.query.all())

@app.route('/tournaments/new')
def tournaments_form():
    return render_template('tournaments/new.html', form = TournamentPackageForm())

@app.route('/tournaments/', methods=['POST'])
def tournaments_create():
    form = TournamentPackageForm(request.form)
    t = TournamentPackage(form.tournament.data, form.buyIn.data, form.pctToBeSold.data)
    t.pctLeft = form.pctToBeSold.data

    #t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tournaments_index"))

@app.route('/tournaments/<tournament_id>', methods=["POST"])
def tournaments_buy_percentage(tournament_id):
    t = TournamentPackage.query.get(tournament_id)

    percentage = int(request.form['text'])

    t.pctLeft = t.pctLeft - percentage
    db.session.commit()

    return redirect(url_for('tournaments_index'))