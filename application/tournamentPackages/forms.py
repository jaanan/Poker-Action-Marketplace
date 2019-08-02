from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

class TournamentPackageForm(FlaskForm):
    tournament = StringField('Tournament name')
    buyIn = IntegerField('BuyIn')
    pctToBeSold = IntegerField('pctToBeSold')
    pctLeft = IntegerField('pctLeft')

    class Meta:
        csrf = False