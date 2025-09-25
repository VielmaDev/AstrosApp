import flet as ft
from flet import Page, TextField, ElevatedButton, Column, Row, Text, Container, alignment, Dropdown, dropdown, Colors, Image
import dbapi
from datetime import datetime
from time import strftime

# ---CONFIGURACIÓN DE FORMATOS ---
ORIGINAL_API_FORMAT = "%Y-%m-%d" # Ejemplo de formato ISO, común en APIs
API_DATE_FORMAT = "%d-%m-%Y" # Formato fecha a convertir.

class myapp:
    def __init__(self, page: ft.Page):
        page.title = "Agenda NASA"
        page.bgcolor = Colors.BLACK26
        page.theme_mode = "dark"
        page.scroll = ft.ScrollMode.ADAPTIVE

        # Conexión con módulo dbapi 
        Apod= dbapi.apod()
        Neows= dbapi.neows() 

        # Método selector de pestaña
        def tab_chance(e):
            print("Selected tab:", e.control.selected_index)

            if page.navigation_bar.selected_index == 0:
                page.remove(asteroid_container)
                page.add(news_container)
            elif page.navigation_bar.selected_index == 1:
                page.remove(news_container)
                page.add(asteroid_container)

        # Menú de la app
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.BLUE_600,
            inactive_color=ft.Colors.WHITE,
            active_color=ft.Colors.BLACK,
            on_change = tab_chance, # Selector de pestaña
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME,
                                            selected_icon=ft.Icons.HOME, label="NEWS"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="ASTEROIDS"),
            ],
            selected_index = 0,
        )

        # Widgets news         
        titulo = ft.Text(f"{Apod['title']}", size=28, 
                         color=ft.Colors.BLUE,
                         text_align=ft.TextAlign.CENTER)
        apod_titulo = Row(
                        controls=[titulo],
                        alignment="center", # Alineación horizontal
                    )
        
        fecha_objeto = datetime.strptime(Apod['date'], ORIGINAL_API_FORMAT) #Convierte la cadena de la API en un objeto 'datetime'.
        fecha_formateada = fecha_objeto.strftime(API_DATE_FORMAT) # Formatea el objeto `datetime` al nuevo formato de cadena.

        fecha = ft.Text(
                        fecha_formateada,
                        size=16,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER)
        
        apod_fecha = Row(
                        controls=[fecha],
                        alignment="center", # Alineación horizontal
                    )
       
        imagen = ft.Image(src=f"{Apod['url']}", width=380, height=380)
        apod_imagen = Row(
                        controls=[imagen],
                        alignment="center", # Alineación horizontal
                        vertical_alignment="center"  # Alineación vertical
                    )
        apod_contenido = ft.Container(
                content=ft.Column([
                        ft.Text(f"{Apod['explanation']}",size=18,
                                color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.JUSTIFY),
                    ]),
                padding=20)

        # widget asteroids
        titulo = ft.Text("Asteroides cercanos a la Tierra", size=20,
                            color=ft.Colors.BLUE, 
                            text_align=ft.TextAlign.CENTER)
        neows_titulo = Row(
                        controls=[titulo],
                        alignment="center", # Alineación horizontal
                    )
        
        id = ft.Text("ID:", size=14, 
                         color=ft.Colors.BLUE,
                         text_align=ft.TextAlign.CENTER)
        neows_id = Row(
                        controls=[id],
                        alignment="center", # Alineación horizontal
                    )
        
        # Contenedor de widgets news
        news_container = Container(
                    content=ft.Column(
                        controls=[
                            apod_titulo,
                            apod_fecha,
                            apod_imagen,
                            apod_contenido
                        ],
                    ),padding=20 
                )
        
        # Contenedor de widgets neows
        asteroid_container = Container(
                        content=ft.Column(
                                controls=[
                                    neows_titulo,
                                    neows_id,
                            ],
                    ),padding=20 
                )

        page.add(news_container)
        page.update()

if __name__ == "__main__":
    ft.app(target = myapp)