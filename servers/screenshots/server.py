from flask import Flask
from flask.globals import request
from flask_restful import Resource, Api, reqparse   

app = Flask(__name__)
api = Api(app)

screen_args = reqparse.RequestParser()
screen_args.add_argument("image", type=str, required=True)

class FetchScreenshot(Resource):
    def post(self):
        args = screen_args.parse_args()
        print(args)
        return "received"

api.add_resource(FetchScreenshot, '/')

if __name__ == "__main__":
    app.run(debug=True)