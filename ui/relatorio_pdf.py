import os
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class RelatorioPDF:
    def __init__(self):
        self.pasta_data = "data"

    def gerar_pdf(self):
        caminho_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile="Lista de IP.pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar relatório como..."
        )

        if not caminho_pdf:
            return

        # Lê os dados agrupados por tipo de dispositivo
        dados_por_tipo = {}
        for arquivo in os.listdir(self.pasta_data):
            if arquivo.endswith(".txt"):
                tipo = os.path.splitext(arquivo)[0].replace("_", " ").title()
                with open(os.path.join(self.pasta_data, arquivo), "r", encoding="utf-8") as f:
                    for linha in f:
                        if "|" in linha:
                            nome, ip = linha.strip().split("|")
                            dados_por_tipo.setdefault(tipo, []).append((nome.strip(), ip.strip()))

        if not dados_por_tipo:
            messagebox.showinfo("Relatório", "Nenhum dispositivo encontrado para gerar o relatório.")
            return

        try:
            pdf = canvas.Canvas(caminho_pdf, pagesize=A4)
            largura, altura = A4
            y = altura - 50

            # Título principal
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawCentredString(largura / 2, y, "Lista de IP")
            y -= 30

            for tipo, dispositivos in sorted(dados_por_tipo.items()):
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawCentredString(largura / 2, y, tipo)
                y -= 20

                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(50, y, "Nome do Dispositivo")
                pdf.drawString(300, y, "Endereço IP")
                y -= 15
                pdf.setStrokeColor(colors.grey)
                pdf.line(50, y, largura - 50, y)
                y -= 10

                pdf.setFont("Helvetica", 11)
                for nome, ip in dispositivos:
                    if y < 100:  # Nova página se necessário
                        pdf.showPage()
                        y = altura - 50
                        pdf.setFont("Helvetica-Bold", 14)
                        pdf.drawCentredString(largura / 2, y, tipo + " (continuação)")
                        y -= 30
                        pdf.setFont("Helvetica-Bold", 12)
                        pdf.drawString(50, y, "Nome do Dispositivo")
                        pdf.drawString(300, y, "Endereço IP")
                        y -= 15
                        pdf.setStrokeColor(colors.grey)
                        pdf.line(50, y, largura - 50, y)
                        y -= 10
                        pdf.setFont("Helvetica", 11)

                    pdf.drawString(50, y, nome)
                    pdf.drawString(300, y, ip)
                    y -= 18

                y -= 25  # Espaço entre seções

            pdf.save()
            messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{caminho_pdf}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o relatório:\n{str(e)}")
