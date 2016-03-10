# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from kanye_display.extensions import login_manager
from kanye_display.public.forms import LoginForm
from kanye_display.user.forms import RegisterForm
from kanye_display.user.models import User
from kanye_display.utils import flash_errors
from pymongo import MongoClient
import json
import random
blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    tweets = ''
    client = MongoClient()
    x = []
    tones = []
    tweet = {}    
    for i in client.crawler3.tweets.find().sort([("date",-1)]).limit(2):
	ids = []
	x = []
	for v in i.get('tone').get('document_tone').get('tone_categories'):
		scores = []
		for k, t in enumerate(v.get('tones')):
		
			scores.append(t.get('score'))		 
		ids.append(str(random.randint(0, 15000)) + '-id')	
		x.append(scores)
	tones.append({'ids':ids, 'scores':x, 'tweet':i})
	i.pop('tone')        
    return render_template('public/home.html', tones=tones)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)
