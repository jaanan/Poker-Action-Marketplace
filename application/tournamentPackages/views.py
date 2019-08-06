from application import app, db
from flask import render_template, request, redirect, url_for
from application.tournamentPackages.models import TournamentPackage, BoughtActionFromTournament
from application.auth.models import User
from flask_login import login_required, current_user
from application.tournamentPackages.forms import TournamentPackageForm


@app.route('/tournaments/', methods=['GET'])
@login_required
def tournaments_index():
    tournaments = TournamentPackage.join_account_on_tournaments()
    tournaments.sort(key = lambda x: x.user, reverse=True)

    return render_template('tournaments/list.html', tournaments = tournaments)

@app.route('/tournaments/new')
@login_required
def tournaments_form():
    return render_template('tournaments/new.html', form = TournamentPackageForm())

@app.route('/tournaments/', methods=['POST'])
@login_required
def tournaments_create():
    form = TournamentPackageForm(request.form)
    t = TournamentPackage(form.tournament.data, form.buyIn.data, form.pctToBeSold.data)
    t.pctLeft = form.pctToBeSold.data

    t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tournaments_index"))

@app.route('/tournaments/<tournament_id>', methods=["POST"])
@login_required
def tournaments_buy_percentage(tournament_id):
    t = TournamentPackage.query.get(tournament_id)
    user = User.query.get(t.account_id)
    percentage = int(request.form['text'])

    t.pctLeft = t.pctLeft - percentage

    boughtAction = BoughtActionFromTournament(percentage, user.username)
    boughtAction.buyer_id = current_user.id
    boughtAction.tournament_package_id = tournament_id

    db.session.add(boughtAction)
    db.session.commit()


    return redirect(url_for('tournaments_index'))

@app.route('/tournaments/bought', methods=["GET"])
@login_required
def show_purchased_tournaments():


    boughtTournaments = TournamentPackage.tournaments_bought_action_from(current_user.id)
    print(type(boughtTournaments))
    for row in boughtTournaments:
        print(type(row))
        print(row)
    return render_template('tournaments/bought.html', boughtTournaments = boughtTournaments)

    return True

@app.route('/tournaments/sold', methods=["GET"])
@login_required
def show_sold_tournaments():
    return True

