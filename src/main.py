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
                                            selected_icon=ft.Icons.HOME, label="News"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Asteroids"),
            ],
            selected_index = 0,
        )

        # Widgets News         
        label = ft.Text(f"{Apod['title']}", size=25, 
                         color=ft.Colors.BLUE,
                         text_align=ft.TextAlign.CENTER)
        apod_label = Row(
                        controls=[label],
                        alignment="center", # Alineación horizontal
                    )
        
        date_objeto = datetime.strptime(Apod['date'], ORIGINAL_API_FORMAT) #Convierte la cadena de la API en un objeto 'datetime'.
        date_format = date_objeto.strftime(API_DATE_FORMAT) # Formatea el objeto `datetime` al nuevo formato de cadena.

        dates = ft.Text(
                        date_format,
                        size=17,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER)
        
        apod_date = Row(
                        controls=[dates],
                        alignment="center", # Alineación horizontal
                    )
       
        imagen = ft.Image(src=f"{Apod['url']}", width=380, height=380)
        apod_imagen = Row(
                        controls=[imagen],
                        alignment="center", # Alineación horizontal
                        vertical_alignment="center"  # Alineación vertical
                    )
        apod_content = ft.Container(
                content=ft.Column([
                        ft.Text(f"{Apod['explanation']}",size=16,
                                color=ft.Colors.WHITE,
                                text_align=ft.TextAlign.JUSTIFY),
                    ]),
                padding=20)

        # widget Asteroids
        label = ft.Text("Asteroides cercanos a la Tierra", size=23,
                            color=ft.Colors.BLUE, 
                            text_align=ft.TextAlign.CENTER)
        neows_label = Row(
                        controls=[label],
                        alignment="center", # Alineación horizontal
                    )

        count = ft.Text("Cantidad de elementos: ", size=16,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER)

        neows_count = Row(
                        controls=[count],
                        alignment="center", # Alineación horizontal
        )
        
        table= ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Id")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Magnitude")),
                ft.DataColumn(ft.Text("Diameter")),
                ft.DataColumn(ft.Text("Hazardous")),
                ft.DataColumn(ft.Text("Approach date full")),
                ft.DataColumn(ft.Text("Velocity")),
                ft.DataColumn(ft.Text("Miss distance")),
                ft.DataColumn(ft.Text("Orbiting body")),

            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ],
                ),
                
            ],
        )

        neows_table= Row(
                        controls=[table],
                        alignment="center", # Alineación horizontal
                    )
        
        # Contenedor de widgets news
        news_container = Container(
                    content=ft.Column(
                        controls=[
                            apod_label,
                            apod_date,
                            apod_imagen,
                            apod_content
                        ],
                    ),padding=20 
                )
        
        # Contenedor de widgets neows
        asteroid_container = Container(
                        content=ft.Column(
                                controls=[
                                    neows_label,
                                    neows_count,
                                    neows_table,
                            ],
                    ),padding=20 
                )

        page.add(news_container)
        page.update()

if __name__ == "__main__":
    ft.app(target = myapp)