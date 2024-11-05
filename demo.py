# from infra.repository.bank_account_repository import BankAccountRepository
# from infra.repository.bank_repository import BankRepository
# from infra.configs.connection import DBConnectionHandler
# from infra.entities.bank_account import BankAccount
# from infra.entities.bank import Bank  # Importa o modelo Bank
# from infra.configs.base import Base

# if __name__ == "__main__":
#     # Usando o gerenciador de contexto para lidar com a conexão e a sessão
#     repo_ac = BankAccountRepository()
#     repo_bk = BankRepository()
#     a = repo_ac.insert("Teste", 0.0, repo_bk.select()[1])
#     print(repo_ac.select())
#     print(a)
#     print()
    
#     print(a)
    
#     # repo_bk.insert(name="BANK 999999", description="TESTE")


import math
import flet as ft

def main(page: ft.Page):

    page.add(
        ft.Container(
            alignment=ft.alignment.center,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                    "0xff870160",
                    "0xffac255e",
                    "0xffca485c",
                    "0xffe16b5c",
                    "0xfff39060",
                    "0xffffb56b",
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 3,
            ),
            width=150,
            height=150,
            border_radius=5,
        )
    )

ft.app(target=main)
