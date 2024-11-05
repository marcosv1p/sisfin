import math
import flet as ft
from datetime import datetime

def main(page: ft.Page):
    # Page Settings
    page.padding = 0
    page.window.width = 420
    page.window.height = 720
    page.window.title_bar_hidden = True
    page.window.center()
    page.bgcolor = "#1A1A1A"
    
    # Load Fonts
    page.fonts = {
        "Geist-Black": "",
        "Geist-Bold": "fonts/Geist/ttf/Geist-Bold.ttf",
        "Geist-ExtraBold": "fonts/Geist/ttf/Geist-ExtraBold.ttf",
        "Geist-ExtraLight": "fonts/Geist/ttf/Geist-ExtraLight.ttf",
        "Geist-Light": "fonts/Geist/ttf/Geist-Light.ttf",
        "Geist-Medium": "fonts/Geist/ttf/Geist-Medium.ttf",
        "Geist-Regula": "fonts/Geist/ttf/Geist-Regular.ttf",
        "Geist-SemiBold": "fonts/Geist/ttf/Geist-SemiBold.ttf",
        "Geist-Thin": "fonts/Geist/ttf/Geist-Thin.ttf",
    }
    
    page.theme = ft.Theme(font_family="Geist-Black")
    page.scroll = True
    
    # Colors
    COLOR01 = "#D3D3D3" # Branco
    COLOR02 = "#1A1A1A" # Cinza
    COLOR03 = "#FF204E" # Magenta
    COLOR04 = "#A0153E" # Magenta Escuro
    COLOR05 = "#5D0E41" # Roxo
    COLOR06 = "#00224D" # Azul Escuro
    COLOR07 = "#A2E3C4" # Verde Limão
    COLOR08 = "#597D6E" # Verde Musgo
    
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary = COLOR03,
            on_primary = COLOR01,
            primary_container = COLOR01,
            on_primary_container = COLOR01,
            secondary = COLOR03,
            on_secondary = COLOR01,
            secondary_container = COLOR01,
            on_secondary_container = COLOR01,
            tertiary = COLOR03,
            on_tertiary = COLOR03,
            tertiary_container = COLOR03,
            on_tertiary_container = COLOR03,
            error = COLOR01,
            on_error = COLOR01,
            error_container = COLOR01,
            on_error_container = COLOR01,
            background = COLOR01,
            on_background = COLOR01,
            surface = COLOR03,
            on_surface = COLOR03,
            surface_variant = COLOR04,
            on_surface_variant = COLOR04,
            outline = COLOR04,
            outline_variant = COLOR01,
            shadow = COLOR01,
            scrim = COLOR02,
            inverse_surface = COLOR03,
            on_inverse_surface = COLOR03,
            inverse_primary = COLOR04,
            surface_tint = COLOR03
        ),
    )
    
    # Telas
    def homepage(*args):
        def title(text):
            ttl = ft.Container(
                ft.Text(text, color=COLOR01, font_family="Verdana", size=16, weight=ft.FontWeight.W_300),
                margin=ft.margin.only(50, 20),
            )
            return ttl
        
        page.clean()
        
        structure = ft.Container()
        structure.content = ft.Column()
        # structure.bgcolor = "#d3d3d3"
        structure.width = 1000
        svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg id="Camada_2" data-name="Camada 2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 186.12 56.69">
  <defs>
    <style>
      .cls-1 {
        fill: #d3d3d3;
      }
    </style>
  </defs>
  <g id="Camada_1-2" data-name="Camada 1">
    <g>
      <rect class="cls-1" x="32.51" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(89.2 2.08) rotate(90)"/>
      <rect class="cls-1" x="76.07" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(132.76 -41.48) rotate(90)"/>
      <g>
        <rect class="cls-1" x="48.35" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(105.04 -13.76) rotate(90)"/>
        <rect class="cls-1" x="64.28" y="45.73" width="14" height="7.92" rx="3.74" ry="3.74" transform="translate(120.97 -21.59) rotate(90)"/>
      </g>
      <g>
        <rect class="cls-1" x="-7.09" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(49.6 41.68) rotate(90)"/>
        <rect class="cls-1" x="16.67" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(73.36 17.92) rotate(90)"/>
        <rect class="cls-1" x="8.84" y="37.63" width="14" height="7.92" rx="3.74" ry="3.74" transform="translate(57.43 25.75) rotate(90)"/>
      </g>
      <g>
        <rect class="cls-1" x="143.39" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(200.08 -108.8) rotate(90)"/>
        <rect class="cls-1" x="138.13" y="41.68" width="8.86" height="7.92" rx="3.74" ry="3.74" transform="translate(188.2 -96.92) rotate(90)"/>
      </g>
      <g>
        <rect class="cls-1" x="159.23" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(215.92 -124.64) rotate(90)"/>
        <rect class="cls-1" x="177.73" y="48.3" width="8.86" height="7.92" rx="3.74" ry="3.74" transform="translate(234.42 -129.9) rotate(90)"/>
      </g>
      <g>
        <rect class="cls-1" x="91.91" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(148.6 -57.32) rotate(90)"/>
        <rect class="cls-1" x="115.67" y="41.68" width="22.11" height="7.92" rx="3.74" ry="3.74" transform="translate(172.36 -81.08) rotate(90)"/>
        <rect class="cls-1" x="107.84" y="37.63" width="14" height="7.92" rx="3.74" ry="3.74" transform="translate(156.43 -73.25) rotate(90)"/>
      </g>
      <path class="cls-1" d="M0,7.68h7.03l.16,3.4c1.13-2.51,3.27-3.88,5.82-3.88,3.03,0,5.09,1.7,6.02,4.41,1.09-2.91,3.32-4.41,6.02-4.41,4.33,0,7.4,2.79,7.4,8.29v14.03h-7.84v-11.72c0-3.07-.65-4.57-2.47-4.57-1.7,0-2.51,1.66-2.51,4.57v11.72h-6.87v-11.72c0-3.07-.61-4.57-2.43-4.57-1.7,0-2.51,1.66-2.51,4.57v11.72H0V7.68Z"/>
      <path class="cls-1" d="M38.26,0h8.09v5.5h-8.09V0ZM38.39,7.68h7.84v21.83h-7.84V7.68Z"/>
      <path class="cls-1" d="M54.85,7.84h7.03l.16,3.36c1.21-2.83,3.52-3.84,6.31-3.84,4.53,0,7.48,2.95,7.48,8.29v14.03h-7.84v-11.32c0-3.15-.4-4.97-2.51-4.97-1.98,0-2.79,1.82-2.79,4.97v11.32h-7.84V7.84Z"/>
      <path class="cls-1" d="M83.08.16h8.09v5.5h-8.09V.16ZM83.2,7.84h7.84v21.83h-7.84V7.84Z"/>
      <path class="cls-1" d="M98.61,7.84h7.03l.16,3.4c1.13-2.51,3.27-3.88,5.82-3.88,3.03,0,5.09,1.7,6.02,4.41,1.09-2.91,3.32-4.41,6.02-4.41,4.33,0,7.4,2.79,7.4,8.29v14.03h-7.84v-11.72c0-3.07-.65-4.57-2.47-4.57-1.7,0-2.51,1.66-2.51,4.57v11.72h-6.87v-11.72c0-3.07-.61-4.57-2.43-4.57-1.7,0-2.51,1.66-2.51,4.57v11.72h-7.84V7.84Z"/>
      <path class="cls-1" d="M136.74,24.18c0-3.88,2.63-5.78,7.4-6.79l6.55-1.37c0-2.26-1.01-3.48-2.75-3.48s-2.83.89-3.07,2.63l-7.76-.24c.85-5.26,4.69-7.56,10.83-7.56,7.12,0,10.59,3.07,10.59,9.3v6.39c0,1.41.49,1.7,1.29,1.7h.44v4.93c-.49.16-1.74.32-2.75.32-2.02,0-4.53-.65-5.22-3.68-1.13,2.39-3.6,3.84-7.68,3.84-4.61,0-7.88-2.18-7.88-5.98ZM150.68,21.1v-.73l-3.56.89c-1.37.32-2.34,1.05-2.34,2.18s.61,1.78,2.02,1.78c2.18,0,3.88-1.29,3.88-4.12Z"/>
      <path class="cls-1" d="M166.32,22.8V.81h7.84v21.1c0,1.54.73,2.06,2.02,2.06h1.17v5.54h-4.41c-4.2,0-6.63-1.94-6.63-6.71Z"/>
    </g>
  </g>
</svg>"""
        structure.content.controls = [ft.Image(src=svg, height=50, color=COLOR01)]
        structure.alignment = ft.alignment.center
        structure.padding = ft.padding.only(top=50, bottom=10)
        
        page.add(structure)
        
        dashboard = ft.Container()
        dashboard.content = ft.Column()
        dashboard.bgcolor = COLOR01
        dashboard.width = 1000
        
        block00 = ft.CupertinoButton(
            content=ft.Row(
                [   
                    ft.Icon(name=ft.icons.KEYBOARD_ARROW_DOWN_ROUNDED, color=COLOR02, size=30),
                    ft.Text("OUTUBRO", color=COLOR02, font_family="Verdana", size=16, weight=ft.FontWeight.W_400),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime(year=2023, month=10, day=1),
                    last_date=datetime(year=2024, month=10, day=1),
                    # on_change=handle_change,
                    # on_dismiss=handle_dismissal,
                )
            )
        )
        
        block01 = ft.Column(
            [
                ft.Text("Saldo em contas", color=COLOR02, font_family="Verdana", size=16, weight=ft.FontWeight.W_300),
                ft.Text("R$ 2.000,00", color=COLOR02, font_family="Verdana", size=26, weight=ft.FontWeight.W_900),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        
        subblock01 = ft.CupertinoButton(
            content=ft.Row(
                [   
                    ft.Icon(name=ft.icons.TRENDING_UP_ROUNDED, color=COLOR08, size=40),
                    ft.Column(
                        [
                            ft.Text("Receitas", color=COLOR02, font_family="Verdana", size=14, weight=ft.FontWeight.W_100),
                            ft.Text("R$ 2.000,00", color=COLOR08, font_family="Verdana", size=22, weight=ft.FontWeight.W_900),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=0,
                    )
                ],
                spacing=10,
            )
        )
        subblock02 = ft.CupertinoButton(
            content=ft.Row(
                [   
                    ft.Icon(name=ft.icons.TRENDING_DOWN_ROUNDED, color=COLOR04, size=40),
                    ft.Column(
                        [
                            ft.Text("Despesas", color=COLOR02, font_family="Verdana", size=14, weight=ft.FontWeight.W_100),
                            ft.Text("R$ 2.000,00", color=COLOR04, font_family="Verdana", size=22, weight=ft.FontWeight.W_900),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=0,
                    )
                ],
                spacing=10,
            )
        )
        
        block02 = ft.Row(
            [
                subblock01,
                subblock02
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        dashboard.content.controls.extend([block00, block01, block02])
        dashboard.content.spacing = 0
        dashboard.content.alignment = ft.MainAxisAlignment.CENTER
        dashboard.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        dashboard.alignment = ft.alignment.center
        dashboard.padding = ft.padding.all(0)
        
        page.add(title("Balanço"))
        page.add(dashboard)
        
        
        banner01 = ft.CupertinoButton(
            content=ft.Row(
                [   
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Image(border_radius=1000, src="https://play-lh.googleusercontent.com/JCYKHXuu2Q6IzhmkW9N4bDX0S8_3XVYnlPtheNcdwlOaSr0TTKJljm3RVexsXkw3_ec=w240-h480-rw"),
                                border_radius=1000,
                                width=50,
                                height=50,
                                border=ft.border.all(0.5, color=COLOR02),
                                padding=5,
                            ),
                            ft.Column(
                                [
                                    ft.Text("Inifite Pay", color=COLOR02, font_family="Verdana", size=16, weight=ft.FontWeight.W_300),
                                    ft.Text("R$ 2.000,00", color=COLOR08, font_family="Verdana", size=20, weight=ft.FontWeight.W_900),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=0,
                            )
                        ]
                    ),
                    ft.Icon(name=ft.icons.KEYBOARD_ARROW_RIGHT_ROUNDED, color=COLOR02)
                ],
                spacing=10,
                width=400,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        
        
        
        caption = ft.Column(
            [
                ft.Text("Contas ", color=COLOR02, font_family="Verdana", size=16, weight=ft.FontWeight.W_300)
            ],
            alignment=ft.MainAxisAlignment.START,
            # width=300
        )
        
        accounts_area = ft.Container()
        accounts_area.content = ft.Column()
        accounts_area.bgcolor = COLOR01
        accounts_area.width = 1000
        # accounts_area.content.controls.append(caption)
        accounts_area.content.controls.extend([banner01 for i in range(10)])
        accounts_area.content.spacing = 0
        accounts_area.content.alignment = ft.MainAxisAlignment.CENTER
        accounts_area.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        accounts_area.alignment = ft.alignment.center
        accounts_area.padding = ft.padding.all(0)
        
        page.add(title("Contas"))
        page.add(accounts_area)
    
    
    homepage()
    
    
    
    
    
    """
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Column(
                        [ft.Text("", size=20, font_family="mono123"),ft.Text("MINIMAL", size=20, font_family=r"Geist Extraleve"),],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        height=100,
                        # spacing=10
                    ),
                    # ft.Text("This is a new app...", size=14, font_family="mono1234"),
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [ft.Container(content=ft.Text("Contas", size=14, font_family="mono1234",))], # color="#2b2b2b"))],
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            # height=50,
                                            width=350
                                            
                                        ),
                                        ft.Container(
                                            content=ft.Row(
                                                [   
                                                    ft.Container(content=ft.Container(content=ft.Image(src_base64="iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"),
                                                            bgcolor="#2b2b2b",
                                                            border_radius=100,
                                                            width=50,
                                                            height=50,
                                                        ),
                                                        width=70,
                                                        height=70,
                                                        border=ft.border.all(2, "#2b2b2b"),
                                                        border_radius=100,
                                                        padding=5,
                                                    ),
                                                    ft.Column(
                                                        [
                                                            ft.Text("Conta Flet", size=14, font_family="mono123", color="#2b2b2b"),
                                                            ft.Text("R$ 1.234,56", size=20, font_family="mono123", color="#597D6E"),
                                                        ],
                                                        spacing=0,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                    ),
                                                ],
                                                spacing=20,
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            # border=ft.border.all(1,), #"#2b2b2b"),
                                            width=350,
                                            # height=70,
                                            # border_radius=100,
                                            alignment=ft.alignment.center_left,
                                            padding=ft.padding.symmetric(5, 20),
                                            # on_click=lambda e: print(e),
                                        ),
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.Image(src_base64="iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"),
                                                    ft.Column(
                                                        [
                                                            ft.Text("Conta Flet", size=14, font_family="mono1234",), # color="#2b2b2b"),
                                                            ft.Text("R$ 1.234,56", size=20, font_family="mono1234",), # color="#2b2b2b"),
                                                        ],
                                                        spacing=0,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                    ),
                                                ],
                                                spacing=20,
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            border=ft.border.all(1,), #"#2b2b2b"),
                                            width=350,
                                            # height=70,
                                            border_radius=100,
                                            alignment=ft.alignment.center_left,
                                            padding=ft.padding.symmetric(5, 20),
                                            # on_click=lambda e: print(e),
                                        ),
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.Image(src_base64="iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"),
                                                    ft.Column(
                                                        [
                                                            ft.Text("Conta Flet", size=14, font_family="mono1234",), # color="#2b2b2b"),
                                                            ft.Text("R$ 1.234,56", size=20, font_family="mono1234",), # color="#2b2b2b"),
                                                        ],
                                                        spacing=0,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                    ),
                                                ],
                                                spacing=20,
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            border=ft.border.all(1,), #"#2b2b2b"),
                                            width=350,
                                            # height=70,
                                            border_radius=100,
                                            alignment=ft.alignment.center_left,
                                            padding=ft.padding.symmetric(5, 20),
                                            # on_click=lambda e: print(e),
                                        ),
                                        ft.Container(
                                            content=ft.Row(
                                                [
                                                    ft.Image(src_base64="iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"),
                                                    ft.Column(
                                                        [
                                                            ft.Text("Conta Flet", size=14, font_family="mono1234",), # color="#2b2b2b"),
                                                            ft.Text("R$ 1.234,56", size=20, font_family="mono1234",), # color="#2b2b2b"),
                                                        ],
                                                        spacing=0,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                    ),
                                                ],
                                                spacing=20,
                                                alignment=ft.MainAxisAlignment.START,
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            ),
                                            border=ft.border.all(1,), #"#2b2b2b"),
                                            width=350,
                                            # height=70,
                                            border_radius=100,
                                            alignment=ft.alignment.center_left,
                                            padding=ft.padding.symmetric(5, 20),
                                            # on_click=lambda e: print(e),
                                        ),
                                    ],
                                    scroll=True,
                                    # alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                # border=ft.border.all(2, ft.colors.BLACK),
                                # ink_color=ft.colors.RED,
                                width=500,
                                # height=200,
                                padding=20,
                                bgcolor="#d3d3d3",
                            ),
                        ],
                        spacing=200,
                        # alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=200,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=True,
                height=1000
                ),
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0, 1),
                colors=[
                    "#2b2b2b",
                    # "#00224D",
                ],
                tile_mode=ft.GradientTileMode.CLAMP,
                # rotation=math.pi / 3,
            ),
            width=420,
            # height=877,
            # border_radius=20,
            margin=0,
            padding=0
        )
    )"""

ft.app(target=main, assets_dir="files", view=ft.AppView.WEB_BROWSER, web_renderer=ft.WebRenderer.HTML)
