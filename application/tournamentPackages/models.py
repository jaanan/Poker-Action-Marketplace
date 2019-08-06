from application import db
from application.models import Base
from sqlalchemy.sql import text
from flask_login import current_user

class TournamentPackage(Base):
    tournament = db.Column(db.String(144), nullable=False)
    buyIn = db.Column(db.Integer, nullable=False)
    pctToBeSold = db.Column(db.Integer, nullable=False)
    pctLeft = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)


    def __init__(self, tournament, buyIn, pctToBeSold):
        self.tournament = tournament
        self.buyIn = buyIn
        self.pctToBeSold = pctToBeSold
        self.pctLeft = pctToBeSold
        self.user = ''
        self.userid = ''


    @staticmethod
    def join_account_on_tournaments():
        stmt = text("SELECT * FROM tournament_package"
                    " LEFT JOIN account on tournament_package.account_id = account.id")
        res = db.engine.execute(stmt)


        tournaments = []
        for row in res:
            tournament = TournamentPackage(row[3], row[4], row[5])
            tournament.user = row[-2]
            tournament.id = row[0]
            tournament.userid = row[7]
            tournament.pctLeft = row[6]
            if tournament.userid == current_user.id:
                continue
            tournaments.append(tournament)

        return tournaments

    @staticmethod
    def tournaments_bought_action_from(id):
        stmt = text("SELECT bought_action_from_tournament.seller_name, tournament_package.tournament, bought_action_from_tournament.actionBoughtPct FROM account"
                " LEFT JOIN bought_action_from_tournament ON account.id = bought_action_from_tournament.buyer_id"
                " LEFT JOIN tournament_package ON bought_action_from_tournament.tournament_package_id = tournament_package.id"
                " WHERE bought_action_from_tournament.buyer_id = {}".format(id))

        # tournament_package.buyIn,

        print('ENSIMMAINEN ETAPPI!')
        res = db.engine.execute(stmt)
        print('TOINEN ETAPPI')
        asAnArray = []
        for row in res:
            temp = list(row)
            asAnArray.append(temp)

        return asAnArray


class BoughtActionFromTournament(Base):
    tournament_package_id = db.Column(db.Integer, db.ForeignKey('tournament_package.id'), nullable=False)
    seller_name = db.Column(db.String(144), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    actionBoughtPct = db.Column(db.Integer, nullable=False)

    def __init__(self, actionBoughtPct, seller_name):
        self.actionBoughtPct = actionBoughtPct
        self.seller_name = seller_name