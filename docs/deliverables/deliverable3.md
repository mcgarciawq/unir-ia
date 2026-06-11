# Proyecto: entregable 3

## Objetivos

Continuamos trabajando en el proyecto de generación de tareas a partir de historias de usuario. En este entregable, el objetivo es completar el desarrollo de la aplicación con interfaz de usuario y base de datos. Para ello, conectarás la aplicación FastAPI a base de datos relacional MySQL y utilizarás salidas estructuradas de IA para almacenar resultados y mostrarlos por la interfaz de usuario.

---

# Pautas de elaboración

Crea una aplicación FastAPI dividida en múltiples archivos donde tengas:

## 1. Conexión a base de datos MySQL local.

## 2. Generación de modelos SQLAlchemy:

### UserStory con campos:

- id (primary key).
- project (nombre de proyecto).
- role (rol de usuario en la historia).
- goal (objetivo de la historia de usuario).
- reason (razón de la historia de usuario).
- description (texto largo que describe en qué consiste toda la historia de usuario).
- priority (prioridad baja, media, alta, bloqueante).
- story_points (puntos de historia estimados 1-8).
- effort_hours (número decimal, horas estimadas para completar la historia).
- created_at (fecha creación se crea automática a nivel de base de datos).
- Agregar más campos si se quiere.

### Task

- id (primary key).
- title (título de la tarea).
- description (texto largo que describe completamente la tarea).
- priority (prioridad baja, media, alta, bloqueante).
- effort_hours (número decimal, horas estimadas para completar la historia).
- status (estado pendiente, en progreso, en revisión, completada).
- assigned_to (string, persona del equipo a la que se asigna).
- user_story_id (asociación many to one con UserStory).
- created_at (fecha creación se crea automática a nivel de base de datos).
- Agregar más campos si se quiere.

## 3. Generación de Schemas con Pydantic:

- UserStorySchema.
- UserStorySchemas.
- TaskSchema.
- TaskSchemas.

## 4. Generación de endpoints mvc:

### GET /user-stories

Que devolverá un HTML `user-stories.html`, donde se verán todas las historias de usuario y tendrá una textarea para escribir prompt para enviar a backend para solicitar generar historias de usuario a partir del prompt.

Mostrará un listado con todas las historias de usuario existentes en base de datos.

Cada historia de usuario tendrá un botón «Generar tareas», que al pulsarlo llamará a otro endpoint.

### POST /user-stories

Al que se envía el formulario de `user-stories.html`, extrae el prompt y lo usa para generar una historia de usuario completa y almacenarla en base de datos.

### POST /user-stories/{id}/generate-tasks

Este endpoint es el que se invoca cuando se pulsa el botón de generar tareas sobre una historia de usuario. Aquí se generan las tareas para esa historia de usuario usando IA y se almacenan en base de datos asociadas a la historia de usuario.

Tras ello se vuelve a mostrar la pantalla de `tasks.html` en una URL `GET /user-stories/{id}/tasks`, donde se verían las tareas de esa historia de usuario.

---

# Extensión y formato

Entrega un archivo `m4_proyecto_nombre_apellido.zip` que contenga una carpeta con el proyecto FastAPI y los archivos necesario Python y HTML para conseguir el resultado deseado.

---

# Rúbrica

| Proyecto: entregable 3 | Descripción | Puntuación máx. (puntos) | Peso % |
|---|---|---|---|
| Modelos y base de datos | Modelos SQLAlchemy y schemas Pydantic y conexión a base de datos relacional. | 2 | 20 % |
| Historias de usuario | Endpoints de FastAPI para gestionar y generar historias de usuario y almacenarlas en base de datos. Endpoints para poder mostrar las historias de usuario. | 3 | 30 % |
| Tareas | Endpoints de FastAPI para gestionar y generar tareas a partir de historias de usuario y almacenarlas en base de datos. Endpoints para poder mostrar las tareas. | 2 | 20 % |
| UI | Interfaz de usuario con Jinja HTML Bootstrap o Tailwind CSS para mostrar y gestionar las historias de usuario y tareas con las acciones mencionadas. No es necesario editar ni borrar. | 3 | 30 % |
|  |  | 10 | 100 % |