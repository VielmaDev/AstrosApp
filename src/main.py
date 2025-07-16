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
                page.remove(asteroide_container)
                page.add(news_container)
               
            elif page.navigation_bar.selected_index == 1:
                page.remove(news_container)
                page.add(asteroide_container)

        #Método selector de fecha
        def handle_date_change(e: ft.ControlEvent):
            search_fecha.value = f"{e.control.value.strftime('%d-%m-%Y')}"
            page.update()


        #Menú de la app
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.BLUE_600,
            inactive_color=ft.Colors.WHITE,
            active_color=ft.Colors.BLACK,
            on_change = tab_chance, #Selector de pestaña
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME,
                                            selected_icon=ft.Icons.HOME, label="NEWS"),
                ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="ASTEROIDES"),
            ],
            selected_index = 0,
        )

        # Widgets news         
        titulo = ft.Text(f"{datos['title']}", size=28, 
                         color=ft.Colors.BLUE,
                         text_align=ft.TextAlign.CENTER)
        news_titulo = Row(
                        controls=[titulo],
                        alignment="center", # Alineación horizontal
                    )
        fecha = ft.Text(f"{datos['date']}", size=16, 
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER)
        news_fecha = Row(
                        controls=[fecha],
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

        #widget asteroides
        label= ft.Text(f"Asteroides-NeoWs", size=26, 
                         color=ft.Colors.BLUE,
                         text_align=ft.TextAlign.CENTER)
        label_title = Row(
                        controls=[label],
                        alignment="center", # Alineación horizontal
                    )
        
        cupertino_date_picker = ft.CupertinoDatePicker(
            date_picker_mode=ft.CupertinoDatePickerMode.DATE,
            on_change=handle_date_change, 
        )

        buttom = ft.CupertinoFilledButton("Buscar",
            on_click=lambda e: page.open(
                ft.CupertinoBottomSheet(
                    cupertino_date_picker,
                    height=150,
                    padding=ft.padding.only(top=5),
                )
            ),
        )
        search_buttom = Row(
                        controls=[buttom],
                        alignment="center", # Alineación horizontal
                    )
        
        search_fecha = ft.Text(f" ", size=16, 
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER)
        search_date = Row(
                        controls=[search_fecha],
                        alignment="center", # Alineación horizontal
                    )
         
        #Contenedor de widgets news
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
        
        #Contenedor de widgets asteroides
        asteroide_container = Container(
                    content=ft.Column(
                        controls=[
                            label_title,
                            search_buttom,
                            search_date,
                            cupertino_date_picker
                        ],
                    ),padding=10 
                ) 
        
        page.add(news_container)
        page.update()

if __name__ == "__main__":
    ft.app(target = myapp)
