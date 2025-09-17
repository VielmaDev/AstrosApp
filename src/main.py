import flet as ft
from flet import Page, TextField, ElevatedButton, Column, Row, Text, Container, alignment, Dropdown, dropdown, Colors, Image
import news, asteroid
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

        # Conexión con módulo news
        noticia= news.news_today() 

        # Método selector de pestaña
        def tab_chance(e):
            print("Selected tab:", e.control.selected_index)

            if page.navigation_bar.selected_index == 0:
                page.remove(asteroid_container)
                page.add(news_container)
            elif page.navigation_bar.selected_index == 1:
                page.remove(news_container)
                page.add(asteroid_container)

        # Método selector de fecha
        #def handle_date_change(e: ft.ControlEvent):
            #search_fecha.value = f"{e.control.value.strftime(API_DATE_FORMAT)}"
            #page.update()

        # Menú de la app
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.BLUE_600,
            inactive_color=ft.Colors.WHITE,
            active_color=ft.Colors.BLACK,
            on_change = tab_chance, # Selector de pestaña
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME,
                                            selected_icon=ft.Icons.HOME, label="NEWS"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="ASTEROIDES"),
            ],
            selected_index = 0,
        )

        # Widgets news         
        titulo = ft.Text(f"{noticia['title']}", size=28, 
                         color=ft.Colors.BLUE,
                         text_align=ft.TextAlign.CENTER)
        news_titulo = Row(
                        controls=[titulo],
                        alignment="center", # Alineación horizontal
                    )
        
        fecha_objeto = datetime.strptime(noticia['date'], ORIGINAL_API_FORMAT) #Convierte la cadena de la API en un objeto 'datetime'.
        fecha_formateada = fecha_objeto.strftime(API_DATE_FORMAT) # Formatea el objeto `datetime` al nuevo formato de cadena.

        fecha = ft.Text(
                        fecha_formateada,
                        size=16,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER)
        
        news_fecha = Row(
                        controls=[fecha],
                        alignment="center", # Alineación horizontal
                    )
       
        imagen = ft.Image(src=f"{noticia['url']}", width=380, height=380)
        news_imagen = Row(
                        controls=[imagen],
                        alignment="center", # Alineación horizontal
                        vertical_alignment="center"  # Alineación vertical
                    )
        news_contenido = ft.Container(
                content=ft.Column([
                        ft.Text(f"{noticia['explanation']}",size=16,
                                text_align=ft.TextAlign.JUSTIFY,
                                color=ft.Colors.WHITE, 
                            ),
                    ]),
                padding=20)

        # widget asteroid
        neows_titulo = ft.Text("Asteroides Cercanos a la Tierra", size=20,
                                color=ft.Colors.BLUE, 
                                text_align=ft.TextAlign.CENTER)

        neows_titulo = Row(
                        controls=[neows_titulo],
                        alignment="center", # Alineación horizontal
                    )

        neows_container = ft.Text("Seleccione una fecha del calendario.",
                                size=16,
                                color=ft.Colors.BLUE, 
                                text_align=ft.TextAlign.CENTER,
                            )
        neows_container = Column(
                        controls=[neows_container],
                        alignment="center", # Alineación horizontal
                        scroll=ft.ScrollMode.ADAPTIVE,
                        expand=True,
        ) 
                    
        # Contenedor para mostrar los resultados en NeoWs
        neows_container = ft.Container(
                content=ft.Column([
                        ft.Text("Seleccione una fecha del calendario.",
                                size=16,
                                color=ft.Colors.BLUE, 
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ft.Divider(),
                    ], 
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                    ),
                )

        selected_date_text = ft.Text("¡Ninguna fecha seleccionada!", 
                                     size=16)

        # Cupertino Date Picker
        cupertino_date_picker= ft.CupertinoDatePicker(
            date_picker_mode=ft.CupertinoDatePickerMode.DATE,
            #on_change=on_date_selected,
            height=250,
            width=300,
        )
        
        def on_date_selected(e):
            selected_date = e.control.value
            if selected_date:
                formatted_date = selected_date.strftime(API_DATE_FORMAT)
                selected_date_text.value = f"Fecha seleccionada: {formatted_date}"
                page.update()
                #fetch_neo_data(formatted_date)
            else:
                selected_date_text.value = "Ninguna fecha seleccionada"
                page.update()

        
        
        # Contenedor de widgets news
        news_container = Container(
                    content=ft.Column(
                        controls=[
                            news_titulo,
                            news_fecha,
                            news_imagen,
                            news_contenido
                        ],
                    ),padding=20 
                )
        
        # Contenedor de widgets neows
        asteroid_container = Container(
                        content=ft.Column(
                                controls=[
                                    neows_titulo,
                                    neows_container,
                            ],
                    ),padding=20 
                )


        page.add(news_container)
        page.update()

if __name__ == "__main__":
    ft.app(target = myapp)