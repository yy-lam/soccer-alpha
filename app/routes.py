from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.forms import *
from app.models import *
from werkzeug.urls import url_parse

import json, requests
import numpy as np
import pickle

from data import Match


@app.route('/')
@app.route('/index')
#@login_required
def home():
    return render_template('pages/home.html')


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        # all fields should be valid otherwised skipped
        # flash('Login requested for user')
        user = User.query.filter_by(username=form.username.data).first()
        if user == None or not user.check_password(form.password.data):
            flash('Username/Password is invalid') 
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if next_page == None or url_parse(next_page).netlog != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('forms/login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('User Logged Out')
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User is registered and automatically logged in!')
        login_user(user)
        return redirect(url_for('home'))
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm()
    return render_template('forms/forgot.html', form=form)


@app.route('/test')
def test():
    #with open('data/fixtures.json', 'r') as f:
    #    fixtures = json.load(f)['api']['fixtures']

    url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/next/8"

    querystring = {"timezone":"Europe/London"}

    headers = {
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
        'x-rapidapi-key': "9a4cc675c7mshdaa84f5b192909ap1f9979jsn18ef7493b7db"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    fixtures = response.json()['api']['fixtures']
    
    return render_template('pages/match.html', fixtures=fixtures, N=len(fixtures))

@app.route('/predict', methods=['GET' ,'POST'])
def predict():
    home = request.args.get('home')
    away = request.args.get('away')
    match = Match(str(home), str(away))
    prediction = match.predict()
    pred_text = "Draw"
    if prediction == 0:
        pred_text = "Lose"
    elif prediction == 1:
        pred_text = "Win"
    p_lose, p_win, p_draw = np.round( 100 * match.predict_proba(), 1) 
    return jsonify({'prediction': pred_text,
                   'p_win': str(p_win),
                   'p_lose': str(p_lose),
                   'p_draw': str(p_draw)})
