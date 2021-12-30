"""
This is an example REST API created in Python and Flask used as a template for all apis
"""

import argparse
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

argparser = argparse.ArgumentParser(
    description="this is an api for videos"
)

argparser.add_argument(
    "-c",
    "--create",
    action="store_true",
    help="Pass this argument if you would like to create the database tables on first run"
)

argparser.add_argument(
    "-s",
    "--secretkey",
    default="Password123",
    help="Pass this argument if you would like to use a custom secret key. Default is Password123"
)

argparser.add_argument(
    "-d",
    "--databaseurl",
    default="sqlite:///database.db",
    help="Pass this argument if you would like to set a custom database url. Default is sqlite:///database.db"
)

mainargs = argparser.parse_args()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = mainargs.secretkey
app.config['SQLALCHEMY_DATABASE_URI'] = mainargs.databaseurl
db = SQLAlchemy(app)

object_name = 'video'
class ObjModel(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Obj(name={self.name}, views={self.views}, likes={self.likes})"

if mainargs.create:
    db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help=f"Name of the {object_name} is required", required=True)
video_put_args.add_argument("views", type=int, help=f"Views of the {object_name} is required", required=True)
video_put_args.add_argument("likes", type=int, help=f"Likes on the {object_name} is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help=f"Name of the {object_name} is required")
video_update_args.add_argument("views", type=int, help=f"Views of the {object_name} is required")
video_update_args.add_argument("likes", type=int, help=f"Likes on the {object_name} is required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Obj(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = ObjModel.query.get(video_id)

        if not result:
            abort(404, message=f'Could not find {object_name} with id [{video_id}]')
        return result

    def post(self, video_id):
        args = video_put_args.parse_args()
        result = ObjModel.query.get(video_id)
        
        if result:
            abort(409, message='Video id taken...')

        result = ObjModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(result)
        db.session.commit()
        return 'OK', 201

    def put(self, video_id):
        args = video_update_args.parse_args()

        result = ObjModel.query.get(video_id)

        if not result:
            abort(404, message="Video doesn't exist, cannot update")
        
        key_list = ObjModel.__table__.columns.keys()

        for key in key_list:
            if key != 'id' and getattr(result, key):
                setattr(result, key, args[key])
        
        db.session.commit()
        return 'OK', 200

    def delete(self, video_id):
        result = ObjModel.query.get(video_id)

        if not result:
            abort(404, message=f"{object_name} doesn't exist, cannot delete")

        db.session.delete(result)
        db.session.commit()
        return '', 200

api.add_resource(Obj, f"/{object_name}/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
