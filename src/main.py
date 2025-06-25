import flet as ft
from flet import Page, TextField, ElevatedButton, Column, Row, Text, Container, alignment, Dropdown, dropdown, Colors, Image
import news

class myapp:

    def __init__(self, page: ft.Page):
        page.title = "Agenda NASA"
        page.bgcolor = Colors.BLACK26
        page.theme_mode = "dark"
        page.scroll = ft.ScrollMode.ADAPTIVE
        
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.BLUE_600,
            inactive_color=ft.Colors.WHITE,
            active_color=ft.Colors.BLACK,
            on_change=lambda e: print("Selected tab:", e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.NEWSPAPER, 
                                            selected_icon=ft.Icons.NEWSPAPER, label="News"),
                ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="Calendar"),
            ],
        )

        datos= news.news_today() #Identación del módulo news para la API NASA

        fecha = ft.Text(f"{datos['date']}", size=16, color=ft.Colors.WHITE)
        news_fecha = Row(
                            controls=[fecha],
                            alignment="center", # Alineación horizontal
                        )

                    
        titulo = ft.Text(f"{datos['title']}", size=26, color=ft.Colors.WHITE, 
                         max_lines=2)
        news_titulo = Row(
                        controls=[titulo],
                        alignment="center", # Alineación horizontal
                    )
        
        imagen = ft.Image(src=f"{datos['url']}", width=380, height=380)
        news_imagen = Row(
                        controls=[imagen],
                        spacing=2,
                        alignment="center", # Alineación horizontal
                        vertical_alignment="center" # Alineación vertical
                    )
        
        news_contenido = ft.Container(
                content=ft.Column([
                        ft.Text(f"{datos['explanation']}",size=16,
                                text_align=ft.TextAlign.JUSTIFY,
                                color=ft.Colors.WHITE, 
                            ),
                    ]),
                padding=25)
        
        news_autor = ft.Text(f"Autor(es): {datos['copyrights']}", size=14,
                        color=ft.Colors.YELLOW, 
                        max_lines=2,)
        autor = Row(
                        controls=[news_autor],
                        spacing=5,
                        alignment="center", # Alineación horizontal
                        vertical_alignment="center" # Alineación vertical
                    )


        # Agrega el widget a la página
        page.add(news_fecha, news_titulo, news_imagen, news_contenido)

        # Actualiza la interfaz Flet
        page.update()

ft.app(target=myapp)
