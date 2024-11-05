import math
import flet as ft

def main(page: ft.Page):
    page.window.width = 420
    page.window.height = 720
    page.padding = 0
    page.window.title_bar_hidden = True
    page.window.center()
    # page.scroll = True
    page.fonts = {
        "mono123": r"C:\Users\marco\Documents\GitHub\SisFin\files\fonts\GeistMono-1.4.01\GeistMono-1.4.01\otf\GeistMono-Black.otf",
        "mono1234": r"C:\Users\marco\Documents\GitHub\SisFin\files\fonts\GeistMono-1.4.01\GeistMono-1.4.01\otf\GeistMono-Ligth.otf",
    }
    
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Column(
                        [ft.Text("", size=20, font_family="mono123"),ft.Text("MINIMAL", size=20, font_family=r"C:\Users\marco\Documents\GitHub\SisFin\files\fonts\GeistMono-1.4.01\GeistMono-1.4.01\otf\GeistMono-Black.otf"),],
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
                                            [ft.Container(content=ft.Text("Contas", size=14, font_family="mono1234", color="#ffffff"))],
                                            alignment=ft.MainAxisAlignment.START,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                            # height=50,
                                            width=300
                                        ),
                                        ft.Container(
                                            border=ft.border.all(1, "#ffffff"),
                                            width=300,
                                            height=70,
                                            border_radius=100,
                                        ),
                                    ],
                                    scroll=True,
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=20,
                                ),
                                # border=ft.border.all(2, ft.colors.BLACK),
                                # ink_color=ft.colors.RED,
                                width=500,
                                # height=200,
                                padding=20,
                                bgcolor="#001829",
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
            # alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0, 1),
                colors=[
                    "#FF204E",
                    "#00224D",
                ],
                tile_mode=ft.GradientTileMode.CLAMP,
                rotation=math.pi / 3,
            ),
            width=420,
            # height=877,
            # border_radius=20,
            margin=0,
            padding=0
        )
    )

ft.app(target=main)
