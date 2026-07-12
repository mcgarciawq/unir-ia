# Proyecto: entregable 4

## Asignatura

**Programa Avanzado en Inteligencia Artificial para Programar**

**Apellidos:**

**Nombre:**

---

# Actividades

## Objetivos

- Con esta actividad se aprenderá a empaquetar aplicaciones en contenedores utilizando Docker.
- Se podrá automatizar la construcción, la prueba y el despliegue de contenedores mediante pipelines de integración continua con GitHub Actions o Azure Pipelines.
- Se desarrollarán habilidades para garantizar la reproducibilidad y portabilidad de aplicaciones a través de contenedores.
- Se evaluarán las ventajas de la integración continua en la automatización del ciclo de vida de aplicaciones.

## Enunciado

Crear y desplegar una aplicación web utilizando Flask, contenerizada con Docker y configurada con un pipeline de integración continua usando GitHub Actions.

### Requisitos

1. Crear una aplicación web simple en Python utilizando Flask. La aplicación debe responder con un mensaje de saludo cuando se acceda a la raíz (`/`).

2. Contenerizar la aplicación usando Docker, con un archivo `Dockerfile` que:

   - Utiliza una imagen base oficial de Python.
   - Instala las dependencias necesarias desde un archivo `requirements.txt`.
   - Expone el puerto `5000` para la aplicación Flask.
   - Configura el comando necesario para ejecutar la aplicación Flask.

3. Crear un pipeline de integración continua con GitHub Actions para:

   - Descargar el código desde el repositorio.
   - Construir una imagen Docker a partir del Dockerfile.
   - Subir la imagen Docker a Docker Hub.
   - **Opcional:** incluir pruebas automatizadas utilizando `pytest` para asegurar que la aplicación responde correctamente.

### Pasos adicionales

- Configura los secretos de Docker Hub en GitHub para permitir el acceso y la subida de imágenes.
- **Opcional:** añadir pruebas unitarias con `pytest` para verificar que la aplicación funciona correctamente antes de construir la imagen Docker.

---

# Pautas de elaboración

## 1. Preparación del entorno

- Crea un proyecto en GitHub o Azure Repos con una aplicación sencilla en Python.
- Asegúrate de tener configurado Docker en tu máquina y una cuenta activa en Docker Hub.

## 2. Creación del Dockerfile

Escribe un `Dockerfile` para tu aplicación que contenga:

- Imagen base.
- Instalación de dependencias.
- Configuración de puertos expuestos.
- Comando de ejecución de la aplicación.

## 3. Automatización del pipeline

Define un pipeline de CI para construir, probar y desplegar tu contenedor.

Usa GitHub Actions o Azure Pipelines. Configura:

- **Etapa de build:** construcción de la imagen Docker.
- **Etapa de prueba:** ejecución de pruebas unitarias de tu aplicación dentro del contenedor.
- **Etapa de push:** subida de la imagen Docker al Docker Hub o Azure Container Registry.

## 4. Ejecución y verificación

- Ejecuta el pipeline desde el repositorio y verifica que todas las etapas se completen correctamente.
- Comprueba que la imagen del contenedor esté disponible en Docker Hub o Azure Container Registry y que funcione al ser desplegada.

## 5. Entrega

Sube tu proyecto completo al repositorio, incluyendo:

- El `Dockerfile`.
- El archivo del pipeline.
- Un `README` con las instrucciones para ejecutar la imagen.

---

# Extensión y formato

## Entrega

Enlace a un repositorio público en GitHub o Azure Repos con:

- El archivo del pipeline (`.yaml`).
- El `Dockerfile`.
- `README.md` con la descripción del proyecto.

## Formato del README

- Fuente: Arial 12.
- Interlineado: 1,5.
- Extensión: mínimo dos páginas.

---

# Rúbrica

| Proyecto: entregable 4 | Descripción | Puntuación máxima | Peso |
|-------------------------|-------------|------------------:|-----:|
| Creación del Dockerfile | El Dockerfile está bien estructurado y funcional. | 2 | 20 % |
| Configuración del pipeline | Pipeline bien definido con etapas claras. | 3 | 30 % |
| Automatización de pruebas | Pruebas ejecutadas correctamente dentro del pipeline. | 2 | 20 % |
| Subida y despliegue del contenedor | Imagen subida y funcional en Docker Hub o Azure Container Registry. | 2 | 20 % |
| Documentación en README.md | Instrucciones claras y detalladas en el README.md. | 1 | 10 % |

**Total: 10 puntos (100 %)**
