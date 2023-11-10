from flask import Flask
from flask_restful import Resource, Api
from google.cloud import storage
from google.cloud.exceptions import NotFound



app = Flask(__name__)
api = Api(app)

# Configura la conexión a la base de datos con SQLAlchemy

class Status(Resource):
    def get(self):
        return ('Estoy Conectado!!!!')


class CreateFile(Resource):
    def post(self):
        # Nombre del archivo que deseas copiar
        archivo_a_copiar = 'Test.txt'

        # Rutas completas de origen y destino
        ruta_origen = 'gs://app-storage-folder/Input/{}'.format(archivo_a_copiar)
        ruta_destino = 'gs://app-storage-folder/Output/{}'.format(archivo_a_copiar)

        # Copiar el archivo
        try:
            storage_client = storage.Client()
            bucket = storage_client.get_bucket('app-storage-folder')

            # Comprobar si el archivo de origen existe
            blob_origen = bucket.blob('Input/{}'.format(archivo_a_copiar))
            blob_origen.reload()

            # Copiar el archivo
            blob_origen.copy_to(bucket, 'Output/{}'.format(archivo_a_copiar))

            return {'status': 'success', 'message': 'Archivo copiado correctamente.'}
        except NotFound:
            return {'status': 'error', 'message': 'El archivo de origen no existe.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

api.add_resource(CreateFile, '/CreateFile')
api.add_resource(Status, '/status')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
