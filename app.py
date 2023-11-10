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
        archivo_a_copiar = 'nombre_del_archivo.txt'

        # Rutas completas de origen y destino
        ruta_origen = 'gs://app-storage-folder/in/{}'.format(archivo_a_copiar)
        ruta_destino = 'gs://app-storage-folder/out/{}'.format(archivo_a_copiar)

        try:
            storage_client = storage.Client()
            bucket = storage_client.get_bucket('app-storage-folder')

            # Comprobar si el archivo de origen existe
            blob_origen = bucket.blob('in/{}'.format(archivo_a_copiar))
            blob_origen.reload()

            # Copiar el archivo
            blob_destino = bucket.blob('out/{}'.format(archivo_a_copiar))
            bucket.copy_blob(blob_origen, blob_destino)

            return {'status': 'success', 'message': 'Archivo copiado correctamente.'}
        except NotFound:
            return {'status': 'error', 'message': 'El archivo de origen no existe.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

api.add_resource(CreateFile, '/CreateFile')
api.add_resource(Status, '/status')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
