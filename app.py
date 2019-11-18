from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)


app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class yafguo_baseballplayersapp(db.Model):
    playerid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2}".format(self.id, self.first_name, self.last_name)

class PlayerForm(FlaskForm):
    playerid = IntegerField('Player ID:')
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])


@app.route('/')
def index():
    all_players = yafguo_baseballplayersapp.query.all()
    return render_template('index.html', players=all_players, pageTitle='Baseball players')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{}%".format(search_value)
        results = yafguo_baseballplayersapp.query.filter(or_(yafguo_baseballplayersapp.first_name.like(search),yafguo_baseballplayersapp.last_name.like(search))).all()
        return render_template('index.html', players=results,pageTitle='Baseball Player', legend="Search Results")
    else:
        return redirect('/')


@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        player = yafguo_baseballplayersapp(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(player)
        db.session.commit()
        return redirect('/')

    return render_template('add_player.html', form=form, pageTitle='Add A New Player')


@app.route('/delete_player/<int:player_id>', methods=['GET','POST'])
def delete_player(player_id):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        player = yafguo_baseballplayersapp.query.get_or_404(player_id)
        db.session.delete(player)
        db.session.commit()
        return redirect("/")

    else: #if it's a GET request, send them to the home page
        return redirect("/")

@app.route('/player/<int:player_id>', methods=['GET','POST'])
def get_player(player_id):
    player = yafguo_baseballplayersapp.query.get_or_404(player_id)
    return render_template('player.html', form=player, pageTitle='Player Details', legend="Player Details")

@app.route('/player/<int:player_id>/update', methods=['GET','POST'])
def update_player(player_id):
    player = yafguo_baseballplayersapp.query.get_or_404(player_id)
    form = PlayerForm()

    if form.validate_on_submit():
        player.first_name = form.first_name.data
        player.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('get_player', player_id=player.playerid))
    #elif request.method == 'GET':
    form.playerid.data=player.playerid
    form.first_name.data = player.first_name
    form.last_name.data = player.last_name
    return render_template('add_player.html', form=form, pageTitle='Update Post',
                            legend="Update A Player")


if __name__ == '__main__':
    app.run(debug=True)
