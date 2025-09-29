import customtkinter as ctk
from tkinter import messagebox
import webbrowser
import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto para uso com PyInstaller ou em desenvolvimento local."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TelaOutros(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Outros Dispositivos")
        self.attributes("-fullscreen", True)
        self.resizable(True, True)

        self.master = master
        self.outros_path = resource_path(os.path.join("data", "outros.txt"))
        os.makedirs(resource_path("data"), exist_ok=True)
        if not os.path.exists(self.outros_path):
            open(self.outros_path, "w").close()

        self.create_widgets()
        self.load_outros()

    def create_widgets(self):
        top_frame = ctk.CTkFrame(self, height=60)
        top_frame.pack(fill="x", side="top")

        btn_voltar = ctk.CTkButton(top_frame, text="← Voltar", width=100, command=self.voltar)
        btn_voltar.pack(side="left", padx=20, pady=10)

        titulo = ctk.CTkLabel(top_frame, text="Lista de Outros Dispositivos", font=("Arial", 24, "bold"))
        titulo.pack(pady=10, expand=True)

        btn_fechar = ctk.CTkButton(top_frame, text="X", width=50, fg_color="#FF6B6B",
                                   hover_color="#FF3B3B", command=self.quit)
        btn_fechar.pack(side="right", padx=20, pady=10)

        self.frame_lista = ctk.CTkScrollableFrame(self)
        self.frame_lista.pack(expand=True, fill="both", padx=40, pady=20)

        self.btn_add = ctk.CTkButton(self, text="Adicionar Dispositivo", height=40,
                                     command=self.adicionar_outro)
        self.btn_add.pack(pady=20)

    def load_outros(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        with open(self.outros_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        for line in lines:
            if "|" not in line:
                continue
            nome, ip = line.split("|")
            self.add_outro_widget(nome, ip)

    def add_outro_widget(self, nome, ip):
        container = ctk.CTkFrame(self.frame_lista)
        container.pack(fill="x", pady=5, padx=10)

        lbl_nome = ctk.CTkLabel(container, text=nome, width=200, anchor="w")
        lbl_nome.pack(side="left", padx=10)

        lbl_ip = ctk.CTkButton(container, text=ip, text_color="blue", fg_color="transparent",
                               hover=False, width=140, command=lambda: webbrowser.open(f"http://{ip}"))
        lbl_ip.pack(side="left", padx=10)

        btn_edit = ctk.CTkButton(container, text="Editar", width=80,
                                 fg_color="#4CAF50", hover_color="#45A049",
                                 command=lambda: self.editar_outro(nome, ip))
        btn_edit.pack(side="right", padx=5)

        btn_delete = ctk.CTkButton(container, text="Excluir", width=80,
                                   fg_color="#FF6B6B", hover_color="#FF3B3B",
                                   command=lambda: self.excluir_outro(nome, ip))
        btn_delete.pack(side="right", padx=5)

    def adicionar_outro(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Novo Dispositivo")
        popup.geometry("300x240")
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Nome:").pack(pady=5)
        entry_nome = ctk.CTkEntry(popup)
        entry_nome.pack(pady=5)

        ctk.CTkLabel(popup, text="IP:").pack(pady=5)
        entry_ip = ctk.CTkEntry(popup)
        entry_ip.pack(pady=5)

        def salvar():
            nome = entry_nome.get().strip()
            ip = entry_ip.get().strip()
            if nome and ip:
                with open(self.outros_path, "a") as f:
                    f.write(f"{nome}|{ip}\n")
                popup.destroy()
                self.load_outros()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        ctk.CTkButton(popup, text="Salvar", command=salvar).pack(pady=10)

    def editar_outro(self, nome_antigo, ip_antigo):
        popup = ctk.CTkToplevel(self)
        popup.title("Editar Dispositivo")
        popup.geometry("300x240")
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Nome:").pack(pady=5)
        entry_nome = ctk.CTkEntry(popup)
        entry_nome.insert(0, nome_antigo)
        entry_nome.pack(pady=5)

        ctk.CTkLabel(popup, text="IP:").pack(pady=5)
        entry_ip = ctk.CTkEntry(popup)
        entry_ip.insert(0, ip_antigo)
        entry_ip.pack(pady=5)

        def salvar():
            novo_nome = entry_nome.get().strip()
            novo_ip = entry_ip.get().strip()
            if novo_nome and novo_ip:
                with open(self.outros_path, "r") as f:
                    linhas = f.readlines()
                with open(self.outros_path, "w") as f:
                    for linha in linhas:
                        if linha.strip() == f"{nome_antigo}|{ip_antigo}":
                            f.write(f"{novo_nome}|{novo_ip}\n")
                        else:
                            f.write(linha)
                popup.destroy()
                self.load_outros()
            else:
                messagebox.showwarning("Atenção", "Preencha todos os campos.")

        ctk.CTkButton(popup, text="Salvar", command=salvar, height=40).pack(pady=10, fill="x", padx=20)

    def excluir_outro(self, nome, ip):
        resposta = messagebox.askyesno("Excluir", f"Excluir dispositivo '{nome}'?")
        if not resposta:
            return
        with open(self.outros_path, "r") as f:
            linhas = f.readlines()
        with open(self.outros_path, "w") as f:
            for linha in linhas:
                if linha.strip() != f"{nome}|{ip}":
                    f.write(linha)
        self.load_outros()

    def voltar(self):
        self.destroy()
        if self.master:
            self.master.deiconify()
