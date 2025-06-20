import flet as ft
from flet import Page, TextField, ElevatedButton, Column, Row, Text, Container, alignment, Dropdown, dropdown, Colors, Image

class myapp:

    def __init__(self, page: ft.Page):
        page.title = "Agenda NASA"
        page.bgcolor = Colors.BLACK26
        page.theme_mode = "dark"
        page.scroll = ft.ScrollMode.ADAPTIVE
        
        page.navigation_bar = ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.BLUE_600,
            inactive_color=ft.Colors.BLACK,
            active_color=ft.Colors.WHITE,
            on_change=lambda e: print("Selected tab:", e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.BOOKMARK_BORDER, 
                                            selected_icon=ft.Icons.BOOKMARK, label="News"),
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
            ],
        )

        # Actualiza la interfaz Flet
        page.update()

ft.app(target=myapp)
