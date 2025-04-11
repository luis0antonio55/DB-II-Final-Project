
# API de Empleados con MongoDB

  

Esta es una API RESTful simple que implementa operaciones CRUD para gestionar empleados en una base de datos MongoDB.

  

## Caracteristicas

  

- Conexion a MongoDB Atlas

- Operaciones CRUD completas (Crear, Leer, Actualizar, Eliminar)

- Documentacion automatica con Swagger UI mediante Flask-RestX

- Validaciones basicas de datos

- Busqueda de empleados por nombre o departamento

  

## Estructura de datos

  

La API trabaja con documentos de empleados que tienen la siguiente estructura:

  

```json

{

"empno": 7369,

"ename": "SMITH",

"job": "CLERK",

"sal": 800,

"departamento": {

"deptno": 20,

"dname": "RESEARCH",

"loc": "DALLAS"

}

}

```

  

## Instalacion

  
1. Instala las dependencias:

  

```bash

pip  install  -r  requirements.txt

```

  

2. Ejecuta la aplicacion:

  

```bash

python  crud.py

```

  

La API estara disponible en `http://localhost:5000`.

O la puede visitar en `https://proyecto-final-delta-two.vercel.app/`.
  

## Documentacion Swagger

  

Una vez que la aplicacion este en funcionamiento, pueden acceder a la documentacion Swagger UI navegando a:

  

```

http://localhost:5000/ o https://proyecto-final-delta-two.vercel.app/

```

  

Esta interfaz permite probar todos los endpoints disponibles.

  

## Endpoints

  

-  `GET /empleados/` - Obtiene todos los empleados

-  `POST /empleados/` - Crea un nuevo empleado

-  `GET /empleados/{empno}` - Obtiene un empleado especifico por su numero

-  `PUT /empleados/{empno}` - Actualiza un empleado existente

-  `DELETE /empleados/{empno}` - Elimina un empleado

-  `GET /empleados/buscar/{nombre}` - Busca empleados por nombre (busqueda parcial)

-  `GET /empleados/departamento/{deptno}` - Obtiene todos los empleados de un departamento especifico

  

