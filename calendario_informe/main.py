import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import json


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds=None
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_token = ruta_actual+'/token.json'


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

def obtener_calendarios():
    #convertir token.json a credenciales
    if os.path.exists(ruta_token):
       creds = Credentials.from_authorized_user_file(ruta_token, SCOPES)
    else:
        return 'Error  credenciales no validas'
    # crear el servicio de calendario
    service = build('calendar', 'v3', credentials=creds)
    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            calenadarios = []
            for calendar_list_entry in calendar_list['items']:
                calenadarios.append(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calenadarios
    except Exception as e:
        print(e)
        return 'Error al obtener calendarios'
    
def informe_por_fecha(fecha,bolean_horas=True,orderBy=1):

     #lista de calendarios  desde google
    # calendarios_informe = service.calendarList().list(pageToken=page_token).execute().get('items')
    print (ruta_actual+"/calendarios_informe.json")
    print("---------------------------")
    if os.path.exists(ruta_actual+"/calendarios_informe.json"):
        with open(ruta_actual+"/calendarios_informe.json") as f:
            calendarios_informe = json.load(f)
    else:
        print("No existe el archivo calendarios_informe.json")
        return "No existe el archivo calendarios_informe.json"
    #convertir token.json a credenciales
   
    if os.path.exists(ruta_token):
       creds = Credentials.from_authorized_user_file(ruta_token, SCOPES)
    else:
        return 'Error  credenciales no validas'
    # crear el servicio de calendario
    service = build('calendar', 'v3', credentials=creds)
    # page_token = None
    page_token = None
  
    # obtener la fecha de hoy
    today = datetime.datetime.utcnow().isoformat() + 'Z'
    #obtener la fecha y hora del comienzo del día de hoy
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    #obtener la fecha y hora del final del día de hoy
    today_end = datetime.datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'

    # Lista de calendarios de Google
    page_token = None
    informe= []
    total_hours_day=0
    while True:
        for calendar_list_entry in calendarios_informe:
            calendar_id = calendar_list_entry['id']
            events = service.events().list(
                calendarId=calendar_id,
                timeMin=today_start,
                timeMax=today_end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            total_hours = 0
            objeto_json = {}
            for event in events.get('items', []):
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                start_time = datetime.datetime.fromisoformat(start)
                end_time = datetime.datetime.fromisoformat(end)
                duration = end_time - start_time
                total_hours += duration.total_seconds() / 3600
            
            # crear objeto json con el nombre del calendario y las horas trabajadas
            objeto_json={
                'id': calendar_list_entry['id'],
                'calendario': calendar_list_entry['summary'],
                'horas': total_hours
            }
            total_hours_day += total_hours
            #si bolean_horas es True se agrega solo cuando total_hours sea mayor a 0
            if bolean_horas:
                if  int(total_hours) > 0:
                    informe.append(objeto_json)

                
            else:
                informe.append(objeto_json)
            # print(f"{calendar_list_entry['summary']}: {total_hours:.2f} horas")                
            # si orderBy es 1 se ordena  por horas de mayor a menor, si es 2 se ordena por horas de menor a mayor y si es culquier otro valor se ordena por nombre del calendario
            if orderBy == 1:
                informe.sort(key=lambda x: x['horas'], reverse=True)
            elif orderBy == 2:
                informe.sort(key=lambda x: x['horas'])
            else:
                informe.sort(key=lambda x: x['calendario'])
            
        
        if not page_token:
            break
        # recorrer informe 
    if(total_hours_day<24):
        informe.append({
            'id': "000000000000",
            'calendario': "Horas libres",
            'horas': 24-total_hours_day})
    
    return informe    
    

informe_por_fecha('2021-06-01')