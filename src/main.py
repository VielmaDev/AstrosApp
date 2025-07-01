import flet as ft
from flet import Page, TextField, ElevatedButton, Column, Row, Text, Container, alignment, Dropdown, dropdown, Colors, Image
import news

class myapp:
    def __init__(self, page: ft.Page):
        page.title = "Agenda NASA"
        page.bgcolor = Colors.BLACK26
        page.theme_mode = "dark"
        page.scroll = ft.ScrollMode.ADAPTIVE

        #Conexión con módulo news
        datos= news.news_today() 

        #Método selector de pestaña
        def tab_chance(e):
            print("Selected tab:", e.control.selected_index)

            if page.navigation_bar.selected_index == 0:
                page.remove(news_fecha)
                page.add(news_container)
               
            elif page.navigation_bar.selected_index == 1:
                page.remove(news_container)
                page.add(news_fecha)

        #Menú de la app
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.BLUE_600,
            inactive_color=ft.Colors.WHITE,
            active_color=ft.Colors.BLACK,
            on_change = tab_chance,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.NEWSPAPER,
                                            selected_icon=ft.Icons.NEWSPAPER, label="News"),
                ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="Calendar"),
            ],
            selected_index = 0,
        )

        # Widgets de la app
        fecha = ft.Text(f"{datos['date']}", size=16, 
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER)
        news_fecha = Row(
                        controls=[fecha],
                        alignment="center", # Alineación horizontal
                    )
                    
        titulo = ft.Text(f"{datos['title']}", size=28, 
                         color=ft.Colors.BLUE,
                         text_align=ft.TextAlign.CENTER)
        news_titulo = Row(
                        controls=[titulo],
                        alignment="center", # Alineación horizontal
                    )
        
        imagen = ft.Image(src=f"{datos['url']}", width=380, height=380)
        news_imagen = Row(
                        controls=[imagen],
                        alignment="center", # Alineación horizontal
                        vertical_alignment="center"  # Alineación vertical
                    )
        
        news_contenido = ft.Container(
                content=ft.Column([
                        ft.Text(f"{datos['explanation']}",size=16,
                                text_align=ft.TextAlign.JUSTIFY,
                                color=ft.Colors.WHITE, 
                            ),
                    ]),
                padding=20)
        
        autor = ft.Text(f"Copyright. {datos['copyright']}", size=14,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.YELLOW,  
                    )
        news_autor = Row(
                        controls=[autor],
                        alignment="center", # Alineación horizontal
                    )
        
        #Contenedor de widgets
        news_container = Container(
                    content=ft.Column(
                        controls=[
                            news_fecha,
                            news_titulo,
                            news_imagen,
                            news_contenido,
                            news_autor
                        ],
                    ),padding=20 
                ) 
         
        page.add(news_container)
        page.update()

if __name__ == "__main__":
    ft.app(target = myapp)
