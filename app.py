from flask import Flask, jsonify, request
from flasgger import Swagger
from calendario_informe.main import Login as login_calendario
from calendario_informe.main import obtener_calendarios, informe_por_fecha
from datetime import datetime
from datetime import datetime


app = Flask(__name__)
swagger = Swagger(app)

@app.route('/hello')
def hello_world():
     """
    Ejemplo de endpoint que saluda al usuario.
    ---
    tags:
      - Saludo
    responses:
      200:
        description: Saludo exitoso
        schema:
          properties:
            message:
              type: string
              description: Saludo al usuario
    """
    
     return 'Hello, World!'

# login 
@app.route('/login')
def login():
    """
    Ejemplo de endpoint que saluda al usuario.
    ---
    tags:
      - Saludo
    responses:
      200:
        description: Saludo exitoso
        schema:
          properties:
            message:
              type: string
              description: Saludo al usuario
    """
    
    return login_calendario()

# obtener calendarios
@app.route('/calendarios')
def calendarios():
    """
    Obtener mis calendarios
    ---
    tags:
      - Calendarios
    responses:
      200:
        description: Calendarios
        schema:
          properties:
            message:
              type: string
              description: calendarios
    """
    
    return obtener_calendarios()

# obtener informe por fecha
@app.route('/informe', methods=['GET'])
def informe():
    """
    Obtener informe por fecha
    ---
    tags:
        - Informe

    parameters:
    - name: fecha
      in: query
      type: string
      required: false
      description: Fecha en formato 'YYYY-MM-DD'
    - name: bolean_horas
      in: query
      type: boolean  # Corregido: era type: boolean
      required: false
      description: True para mostrar horas, False para no mostrar horas
    - name: orderBy
      in: query
      type: integer
      required: false
      description: 0 para ordenar por fecha, 1 para ordenar por hora
    responses:
        200:
            description: Informe por fecha
            schema:
                properties:
                    message:
                        type: string
                        description: informe por fecha
    """
    fecha = request.args.get('fecha', datetime.now().strftime('%Y-%m-%d'))
    bolean_horas = request.args.get('bolean_horas', True)
    orderBy = request.args.get('orderBy', 0)

    try:
        # Validate the date format
        datetime.strptime(fecha, '%Y-%m-%d')
        # Your code to generate the informe for the given fecha
        return informe_por_fecha(fecha,bolean_horas,orderBy)

    except ValueError:
        return 'Invalid date format'


if __name__ == '__main__':
    app.run(debug=True, port=5001)

