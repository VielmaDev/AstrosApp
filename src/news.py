import flet as ft
import requests, json
from datetime import date

def news_today():
    
        #fecha actual tomada del servidor
        now=date.today()

        #API APOD que permite consultar la imagen del día publicada por la NASA
        URL_API="https://api.nasa.gov/planetary/apod?"
                
        try:
                #parámetros de busqueda
                params= {
                        "api_key":"c2OYvrWfzSWPDRAburcCkTmIc0iKnAZk88xLwaVq",
                        "date": now,
                    }
                # Intenta realizar la solicitud GET a la API
                response = requests.get(URL_API, params=params)

                if response.status_code == 200:

                    # Se convierte la respuesta a JSON
                    data = response.json()

        except requests.exceptions.RequestException as e:
            data(f"Error al conectar con la API: {e}")

        except json.JSONDecodeError as e:
            # Maneja errores al decodificar JSON
            data(ft.Text(f"Error al decodificar JSON: {e}"))
        
        return data

news_today()