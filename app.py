from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKry'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class yafguo_baseballplayersapp(db.Model):
    playerid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2}".format(self.playerid, self.first_name, self.last_name)

class playerForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])

@app.route('/')
def index():
    all_players = yafguo_baseballplayersapp.query.all()
    return render_template('index.html', players=all_players, pageTitle='Baseball Players')

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = playerForm()
    if form.validate_on_submit():
        player = yafguo_baseballplayersapp(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(player)
        db.session.commit()
        return "<h2> The baseball player is {0} {1}".format(form.first_name.data, form.last_name.data)

    return render_template('add_player.html', form=form, pageTitle='Add A New Friend')


    if __name__=='__main__':
        app.run(debug=True)
