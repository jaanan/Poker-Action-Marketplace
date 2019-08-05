from application import db
from application.models import Base

class TournamentPackage(Base):

    # POISTA ID JA DATET
    #id = db.Column(db.Integer, primary_key=True)
    tournament = db.Column(db.String(144), nullable=False)
    buyIn = db.Column(db.Integer, nullable=False)
    pctToBeSold = db.Column(db.Integer, nullable=False)
    pctLeft = db.Column(db.Integer, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    #date_created = db.Column(db.DateTime, default= db.func.current_timestamp())
    #date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, tournament, buyIn, pctToBeSold):
        self.tournament = tournament
        self.buyIn = buyIn
        self.pctToBeSold = pctToBeSold
        self.pctLeft = pctToBeSold