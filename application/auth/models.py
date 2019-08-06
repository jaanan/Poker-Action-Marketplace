from application import db
from application.models import Base

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    tournaments = db.relationship('TournamentPackage', backref='account', lazy=True)
    #buypackages = db.relationship('BoughtActionFromTournament', backref='account', lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymoys(self):
        return False

    def is_authenticated(self):
        return True