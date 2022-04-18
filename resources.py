import functools
import settings
from flask import request
from datetime import datetime
from flask_restful import reqparse, abort, Resource, marshal_with
from sqlalchemy import exc
from werkzeug import exceptions as wexc
from models import EventType, EventStatus, User, PayMode, Event, Tag, db
from marshals import user_fields, event_fields, tag_fields, pay_mode_fields


event_type_choices = [t.name for t in EventType]
event_status_choices = [t.name for t in EventStatus]
event_parser = reqparse.RequestParser()
event_parser.add_argument("user_id", type=int, help="User ID")
event_parser.add_argument("execution_dt", type=datetime.fromisoformat, help="Date to execute the event")
event_parser.add_argument("type", type=str, choices=event_type_choices,
                          help=f"Type of event {event_type_choices}")
event_parser.add_argument("amount", type=float, help="Amount of the event")
event_parser.add_argument("tag", type=str, help="The event tag")
event_parser.add_argument("status", type=str, choices=event_status_choices,
                          help=f"Status of event {event_status_choices}")
event_parser.add_argument("pay_mode_id", type=int,
                          required=False, help=f"Pay mode ID ")

filter_parser = reqparse.RequestParser()
filter_parser.add_argument("type", type=EventType, choices=EventType,
                           required=False, help=f"Type of event {event_type_choices}")

tag_parser = reqparse.RequestParser()
tag_parser.add_argument("label", type=str, help="Label for the new tag")

user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, help="User string identifier")


def handle_exceptions():
    def _inner(f):
        @functools.wraps(f)
        def _wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except wexc.BadRequest:
                raise
            except exc.IntegrityError as e:
                return abort(400, message=str(e))
            except Exception as e:
                return abort(500, message=str(e))

        return _wrapper

    return _inner


class UserList(Resource):
    @handle_exceptions()
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        new_user = User(username=args.username)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

    @marshal_with(user_fields)
    def get(self):
        users_list = User.query.all()
        return users_list, 200


class PayModeList(Resource):
    @marshal_with(pay_mode_fields)
    def get(self):
        return PayMode.query.all(), 200


class TagList(Resource):
    @handle_exceptions()
    @marshal_with(tag_fields)
    def post(self):
        args = tag_parser.parse_args()
        new_label = Tag(label=args.label)
        db.session.add(new_label)
        db.session.commit()
        return new_label, 201

    @marshal_with(tag_fields)
    def get(self):
        tag_list = Tag.query.all()
        return tag_list, 200


class TagLabel(Resource):
    @marshal_with(tag_fields)
    def get(self, tag_label):
        tag = Tag.by_label(tag_label)
        return tag, 200


class EventResource(Resource):
    @handle_exceptions()
    @marshal_with(event_fields)
    def post(self, user_id):
        args = event_parser.parse_args()
        tag = Tag.by_label(args.tag)
        new_event = Event(user_id=user_id,
                          execution_dt=args.execution_dt,
                          type=args.type,
                          amount=args.amount,
                          tag=tag,
                          status=args.status,
                          pay_mode_id=args.pay_mode_id)
        db.session.add(new_event)
        db.session.commit()
        return new_event, 201

    @marshal_with(event_fields)
    def get(self, user_id):
        return Event.query.filter(Event.user_id == user_id).all()


class EventHandle(Resource):
    @handle_exceptions()
    @marshal_with(event_fields)
    def put(self, user_id, event_id):
        event = Event.query.filter(Event.id == event_id)
        if event.first().user_id != user_id:
            raise wexc.BadRequest("The event belong to a different user")
        event.update(request.get_json())
        db.session.commit()
        return event.first(), 201


class EventFilter(Resource):
    @marshal_with(event_fields)
    def post(self, user_id):
        args = filter_parser.parse_args()
        filter_ = {k: v for k, v in args.__dict__.items() if v}
        events = User.query.get(user_id).events.filter(**filter_).all()
        return events, 200
