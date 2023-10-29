from Test import create_app
from flask_restful import Api, Resource

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/api/test')

if __name__ == '__main__':
    app.run()