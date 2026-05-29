# Proyecto: entregable 1

## Objetivos
Vamos a crear un proyecto de generación de tareas que se asignan a usuarios. En este entregable, el objetivo es comenzar con el desarrollo de la aplicación Flask con la arquitectura y la lógica de programación, que luego usaremos en los siguientes módulos. Para ello, crearás una aplicación con Flask, organizando toda la arquitectura del proyecto creando rutas que conecten con los controladores para devolver resultados asociados a través de un json.

## Pautas de elaboración
Crea una aplicación Flask que tenga rutas y controladores para la gestión de tareas de usuario. Los campos de tareas tendrán el siguiente interfaz:

### Task
* **id** (primary key).
* **title** (título de la tarea).
* **description** (texto largo que describe completamente la tarea).
* **priority** (prioridad baja, media, alta, bloqueante).
* **effort_hours** (número decimal, horas estimadas para completar la tarea).
* **status** (estado pendiente, en progreso, en revisión, completada).
* **assigned_to** (string, persona del equipo a la que se asigna).

### Generación de endpoints:
* Crear una tarea (**POST /tasks**).
* Leer todas las tareas (**GET /tasks**).
* Leer una tarea específica (**GET /tasks/<id>**).
* Actualizar una tarea (**PUT /tasks/<id>**).
* Eliminar una tarea (**DELETE /tasks/<id>**).

Deberás crear la arquitectura de ficheros del proyecto. Crearás el entorno virtual y la instalación de librerías, así como el fichero de requerimientos.

Crearás un **fichero de rutas**, donde darás de alta todas las rutas especificadas que llamarán a la clase **TaskManager**, que deberá gestionar el uso de tareas con el archivo json. También existirá una clase **Task**, que permitirá definir una tarea y convertirla en un diccionario para poder insertarla en un json.

#### Clase Task
Representa una tarea con los datos del interfaz.
**Métodos:** 
* `to_dict()`: convierte el objeto Task a diccionario.
* `from_dict()`: crea un Task desde un diccionario.

#### Clase TaskManager 
**Métodos estáticos:** 
* `load_tasks()`: carga tareas desde tasks.json y las convierte en objetos Task.
* `save_tasks()`: guarda la lista de Task en el archivo JSON.

### Flask API 
* **GET /tasks** → devuelve todas las tareas.
* **GET /tasks/<id>** → devuelve una tarea específica.
* **POST /tasks** → crea una tarea nueva.
* **PUT /tasks/<id>** → modifica una tarea existente.
* **DELETE /tasks/<id>** → elimina una tarea.

## Extensión y formato
Entrega un archivo `m2_proyecto_nombre_apellido.zip` que contenga una carpeta con el proyecto Flask y los archivos necesarios de Python.

## Rúbrica

| Proyecto: entregable 1 | Descripción | Puntuación máxima (puntos) | Peso % |
| :--- | :--- | :--- | :--- |
| **Arquitectura del proyecto** | Creación del proyecto y arquitectura del proyecto en Flask. | 2,5 | 25 % |
| **Clase Tarea** | Creación de la clase Task. | 2,5 | 25 % |
| **Clase TaskManager** | Creación de la clase TaskManager. | 2,5 | 25 % |
| **Crear rutas** | Crear los endpoints necesarios para poder hacer peticiones y devolver respuestas en formato JSON en el servidor. | 2,5 | 25 % |
| **Total** | | **10** | **100 %** |