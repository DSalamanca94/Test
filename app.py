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
        archivo_a_copiar = 'Test.txt'
        ruta_origen = 'gs://app-storage-folder/Input/{}'.format(archivo_a_copiar)
        ruta_destino = 'gs://app-storage-folder/Output/{}'.format(archivo_a_copiar)

        try:
            # Utiliza las credenciales predeterminadas proporcionadas por la instancia de VM
            storage_client = storage.Client()

            # Comprobar si el archivo de origen existe
            bucket = storage_client.get_bucket('app-storage-folder')
            blob_origen = bucket.blob('Input/{}'.format(archivo_a_copiar))

            if not blob_origen.exists():
                return {'status': 'error', 'message': 'El archivo de origen no existe en el bucket de origen.'}

            # Copiar el archivo
            blob_destino = bucket.blob('Output/{}'.format(archivo_a_copiar))
            bucket.copy_blob(blob_origen, bucket, blob_destino.name)

            return {'status': 'success', 'message': 'Archivo copiado correctamente.'}
        except NotFound:
            return {'status': 'error', 'message': 'El archivo de origen no existe.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


api.add_resource(CreateFile, '/CreateFile')
api.add_resource(Status, '/status')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
