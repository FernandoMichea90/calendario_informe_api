from flask import Flask, jsonify
from flasgger import Swagger

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

if __name__ == '__main__':
    app.run(debug=True)

