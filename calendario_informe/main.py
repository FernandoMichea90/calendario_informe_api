import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds=None

def Login():
    try:
        global creds
        # obtener la ruta del directorio actual
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        # ruta con el archivo de credenciales
        ruta_credenciales = ruta_actual+'/credentials.json'
        # si las credennciales no son validas 
        if not creds or not creds.valid:
            # si las credenciales son refrescables  
            if creds and creds.expired and creds.refresh_token:
                # refrescar las credenciales
                creds.refresh(Request())
            else:
                # crear el flujo de autenticacion
                flow = InstalledAppFlow.from_client_secrets_file(
                    ruta_credenciales, SCOPES)
                # obtener las credenciales
                creds = flow.run_local_server(port=5000)
            # guardar las credenciales
            with open(ruta_actual+'/token.json', 'w') as token:
                token.write(creds.to_json())   
    except Exception as e:
        print(e)
        return 'Error al autenticar' 

    return 'Login exitoso'





