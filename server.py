import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
today = str(datetime.today())
COST = 3


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # Checks if the email address is listed,
    # otherwise redirects to the index page with an error message.
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               today=today)
    except IndexError:
        return render_template('index.html',
                               message='Unknown email address')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               today=today)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Creates a counter to check that the user
    # can buy a maximum of 12 places in several times
    if not competition['name'] in club:
        club[competition['name']] = int(0)

    # Checks that the competition date is before today
    if competition['date'] < today:
        flash('This competition is no more available.')

    # Checks that the number of required places is positive
    elif placesRequired <= 0:
        flash("Please, enter a positive number!")

    # Checks if a club try to purchase more than 12 places
    elif placesRequired+club[competition['name']] > 12:
        flash("You cannot require more than 12 places per competition")

    # Checks if a club has enough points to purchase places
    elif int(club['points']) < (COST*placesRequired):
        flash("Not enough points to require this number of places!")
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired

    # Updates club points
        club['points'] = int(club['points']) - (COST*placesRequired)

    # Updates the counter to check that the user
    # can buy a maximum of 12 places in several times
        club[competition['name']] += placesRequired
        flash('Great-booking complete!')
    return render_template('welcome.html',
                           club=club,
                           competitions=competitions,
                           today=today)


# TODO: Add route for points display
@app.route('/board')
def board():
    return render_template('board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
