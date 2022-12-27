from app.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)


class EmailRecipients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(25), nullable=False)


class Telegram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50))
    token = db.Column(db.String(50), nullable=False, unique=True)


class TelegramGroupId(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('telegram.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50))
    group_id = db.Column(db.String(50), nullable=False)


class Slack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50))
    channel = db.Column(db.String(50), nullable=False, unique=True)
    bot_token = db.Column(db.String(50), nullable=False, unique=True)
    user_token = db.Column(db.String(50), nullable=False, unique=True)
