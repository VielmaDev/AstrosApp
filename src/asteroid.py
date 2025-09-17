import flet as ft
from flet import Page, TextField, ElevatedButton, Column, Row, Text, Container, alignment, Dropdown, dropdown, Colors, Image
import datetime
import requests # Para hacer las llamadas a la API (necesitarás instalarlo: pip install requests)

# --- CONFIGURACIÓN DE LA API DE LA NASA (NeoWs) ---
NASA_API_BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed?"
NASA_API_KEY = "2OYvrWfzSWPDRAburcCkTmIc0iKnAZk88xLwaVq" # ¡IMPORTANTE! Obtén tu propia API Key de NASA para evitar límites: https://api.nasa.gov/
API_DATE_FORMAT = "%Y-%m-%d" # Formato de fecha que la API de la NASA espera (ej: 2023-10-27)
# --- FIN DE LA CONFIGURACIÓN DE LA API ---

def main(page: ft.Page):
    page.title = "Asteroides cercanos a la Tierra (NASA NeoWs)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 500
    page.window_height = 700

    # Texto para mostrar la fecha seleccionada
    selected_date_text = ft.Text("Ninguna fecha seleccionada", size=18)

    # Contenedor para mostrar los resultados de la API
    api_results_container = ft.Column(
        [
            ft.Text("Selecciona una fecha para ver asteroides cercanos a la Tierra.", size=16),
            ft.Divider()
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )

    def on_date_selected(e):
        selected_date = e.control.value
        if selected_date:
            formatted_date = selected_date.strftime(API_DATE_FORMAT)
            selected_date_text.value = f"Fecha seleccionada: {formatted_date}"
            page.update()
            fetch_neo_data(formatted_date)
        else:
            selected_date_text.value = "Ninguna fecha seleccionada"
            page.update()

    def fetch_neo_data(date_to_search: str):
        api_results_container.controls.clear()
        api_results_container.controls.append(ft.ProgressRing())
        api_results_container.controls.append(ft.Text(f"Buscando asteroides para la fecha: {date_to_search}..."))
        page.update()

        try:
            # Construimos la URL para la API NeoWs (usando la misma fecha para start_date y end_date)
            api_url = f"{NASA_API_BASE_URL}?start_date={date_to_search}&end_date={date_to_search}&api_key={NASA_API_KEY}"

            print(f"Realizando llamada a la API de la NASA: {api_url}")
            response = requests.get(api_url, timeout=15) # Aumenta el timeout por si la API tarda
            response.raise_for_status()  # Lanza un error para códigos de estado HTTP 4xx/5xx

            data = response.json()

            api_results_container.controls.clear()
            api_results_container.controls.append(ft.Text(f"Asteroides para {date_to_search}:", size=18, weight=ft.FontWeight.BOLD))

            # La respuesta de NeoWs tiene los asteroides agrupados por fecha
            # Accedemos a los asteroides de la fecha seleccionada
            near_earth_objects_for_date = data.get("near_earth_objects", {}).get(date_to_search, [])

            if near_earth_objects_for_date:
                for neo in near_earth_objects_for_date:
                    neo_name = neo.get("name", "N/A")
                    is_hazardous = "Sí" if neo.get("is_potentially_hazardous_asteroid") else "No"
                    jpl_url = neo.get("nasa_jpl_url", "#")
                    
                    # Obtener el diámetro estimado (ej. en kilómetros)
                    estimated_diameter_km_min = neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min", "N/A")
                    estimated_diameter_km_max = neo.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max", "N/A")

                    # Obtener datos de acercamiento si existen
                    close_approach_data = neo.get("close_approach_data", [])
                    miss_distance_km = "N/A"
                    relative_velocity_kps = "N/A"
                    if close_approach_data:
                        first_approach = close_approach_data[0] # Tomamos el primer acercamiento
                        miss_distance_km = f"{float(first_approach.get('miss_distance', {}).get('kilometers', '0')):.2f} km"
                        relative_velocity_kps = f"{float(first_approach.get('relative_velocity', {}).get('kilometers_per_second', '0')):.2f} km/s"

                    api_results_container.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(f"Nombre: {neo_name}", weight=ft.FontWeight.BOLD, size=16),
                                        ft.Text(f"ID de Referencia NEO: {neo.get('neo_reference_id', 'N/A')}"),
                                        ft.Text(f"¿Potencialmente peligroso?: {is_hazardous}"),
                                        ft.Text(f"Diámetro Estimado (km): {estimated_diameter_km_min:.2f} - {estimated_diameter_km_max:.2f}"),
                                        ft.Text(f"Distancia de Acercamiento: {miss_distance_km}"),
                                        ft.Text(f"Velocidad Relativa: {relative_velocity_kps}"),
                                        ft.FilledButton(
                                            "Ver en NASA JPL",
                                            url=jpl_url,
                                            icon=ft.icons.LINK
                                        )
                                    ]
                                ),
                                padding=10,
                                border_radius=ft.border_radius.all(10)
                            ),
                            margin=ft.margin.only(bottom=10)
                        )
                    )
            else:
                api_results_container.controls.append(ft.Text("No se encontraron asteroides cercanos a la Tierra para esta fecha.", color=ft.colors.ORANGE_500))

        except requests.exceptions.RequestException as e:
            api_results_container.controls.clear()
            api_results_container.controls.append(ft.Text(f"Error de conexión con la API de la NASA: {e}", color=ft.Colors.RED))
        except ValueError as e:
            api_results_container.controls.clear()
            api_results_container.controls.append(ft.Text(f"Error al parsear la respuesta JSON de la API: {e}", color=ft.Colors.RED))
        except Exception as e:
            api_results_container.controls.clear()
            api_results_container.controls.append(ft.Text(f"Ocurrió un error inesperado: {e}", color=ft.Colors.RED))
        finally:
            page.update()

    # Cupertino Date Picker
    cupertino_date_picker= ft.CupertinoDatePicker(
            date_picker_mode=ft.CupertinoDatePickerMode.DATE,
            on_change=on_date_selected,
        )

    page.add(
        ft.AppBar(title=ft.Text("Asteroides Cercanos a la Tierra")),
        ft.Column(
            [
                selected_date_text,
                ft.Container(
                    content= cupertino_date_picker,
                    height=250,
                    width=300,
                    alignment=ft.alignment.center
                ),
                ft.Divider(),
                api_results_container,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
