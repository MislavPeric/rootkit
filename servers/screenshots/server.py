from flask import Flask
from flask.globals import request
from flask_restful import Resource, Api, reqparse
import base64

app = Flask(__name__)
api = Api(app)

screen_args = reqparse.RequestParser()
screen_args.add_argument("image")

class FetchScreenshot(Resource):
    def post(self, request):
        file = request.FILE
        print(file)
        return "received"

api.add_resource(FetchScreenshot, '/')

if __name__ == "__main__":
    app.run(debug=True)