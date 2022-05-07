# Quiz_task
API Rest built in Django Rest Framework

#APP INFO

# Quiz Backend

> Un quiz es una forma de juego o deporte mental en el que los jugadores intentan responder correctamente a preguntas sobre ciertos temas o una variedad de temas. [Wikipedia](https://en.wikipedia.org/wiki/Quiz)

Usualmente un quiz se caracteriza por una cantidad de preguntas que se deben responder correctamente para sumar puntos. Cada pregunta contiene una lista de posibles respuestas, de la cual solo una es correcta. Además cada pregunta tiene un tiempo límite para responder, este lo decide el administrador del quiz.

### Preguntas

Las preguntas pueden ser cualquier cosa, desde cultura general hasta ciencia ficción. La estructura de una pregunta puede ser:

- Texto
- Texto e Imagen

Hablando en términos más técnicos, una pregunta contiene los siguientes elementos:

- Texto de la pregunta
- Imagen de la pregunta
- Puntaje de la pregunta
- Orden de la Pregunta

### Respuestas

Cada pregunta tiene asociada una lista de respuestas de selección simple, la estructura de una respuesta puede ser:

- Texto
- Texto e Imagen

Hablando en términos más técnicos, una respuesta contiene los siguientes elementos:

- Texto de la respuesta
- Imagen de la respuesta
- La respuesta es correcta

### Quiz

El quiz será el conjuntos de preguntas con sus respectivas respuestas, el quiz en general tiene varios elementos:

- Nombre del Quiz
- Descripción del Quiz
- Puntaje máximo del Quiz (Calculado a partir del puntaje de las preguntas)
- Tiempo máximo del Quiz
- Preguntas del Quiz (Calculado a partir de la cantidad preguntas)
- Imagen del Quiz
- Borrador: El quiz al momento de crearse no está listo para ser publicado, es por ello que se le asigna el valor de borrador.

El quiz solo puede ser publicado por el administrador del quiz.

## Requerimientos
- Django Rest Framework como backend
- Base de datos PostgreSQL
- Utilizar Swagger para documentar el API
- Tareas asíncronas con redis y Celery.
-  Se desea que el sistema permita registrarse y loguearse.
-  Se desea que el sistema permita crear quizzes con preguntas y respuestas.
-  Se desea que cada usuario pueda administrar sus propios quizzes, compartirlos con otros usuarios y ver sus resultados una vez finalizados.
- Envio de correo al momento de crearse un usuario, al momento de finalizar un quiz con el puntaje y dichas respuestas.
- Si es posible: Implementación de un websocket, con el propósito de enviar notificaciones a los usuarios que finalizan un quiz mostrando su puntaje, además al administrador del quiz.
- Si es posible: Websocket para gestionar el quiz al momento de realizar la prueba, Enviando las preguntas al usuario y delimitandolo con un tiempo límite.

#INSTRUCCIONES PARA EJECUTAR APLICACIÓN

-INSTALAR ÚLTIMA VERSIÓN DE PYTHON

-CLONAR REPOSITORIO

-DESCARGAR ÚLTIMA VERSIÓN DE POSTGRESQL https://www.postgresql.org/download/

-ACTIVAR EL ENV

-PIP INSTALL REQUIREMENTS.TXT

-DESCARGAR ÚLTIMA VERSIÓN DE REDIS https://redis.io/download/

-EJECUTAR REDIS-SERVER

-CREAR EL WORKER EN OTRA SHELL, CON EL SIGUIENTE COMANDO:   celery -A quizzes_task worker -l info -P gevent 

-EJECUTAR py manage.py makemigrations

-EJECUTAR py manage.py migrate

-EJECUTAR py manage.py runserver

-COMENZAR A REALIZAR LAS PETICIONES 

