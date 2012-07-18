# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#mysql://scott:tiger@localhost/mydatabase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class UserAuth(db.Model):
    __tablename__ = 'userauth'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True)
    secret = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('user', lazy='dynamic'))

    def __init__(self, token, secret):
        self.token = token
        self.secret = secret


class Feed(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    type = db.Column(db.String(255))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    locked = db.Column(db.Boolean)
    update_intervall = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('user', lazy='dynamic'))

    def __init__(self, name, url, update_intervall, type='rss', created=None, locked=False):
        self.name = name
        self.url = db.Column(db.String(255))
        self.update_intervall = update_intervall
        if created is None:
            created = datetime.utcnow()
        self.created = created
        self.updated = updated
        self.locked = False

    def __repr__(self):
        return '<Feed %r>' % self.name


class FeedItem(db.Model):
    __tablename__ = 'feeditems'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    feed = db.relationship('Feed',
        backref=db.backref('feeditems', lazy='dynamic'))

    def __init__(self, title, body, feed, created=None):
        self.title = title
        self.body = body
        self.feed = feed
        if created is None:
            created = datetime.utcnow()
        self.created = created

    def __repr__(self):
        return '<FeedItem %r>' % self.title
