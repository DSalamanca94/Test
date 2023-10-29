from flask import Flask, Resourse
from psycopg2 import DatabaseError
from decouple import config


app = Flask(__name__)

@app.route('/')

def get_connection():
    try:
        return psycopg2.connect(
            host=config('34.82.89.192'),
            port=config('5432'),
            user=config('postgres'),
            password=config('postgres'),
            database=config('postgres')
        )
    except DatabaseError as ex:
        raise ex


class User(Resourse):
    def post(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO userlogin (username, useremail, userpassword) VALUES (%s, %s, %s)', ('test', 'test', 'test'))
        except DatabaseError as ex:
            raise Exception(ex)



def hello_world():    
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
