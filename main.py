"""
This is an example REST API created in Python and Flask
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
    "-d",
    "--databaseurl",
    default="sqlite:///database.db",
    help="Pass this argument if you would like to create the database tables on first run"
)

mainargs = argparser.parse_args()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = mainargs.databaseurl
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

if mainargs.create:
    db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video is required")
video_update_args.add_argument("likes", type=int, help="Likes on the video is required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.get(video_id)

        if not result:
            abort(404, message=f'Could not find video with id [{video_id}]')
        return result

    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.get(video_id)
        
        if result:
            abort(409, message='Video id taken...')

        result = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(result)
        db.session.commit()
        return 'OK', 201

    def patch(self, video_id):
        args = video_update_args.parse_args()

        result = VideoModel.query.get(video_id)

        if not result:
            abort(404, message="Video doesn't exist, cannot update")
        
        if args['name']:
            result.name = args['name']
        
        if args['views']:
            result.views = args['views']

        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()
        return 'OK', 200

    def delete(self, video_id):
        result = VideoModel.query.get(video_id)

        if not result:
            abort(404, message="Video doesn't exist, cannot delete")

        db.session.delete(result)
        db.session.commit()
        return '', 200

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
