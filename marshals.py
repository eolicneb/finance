from flask_restful import fields


user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

event_fields = {
    'id': fields.Integer,
    'user': fields.String,
    'inserted_dt': fields.DateTime,
    'execution_dt': fields.DateTime,
    'type': fields.String,
    'amount': fields.Float,
    'tag': fields.Nested({'label': fields.String}),
    'status': fields.String,
    'pay_mode': fields.Nested({'mode': fields.String})
}

tag_fields = {
    'id': fields.Integer,
    'label': fields.String
}

pay_mode_fields = {
    'id': fields.Integer,
    'mode': fields.String
}
