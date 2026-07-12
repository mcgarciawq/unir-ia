# Proyecto: entregable 5

## Asignatura

**Programa Avanzado en Inteligencia Artificial para Programar**

**Apellidos:**

**Nombre:**

---

# Actividades

## Objetivos

- Diseñar y configurar un pipeline CI/CD para el despliegue automatizado de una aplicación en la nube.
- Implementar una aplicación backend con base de datos, contenida en Docker y gestionada con Docker Compose.
- Desplegar la aplicación en Azure utilizando Azure Container Apps o Azure Container Instances.
- Integrar una base de datos con la aplicación y aplicar buenas prácticas de configuración y seguridad.
- Monitorizar y validar el correcto funcionamiento del despliegue.

---

# Pautas de elaboración

## 1. Configuración del entorno

- Crea un repositorio en Azure Repos (o GitHub si lo prefieres).
- Estructura el código de la aplicación backend utilizando Python (Flask) o Node.js (Express).
- Define un archivo `.env` con las credenciales y parámetros de conexión de la base de datos.

## 2. Contenerización de la aplicación

- Crea un `Dockerfile` para definir la imagen de la aplicación.
- Implementa un archivo `docker-compose.yml` que incluya:

  - Un servicio para la aplicación backend.
  - Un servicio de base de datos MySQL o PostgreSQL.
  - Variables de entorno necesarias para la conexión.

- Prueba la aplicación en local con:

```bash
docker-compose up --build
```

## 3. Registro y gestión de contenedores en Azure

- Crea un Azure Container Registry (ACR) para almacenar la imagen del contenedor.
- Sube la imagen con los comandos:

```bash
az acr login --name <tu_acr>
docker tag mi-backend:v1 <tu_acr>.azurecr.io/mi-backend:v1
docker push <tu_acr>.azurecr.io/mi-backend:v1
```

## 4. Despliegue de la aplicación en Azure

- Configura un servicio en Azure Container Apps o Azure Container Instances.
- Despliega la aplicación desde ACR asegurando que la base de datos esté accesible.
- Define variables de entorno en la configuración del servicio.

## 5. Automatización con CI/CD

Crea un pipeline en Azure Pipelines o GitHub Actions para:

- Compilar y construir la imagen del contenedor.
- Ejecutar pruebas unitarias y de integración.
- Subir la imagen a ACR.
- Desplegar automáticamente la nueva versión en Azure Container Apps o Azure Container Instances (ACI).

## 6. Monitoreo y validación

- Verifica los logs de la aplicación con:

```bash
az containerapp logs show --name mi-backend
```

- Realiza pruebas de conexión con la base de datos desde la aplicación.

---

# Extensión y formato

- **Formato:** documento PDF o informe en Word con capturas de pantalla del proceso.
- **Extensión:** de 3 a 5 páginas con explicaciones detalladas.
- **Fuente y estilo:** Arial o Calibri, tamaño 12, interlineado 1,5.

---

# Rúbrica

| Proyecto: entregable 5 | Descripción | Puntuación máxima | Peso |
|-------------------------|-------------|------------------:|-----:|
| Configuración y estructuración | Correcta configuración del repositorio y estructura del código. | 1,5 | 15 % |
| Contenerización | Creación adecuada del `Dockerfile` y `docker-compose.yml`. | 1,5 | 15 % |
| Registro en Azure | Uso correcto de Azure Container Registry (ACR) para el almacenamiento de la imagen. | 2 | 20 % |
| Despliegue en Azure | Configuración y ejecución en Azure Container Apps o Azure Container Instances. | 2 | 20 % |
| Pipeline CI/CD | Configuración del flujo de automatización con pruebas y despliegue continuo. | 2 | 20 % |
| Monitoreo y validación | Implementación de logs y pruebas de conexión. | 1 | 10 % |

**Total: 10 puntos (100 %)**