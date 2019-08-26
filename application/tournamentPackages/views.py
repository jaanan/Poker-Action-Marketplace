from application import app, db, login_required
from flask import render_template, request, redirect, url_for, flash
from application.tournamentPackages.models import TournamentPackage, BoughtActionFromTournament
from application.auth.models import User
from flask_login import current_user
from application.tournamentPackages.forms import TournamentPackageForm
import re


@app.route('/tournaments/', methods=['GET'])
@login_required(role="USER")
def tournaments_index():
    tournaments = TournamentPackage.join_account_on_tournaments()

    return render_template('tournaments/list.html', tournaments = tournaments)

@app.route('/tournaments/new')
@login_required(role="USER")
def tournaments_form():
    return render_template('tournaments/new.html', form = TournamentPackageForm())

@app.route('/tournaments/', methods=['POST'])
@login_required(role="USER")
def tournaments_create():
    form = TournamentPackageForm(request.form)

    t = TournamentPackage(form.tournament.data, form.buyin.data, form.pcttobesold.data)
    t.pctLeft = form.pcttobesold.data

    t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tournaments_form"))

def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


@app.route('/tournaments/<tournament_id>', methods=["POST"])
@login_required(role="USER")
def tournaments_buy_percentage(tournament_id):
    t = TournamentPackage.query.get(tournament_id)
    user = User.query.get(t.account_id)

    onlynumbers = re.match("^[0-9]*$", request.form['text'])
    input = request.form['text']

    if input == '' or not onlynumbers:
        flash('Only numbers and the field cannot be empty!')
        return redirect(url_for('tournaments_index'))

    percentage = int(request.form['text'])
    if percentage < 0 or percentage > t.pctleft:
        flash("You need to buy more than 0 and less or equal what is for sale")
        return redirect(url_for('tournaments_index'))


    t.pctleft = t.pctleft - percentage

    boughtAction = BoughtActionFromTournament(percentage, user.username)
    boughtAction.buyer_id = current_user.id
    boughtAction.tournament_package_id = tournament_id

    db.session.add(boughtAction)
    db.session.commit()


    return redirect(url_for('tournaments_index'))

@app.route('/tournaments/bought', methods=["GET"])
@login_required(role="USER")
def show_purchased_tournaments():


    boughtTournaments = TournamentPackage.tournaments_bought_action_from(current_user.id)
    print(type(boughtTournaments))
    for row in boughtTournaments:
        print(type(row))
        print(row)
    return render_template('tournaments/bought.html', boughtTournaments = boughtTournaments)

    return True

@app.route('/tournaments/sold', methods=["GET"])
@login_required(role="USER")
def show_sold_tournaments():
    soldtournaments = TournamentPackage.tournaments_sold_action_from(current_user.id)
    for row in soldtournaments:
        print(row.tournament)
        for tour in row.buyers:
            print(tour)
    return render_template('tournaments/sold.html', soldTournaments = soldtournaments)

@app.route('/tournaments/sold/<tournament_id>/', methods=['POST'])
@login_required(role="USER")
def remove_tournament_from_sale(tournament_id):
    tournamentToDelete = TournamentPackage.query.get(tournament_id)
    referencesToDelete = BoughtActionFromTournament.query.filter_by(tournament_package_id = tournament_id)

    db.session.delete(tournamentToDelete)
    for reference in referencesToDelete:
        db.session.delete(reference)

    try:
        db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for('show_sold_tournaments'))

@app.route('/tournaments/statistics/', methods=["GET"])
@login_required(role="ADMIN")
def show_statistics():
    topBuyers = TournamentPackage.top_buyers()
    topBuyers.sort(key=lambda x: x[0], reverse=True)
    topSellers = TournamentPackage.top_sellers()
    topSellers.sort(key=lambda x: x[0], reverse=True)

    return render_template('tournaments/statistics.html', topBuyers = topBuyers, topSellers = topSellers)