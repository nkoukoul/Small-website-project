from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
)


hates = db.Table('hates',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    movies = db.relationship('Movie', backref='author', lazy='dynamic')
    liked = db.relationship('Movie', secondary=likes, backref=db.backref("fans", lazy='dynamic'), lazy='dynamic')
    hated = db.relationship('Movie', secondary=hates, backref=db.backref("haters", lazy='dynamic'), lazy='dynamic')
    

    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def like(self, movie):
        if not self.does_like(movie):
            self.liked.append(movie)
            if self.does_hate(movie):
                self.unhate(movie)
            return True
        else:
            return False
    
    def unlike(self, movie):
        if self.does_like(movie):
            self.liked.remove(movie)
            return True
        else:
            return False

    def does_like(self, movie):
        return self.liked.filter(likes.c.movie_id == movie.id).count() > 0

    def hate(self, movie):
        if not self.does_hate(movie):
            self.hated.append(movie)
            if self.does_like(movie):
                self.unlike(movie)
            return True
        else:
            return False

    def unhate(self, movie):
        if self.does_hate(movie):
            self.hated.remove(movie)
            return True
        else:
            return False

    def does_hate(self, movie):
        return self.hated.filter(hates.c.movie_id == movie.id).count() > 0


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    description = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Movie {}>'.format(self.title)

    def get_fans(self):
        return self.fans.count()

    def get_haters(self):
        return self.haters.count()
    
