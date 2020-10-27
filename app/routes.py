from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AddMovieForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Movie
from datetime import datetime, timezone


@app.route('/')
@app.route('/index')
def index():
    movies = Movie.query.all()
    now = datetime.utcnow()
    return render_template('index.html', title='Home', movies=movies, now=now)


@app.route('/index/<value>')
def sort(value):
    if value in ('0','1','2'):
        if int(value) == 2:
            movies = Movie.query.order_by(Movie.timestamp.desc()).all()
        else:
            movies = Movie.query.all()
            movies_dic = {}
            for movie in movies:
                if int(value) == 0:
                    movies_dic[movie] =  movie.get_fans()
                elif int(value) == 1:
                    movies_dic[movie] =  movie.get_haters()
                movies = {k: v for k, v in sorted(movies_dic.items(), key=lambda item: item[1], reverse=True)}.keys()
        now = datetime.utcnow()
        return render_template('index.html', title='Home', movies=movies, now=now)
    else:
        print('happend')
        return redirect(url_for('index'))


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        #flash('You are already logged in')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        movie = Movie(title=form.title.data, author=user, description=form.description.data)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added succesfully!')
        return redirect(url_for('index'))
    return render_template('add_movie.html', title='Post a Movie', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    movies = Movie.query.filter_by(author=user).all()
    now = datetime.utcnow()
    return render_template('user.html', title='Home', movies=movies, now=now, this_user=username)


@app.route('/user/<username>/<value>')
def u_sort(username, value):
    if value in ('0','1','2'):
        user = User.query.filter_by(username=username).first_or_404()
        if int(value) == 2:
            movies = Movie.query.filter_by(author=user).order_by(Movie.timestamp.desc()).all()
        else:
            movies = Movie.query.filter_by(author=user).all()
            movies_dic = {}
            for movie in movies:
                if int(value) == 0:
                    movies_dic[movie] =  movie.get_fans()
                elif int(value) == 1:
                    movies_dic[movie] =  movie.get_haters()
            movies = {k: v for k, v in sorted(movies_dic.items(), key=lambda item: item[1], reverse=True)}.keys()
        now = datetime.utcnow()
        return render_template('user.html', title='Home', movies=movies, now=now, this_user=username)
    else:
        return redirect(url_for('user', username = username))


@app.route('/like/<moviename>')
@login_required
def like(moviename):
    movie = Movie.query.filter_by(title=moviename).first_or_404()
    if movie.author == current_user:
        flash('You cannot like your own movie!')
        #return redirect(url_for('index'))
    else:
        if not current_user.like(movie):
            flash('Cant like more than once!')
        db.session.commit()
    #return redirect(url_for('index'))
    return redirect(request.referrer)


@app.route('/unlike/<moviename>')
@login_required
def unlike(moviename):
    movie = Movie.query.filter_by(title=moviename).first_or_404()
    if movie.author == current_user:
        flash('You cannot unlike your own movie!')
    else:
        if not current_user.unlike(movie):
            flash('Cant unlike something you have not liked in the first place!')
        db.session.commit()
    return redirect(request.referrer)


@app.route('/hate/<moviename>')
@login_required
def hate(moviename):
    movie = Movie.query.filter_by(title=moviename).first_or_404()
    if movie.author == current_user:
        flash('Why hate your own movie?!?')
        #return redirect(url_for('index'))
    else:
        if not current_user.hate(movie):
            flash('One hate vote is enough')
        db.session.commit()
    #return redirect(url_for('index'))
    return redirect(request.referrer)


@app.route('/unhate/<moviename>')
@login_required
def unhate(moviename):
    movie = Movie.query.filter_by(title=moviename).first_or_404()
    if movie.author == current_user:
        flash('You cannot unhate your own movie!')
    else:
        if not current_user.unhate(movie):
            flash('Cant unhate something you have not hated in the first place!')
        db.session.commit()
    return redirect(request.referrer)
