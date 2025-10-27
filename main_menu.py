import customtkinter as ctk
from PIL import Image
from utils import resource_path
import os

from ui.tela_interfones import TelaInterfones
from ui.tela_leitor_facial import TelaLeitorFacial
from ui.tela_lpr import TelaLPR
from ui.tela_controladora import TelaControladora
from ui.tela_computadores import TelaComputadores
from ui.tela_raspberry_orangepi import TelaRaspberryOrangePi
from ui.tela_antena import TelaAntenas
from ui.tela_biometrico import TelaBiometrico
from ui.tela_cameras import TelaCameras
from ui.tela_roteadores import TelaRoteadores
from ui.relatorio_pdf import RelatorioPDF
from ui.tela_outros import TelaOutros


class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Menu de Dispositivos")

        # === TELA CHEIA GARANTIDA ===
        self.state("zoomed")  # Maximiza a janela no Windows
        self.attributes("-fullscreen", True)  # Tela cheia real
        self.bind("<Escape>", self.toggle_fullscreen)  # Permite sair com ESC

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def toggle_fullscreen(self, event=None):
        """Alterna entre modo tela cheia e modo janela."""
        is_fullscreen = self.attributes("-fullscreen")
        self.attributes("-fullscreen", not is_fullscreen)

    def create_widgets(self):
        # === Cabeçalho ===
        header = ctk.CTkFrame(self, fg_color="#F0F0F0", height=50)
        header.pack(fill="x", side="top")

        title_label = ctk.CTkLabel(header, text="Menu de Dispositivos", font=("Arial", 22, "bold"))
        title_label.pack(side="top", padx=20)

        btn_minimize = ctk.CTkButton(
            header, text="_", width=30, height=30,
            font=("Arial", 18),
            fg_color="#CCCCCC", hover_color="#AAAAAA", text_color="black",
            command=self.iconify
        )
        btn_minimize.pack(side="right", padx=(0, 10), pady=10)

        btn_close = ctk.CTkButton(
            header, text="X", width=30, height=30,
            font=("Arial", 14, "bold"),
            fg_color="#FF6B6B", hover_color="#FF3B3B", text_color="white",
            command=self.destroy
        )
        btn_close.pack(side="right", padx=10, pady=10)

        # === Frame dos botões ===
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(expand=True, fill="both", padx=40, pady=20)

        buttons = [
            ("interfone.png", "Interfone"),
            ("leitor_facial.png", "Leitor Facial"),
            ("lpr.png", "LPR"),
            ("controladora.png", "Controladora SEC"),
            ("computador.png", "Computadores"),
            ("raspberry.png", "Raspberry/Orangepi"),
            ("antena.png", "Antena TAG"),
            ("biometrico.png", "Leitor Biométrico"),
            ("camera.png", "Câmeras"),
            ("roteador.png", "Roteador"),
            ("relatorio.png", "Relatórios"),
            ("outros.png", "Outros"),
        ]

        columns = 4
        for i in range(columns):
            grid_frame.grid_columnconfigure(i, weight=1)

        for idx, (icon_name, label) in enumerate(buttons):
            row = idx // columns
            col = idx % columns

            img_path = resource_path(os.path.join("assets", icon_name))
            image = ctk.CTkImage(light_image=Image.open(img_path), size=(60, 60)) if os.path.exists(img_path) else None

            btn = ctk.CTkButton(
                master=grid_frame,
                image=image,
                text=label,
                font=("Arial", 14),
                compound="top",
                width=140,
                height=140,
                corner_radius=12,
                fg_color="#E6F0FF",
                hover_color="#CCE0FF",
                text_color="black",
                command=lambda l=label: self.handle_click(l)
            )
            btn.grid(row=row, column=col, padx=30, pady=30, sticky="nsew")

    def handle_click(self, label):
        if label == "Interfone":
            self.withdraw()
            TelaInterfones(master=self)

        elif label == "Leitor Facial":
            self.withdraw()
            TelaLeitorFacial(master=self)

        elif label == "LPR":
            self.withdraw()
            TelaLPR(master=self)

        elif label == "Controladora SEC":
            self.withdraw()
            TelaControladora(master=self)

        elif label == "Computadores":
            self.withdraw()
            TelaComputadores(master=self)

        elif label == "Raspberry/Orangepi":
            self.withdraw()
            TelaRaspberryOrangePi(master=self)

        elif label == "Antena TAG":
            self.withdraw()
            TelaAntenas(master=self)

        elif label == "Leitor Biométrico":
            self.withdraw()
            TelaBiometrico(master=self)

        elif label == "Câmeras":
            self.withdraw()
            TelaCameras(master=self)

        elif label == "Roteador":
            self.withdraw()
            TelaRoteadores(master=self)

        elif label == "Relatórios":
            relatorio = RelatorioPDF()
            relatorio.gerar_pdf()

        elif label == "Outros":
            self.withdraw()
            TelaOutros(master=self)

        else:
            print(f"Abrir tela para: {label}")


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
