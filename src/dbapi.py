import flet as ft
import requests, json
from datetime import date

# CONFIGURACIÓN A LA CONEXIÓN DE LAS APIs:

# URLs:
URL_API_APOD="https://api.nasa.gov/planetary/apod?"  # URL de la API APOD
URL_API_NEOWS="https://api.nasa.gov/neo/rest/v1/feed?" # URL de la API NeoWs

# key para acceso:
api_key = "c2OYvrWfzSWPDRAburcCkTmIc0iKnAZk88xLwaVq"

# Parametros de busqueda
now= date.today() # Fecha actual tomada del servidor

def apod(): # Conexión a la Api APOD

        try:
                # Parámetros de busqueda
                params= {
                      "api_key": api_key,
                       "date": now,
                    }
                # Solicitud GET a la API
                response = requests.get(URL_API_APOD, params= params) 

                if response.status_code == 200:
                    apod_data = response.json()  # Se convierte la respuesta a JSON

        except requests.exceptions.RequestException as e:
            apod_data(f"Error al conectar con la API APOD: {e}") # Error de conexión con la api

        except json.JSONDecodeError as e:
            apod_data(ft.Text(f"Error al decodificar JSON: {e}"))  # Manejo de errores al decodificar JSON
        
        return apod_data # Retorno de data
apod()


def neows(): # Conexión a la Api NeoWs
                
        try:
                # Parámetros de busqueda
                params= {
                      "api_key": api_key,
                         "date": now,
                    }
                # Intenta realizar la solicitud GET a la API
                response = requests.get(URL_API_NEOWS, params= params)

                if response.status_code == 200:

                    # Se convierte la respuesta a JSON
                    neows_data = response.json()

        except requests.exceptions.RequestException as e:
            neows_data(f"Error al conectar con la API NeoWs: {e}") # Error de conexión con la api

        except json.JSONDecodeError as e:
           neows_data(ft.Text(f"Error al decodificar JSON: {e}"))  # Maneja errores al decodificar JSON
         
        return neows_data # Retorno de data
neows()