from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from datetime import date
import speedtest
import matplotlib.pyplot as plt
from ping3 import ping, verbose_ping
import io

def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1024 / 1024  # Convertendo para megabits por segundo (Mbps)
    upload_speed = st.upload() / 1024 / 1024  # Convertendo para megabits por segundo (Mbps)
    return upload_speed, download_speed

def test_ping(host):
    # Testa a latência e perda de pacotes
    response_list = []
    for _ in range(5):
        response = verbose_ping(host, count=1, timeout=2)
        if response is not None:
            response_list.append(response)
    if response_list:
        avg_latency = sum(response_list) / len(response_list)
        loss_rate = (1 - len(response_list) / 5) * 100
    else:
        avg_latency = 0
        loss_rate = 100
    return avg_latency, loss_rate

def generate_reports(pairs):
    for source, destination in pairs:
        upload_speed, download_speed = test_speed()
        avg_latency, loss_rate = test_ping(destination)

        # Gráfico de velocidade
        plt.figure(figsize=(8, 6))
        plt.bar(["Upload", "Download"], [upload_speed, download_speed], color=['blue', 'green'])
        plt.ylabel('Velocidade (Mbps)')
        plt.title('Teste de Velocidade')
        plt.grid(True)
        buf_speed = io.BytesIO()
        plt.savefig(buf_speed, format='png')
        buf_speed.seek(0)

        # Gráfico de latência
        plt.figure(figsize=(8, 6))
        plt.plot([1], [avg_latency], marker='o')
        plt.ylabel('Latência Média (ms)')
        plt.title('Latência Média')
        plt.grid(True)
        buf_latency = io.BytesIO()
        plt.savefig(buf_latency, format='png')
        buf_latency.seek(0)

        # Gráfico de perda de pacotes
        plt.figure(figsize=(8, 6))
        plt.plot([1], [loss_rate], marker='o')
        plt.ylabel('Taxa de Perda de Pacotes (%)')
        plt.title('Taxa de Perda de Pacotes')
        plt.grid(True)
        buf_loss = io.BytesIO()
        plt.savefig(buf_loss, format='png')
        buf_loss.seek(0)

        # Gera o PDF
        doc = SimpleDocTemplate(f"relatorio_teste_voip_{source}_{destination}.pdf", pagesize=letter)
        elements = []

        # Título do relatório
        title_style = ParagraphStyle(name='Title', alignment=1, fontSize=15, spaceAfter=20)  
        title = Paragraph(f"<b>Relatório de Teste - {source} para {destination}</b>", title_style)
        elements.append(title)

        # Data do relatório
        today_date = date.today().strftime("%d/%m/%Y")
        date_style = ParagraphStyle(name='Date', alignment=1, fontSize=12, spaceAfter=10)  
        date_paragraph = Paragraph(f"Data: {today_date}", date_style)
        elements.append(date_paragraph)

        # Adiciona os gráficos ao PDF
        img_speed = Image(buf_speed)
        img_speed.drawWidth = 400
        img_speed.drawHeight = 300
        elements.append(img_speed)

        img_latency = Image(buf_latency)
        img_latency.drawWidth = 400
        img_latency.drawHeight = 300
        elements.append(img_latency)

        img_loss = Image(buf_loss)
        img_loss.drawWidth = 400
        img_loss.drawHeight = 300
        elements.append(img_loss)

        # Tabela de dados
        data = [
            ["Item", "Valor"],
            ["Origem", source],
            ["Destino", destination],
            ["Latência Média (ms)", f"{avg_latency:.2f}"],
            ["Taxa de Perda de Pacotes (%)", f"{loss_rate:.2f}"],
            ["Velocidade de Upload (Mbps)", f"{upload_speed:.2f}"],
            ["Velocidade de Download (Mbps)", f"{download_speed:.2f}"]
        ]
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'darkgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), 'lightgrey'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ])

        table = Table(data, colWidths=[doc.width/2.0]*2)
        table.setStyle(table_style)
        elements.append(Spacer(1, 20))
        elements.append(table)

        # Constrói o documento PDF
        doc.build(elements)

# Lista de pares de IPs a serem testados
pairs = [
    ("192.168.217.101", "192.168.217.102"),
    ("192.168.217.103", "192.168.217.104"),
    ("192.168.217.105", "192.168.217.106")
]

# Gera os relatórios para cada par de IPs
generate_reports(pairs)
