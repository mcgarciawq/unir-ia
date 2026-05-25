# Proyecto: entregable 2 Integración de endpoints de IA

## Objetivos

Con esta actividad vas a conseguir implementar funcionalidades con IA Generativa en una aplicación API REST existente.

Comprenderás las ventajas de utilizar LLMs para diferentes tareas como generar descripciones, estimaciones y clasificaciones.

Aprenderás a practicar técnicas de prompt engineering que te ayuden a obtener unas mejores salidas acorde a los objetivos del proyecto.

# Enunciado

Sobre el proyecto del entregable 1 que es una aplicación de Flask o FastAPI que tiene un CRUD sobre un modelo Task, agregaremos nuevos endpoints que usen LLMs.

# Pautas de elaboración

## Configurar el entorno de Azure:

- Accede al portal de Azure e inicia sesión.
- Crea un recurso de Azure OpenAI o Azure AI Foundry y obtén las credenciales necesarias (clave API y endpoint) sobre un modelo cualquiera: gpt-4o-mini, gpt-4.1-nano, gpt-4.1-mini o cualquier otro.
- Opcionalmente puedes usar directamente el proveedor OpenAI o Anthropic o cualquier proveedor de tu preferencia en lugar de Azure.

## Preparar el entorno de desarrollo:

- Instala Python y Visual Studio Code o Cursor, o el IDE que prefieras.
- Configura un entorno virtual (`python -m venv venv`) y actívalo.
- Instala la biblioteca oficial de OpenAI (`pip install openai`) o el sdk de IA que prefieras utilizar.

## Nuevos campos para el modelo Task:

- id
- title
- description
- priority
- effort_hours
- status
- assigned_to
- category --> Nuevo campo puede ser str o enum
- risk_analysis --> Nuevo campo texto
- risk_mitigation --> Nuevo campo texto

## Nuevos endpoints en Flask o FastAPI:

Conservamos los endpoints CRUD ya existentes y agregamos nuevos endpoints, que serán:

### `POST /ai/tasks/describe`

Recibe una task con description vacía y genera su description con LLM a partir del resto de campos como el title.

Este endpoint podría devolver la misma tarea que ha recibido pero con el campo description relleno.

### `POST /ai/tasks/categorize`

Recibe una tarea sin categoría y con LLM debe poder clasificarla bajo una categoría: Frontend, Backend, Testing, Infra, etc.

Este endpoint podría devolver la misma tarea que ha recibido pero con el campo category relleno.

### `POST /ai/tasks/estimate`

Recibe una tarea sin effort_hours y con LLM debe poder estimar su esfuerzo en horas leyendo su title, description y category.

Este endpoint podría devolver la misma tarea que ha recibido pero con el campo effort_hours relleno, importante, es un campo numérico no de texto, por lo que habrá que hacer parsing.

### `POST /ai/tasks/audit`

Recibe una tarea con todos los campos rellenos menos risk_analysis y risk_mitigation.

Con esa tarea utiliza sus datos para lanzar dos peticiones un LLM.

Una primera petición para obtener un análisis de riesgos que puedan surgir en la tarea y almacenarlo en risk_analysis y una segunda petición que use esa info junto a la de la tarea para pedir un plan de mitigación de riesgos que se almacene en risk_mitigation.

## Pruebas con POSTMAN:

Se aconseja probar los nuevos endpoints con Postman, Open API Swagger, o cualquier otro sistema de pruebas de API REST.

# Extensión y formato

## Entrega:

Entrega un archivo comprimido (`.zip`) que contenga:

- La aplicación Flask o FastAPI completa.
- Opcionalmente la colección postman.

## Nota:
Asegúrate de que el endpoint y la clave API estén configurados correctamente antes de probar el programa. No incluyas tus credenciales en la entrega.

# Rúbrica

| Proyecto: entregable 2 | Descripción | Puntuación máxima (puntos) | Peso % |
|---|---|---|---|
| Endpoint `/ai/tasks/describe` | Nuevo endpoint para generar descripciones de tareas. | 2,5 | 25 % |
| Endpoint `/ai/tasks/categorize` | Nuevo endpoint para categorizar tareas. | 2,5 | 25 % |
| Endpoint `/ai/tasks/estimate` | Nuevo endpoint para estimar horas de esfuerzo de una tarea. | 2,5 | 25 % |
| Endpoint `/ai/tasks/audit` | Nuevo endpoint para estimar riesgos y mitigación de esos riesgos en una tarea. | 2,5 | 25 % |
|  |  | 10 | 100 % |
