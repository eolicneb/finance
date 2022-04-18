import pytest
from flask import Flask
from models import User, Event, EventType, Tag, db as model_db


@pytest.fixture
def put_test_cases():
    def _inner():
        return
    return _inner


@pytest.fixture
def app(put_test_cases):
    test_app = Flask(__name__)
    model_db.init_app(test_app)
    with test_app.app_context():
        model_db.create_all()
        put_test_cases()
    return test_app


def test_models(app):
    with app.app_context():
        us1 = User(
            username="menganito"
        )
        laburo = Tag(label='laburo')
        fernet = Tag(label='fernet')

        us1.events.append(
            Event(
                execution_dt='2022-06-01',
                type=EventType.Gasto,
                amount=65000,
                tag=fernet)
        )

        us1.events.append(
            Event(
                execution_dt='2022-05-01',
                type=EventType.Ingreso,
                amount=43000,
                tag=laburo)
        )

        model_db.session.add(us1)

        assert len(us1.events) == 2
