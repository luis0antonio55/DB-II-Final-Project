from flask import Flask, request
from flask_restx import Api, Resource, fields
from pymongo import MongoClient
from bson.json_util import dumps
import json
import os
import certifi
from dotenv import load_dotenv

# Cargamos las variables de entorno 
load_dotenv()

# Iniciamos flask
app = Flask(__name__)

# Variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "hr")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "empleados")

# Mongo client
client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    retryWrites=True,
    retryReads=True,
    maxPoolSize=50,
    waitQueueTimeoutMS=2500,
    connectTimeoutMS=10000,
    socketTimeoutMS=45000
)


db = client[MONGODB_DB] 
empleados_collection = db[MONGODB_COLLECTION]  

# Configurar Flask-RestX para Swagger
api = Api(app, version='1.0', title='API de Empleados',
          description='API CRUD para gestionar empleados en MongoDB')

# Crear un namespace para los endpoints de empleados
ns = api.namespace('empleados', description='Operaciones CRUD de empleados')

# Definir modelos para la documentación de Swagger
departamento_model = api.model('Departamento', {
    'deptno': fields.Integer(required=True, description='Numero de departamento'),
    'dname': fields.String(required=True, description='Nombre del departamento'),
    'loc': fields.String(required=True, description='Ubicacion del departamento')
})

empleado_model = api.model('Empleado', {
    'empno': fields.Integer(required=True, description='Numero de empleado'),
    'ename': fields.String(required=True, description='Nombre del empleado'),
    'job': fields.String(required=True, description='Puesto de trabajo'),
    'sal': fields.Float(required=True, description='Salario'),
    'departamento': fields.Nested(departamento_model, required=True, description='Departamento')
})

def parse_json(data):
    return json.loads(dumps(data))

@ns.route('/')
class EmpleadosList(Resource):
    @ns.doc('listar_empleados')
    def get(self):
        """Obtiene todos los empleados"""
        empleados = list(empleados_collection.find())
        return parse_json(empleados)
    
    @ns.doc('crear_empleado')
    @ns.expect(empleado_model)
    def post(self):
        """Crea un nuevo empleado"""
        nuevo_empleado = request.json
        
        # Validar que no exista un empleado con el mismo empno
        if empleados_collection.find_one({"empno": nuevo_empleado['empno']}):
            return {"mensaje": f"Ya existe un empleado con el numero {nuevo_empleado['empno']}"}, 400
        
        result = empleados_collection.insert_one(nuevo_empleado)
        return {"mensaje": "Empleado creado con exito", "id": str(result.inserted_id)}, 201

@ns.route('/<int:empno>')
@ns.param('empno', 'Numero de empleado')
class Empleado(Resource):
    @ns.doc('obtener_empleado')
    def get(self, empno):
        """Obtiene un empleado por su numero"""
        empleado = empleados_collection.find_one({"empno": empno})
        if empleado:
            return parse_json(empleado)
        return {"mensaje": "Empleado no encontrado"}, 404
    
    @ns.doc('actualizar_empleado')
    @ns.expect(empleado_model)
    def put(self, empno):
        """Actualiza un empleado existente"""
        datos_actualizados = request.json
        
        # Verificar que el empleado exista
        if not empleados_collection.find_one({"empno": empno}):
            return {"mensaje": f"No existe un empleado con el numero {empno}"}, 404
        
        # Asegurar que el empno en el cuerpo coincida con el de la URL
        if 'empno' in datos_actualizados and datos_actualizados['empno'] != empno:
            return {"mensaje": "El numero de empleado no puede ser modificado"}, 400
        
        datos_actualizados['empno'] = empno  # Asegurar que el empno se mantenga
        
        result = empleados_collection.update_one(
            {"empno": empno},
            {"$set": datos_actualizados}
        )
        
        if result.modified_count:
            return {"mensaje": f"Empleado {empno} actualizado con exito"}
        return {"mensaje": "No se realizaron cambios"}, 304
    
    @ns.doc('eliminar_empleado')
    def delete(self, empno):
        """Elimina un empleado"""
        result = empleados_collection.delete_one({"empno": empno})
        if result.deleted_count:
            return {"mensaje": f"Empleado {empno} eliminado con exito"}
        return {"mensaje": "Empleado no encontrado"}, 404

@ns.route('/buscar/<string:nombre>')
@ns.param('nombre', 'Nombre del empleado a buscar')
class BuscarEmpleado(Resource):
    @ns.doc('buscar_por_nombre')
    def get(self, nombre):
        """Busca empleados por nombre (busqueda parcial, no sensible a mayusculas)"""
        # Expresion regular para busqueda parcial insensible a mayusculas/minusculas
        empleados = list(empleados_collection.find(
            {"ename": {"$regex": nombre, "$options": "i"}}
        ))
        return parse_json(empleados)

@ns.route('/departamento/<int:deptno>')
@ns.param('deptno', 'Numero de departamento')
class EmpleadosPorDepartamento(Resource):
    @ns.doc('listar_por_departamento')
    def get(self, deptno):
        """Obtiene todos los empleados de un departamento especifico"""
        empleados = list(empleados_collection.find(
            {"departamento.deptno": deptno}
        ))
        return parse_json(empleados)

# Local
if __name__ == '__main__':
    app.run(debug=True)