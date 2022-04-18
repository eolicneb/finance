from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()


class EventType(Enum):
    Gasto = "Gasto"
    Ingreso = "Ingreso"


class EventStatus(Enum):
    Ejecutado = "Ejecutado"
    Previsto = "Previsto"
    Estimado = "Estimado"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class PayMode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<PayMode {self.mode}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Tag label {self.label}>'

    @classmethod
    def by_label(cls, label: str):
        return cls.query.filter(cls.label == label).first()


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('events', lazy=False))
    inserted_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    execution_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.Enum(EventType), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    tag = db.relationship('Tag', backref=db.backref('events', lazy=False))
    status = db.Column(db.Enum(EventStatus), nullable=False)
    pay_mode_id = db.Column(db.Integer, db.ForeignKey('pay_mode.id'), nullable=True)
    pay_mode = db.relationship('PayMode', backref=db.backref('events', lazy=True))

    def __repr__(self):
        return f'<Event {self.type.value}: {self.amount} on {self.execution_dt} tag: {self.tag.label}>'