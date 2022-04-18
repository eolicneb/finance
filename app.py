from flask import Flask
from flask_restful import Api

from resources import (UserList, TagList, TagLabel, EventResource,
                       EventHandle, PayModeList, EventFilter)
from bootup import insert_pay_modes


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

api = Api(app)
api.add_resource(UserList, '/users/')
api.add_resource(TagList, '/tags/')
api.add_resource(TagLabel, '/tags/label/<tag_label>/')
api.add_resource(EventResource, '/users/<int:user_id>/events/')
api.add_resource(EventHandle, '/users/<int:user_id>/events/<int:event_id>/')
api.add_resource(PayModeList, '/paymodes/')
api.add_resource(EventFilter, '/users/<int:user_id>/events/filter/')

from models import db
db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
    print("Created DB")
    insert_pay_modes()


if __name__ == "__main__":
    app.run()
