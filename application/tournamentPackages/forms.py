from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

class TournamentPackageForm(FlaskForm):
    tournament = StringField('Tournament name')
    buyin = IntegerField('BuyIn')
    pcttobesold = IntegerField('% To Sell')
    pctleft = IntegerField('pctleft')

    class Meta:
        csrf = False