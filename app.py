from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import psycopg2

app = Flask(__name__)
api = Api(app)

# Configura la conexión a la base de datos con SQLAlchemy
db_name = 'postgres'
db_user = 'postgres'
db_password = 'postgres'
db_host = '34.82.89.192'
db_port = '5432'

db_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
db = create_engine(db_string)

class Status(Resource):
    def get(self):
        return ('Estoy Conectado!!!!')


class User(Resource):
    def post(self):
        try:
            conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO userlogin (username, useremail, userpassword) VALUES (%s, %s, %s)', ('test', 'test2', 'test'))
            conn.commit()
            conn.close()
            return {'message': 'User added successfully'}, 201
        except SQLAlchemyError as ex:
            return {'error': str(ex)}, 500

api.add_resource(User, '/user')
api.add_resource(Status, '/status')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
