from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from datetime import date
import iperf3
import matplotlib.pyplot as plt
from ping3 import ping, verbose_ping
import io

def test_speed(source, destination):
    try:
        speeds = []
        client = iperf3.Client()
        client.server_hostname = destination
        for _ in range(5):
            result = client.run()
            if result.error:
                raise Exception(result.error)
            speeds.append(result.sent_Mbps)
        return speeds
    except Exception as e:
        print(f"Erro ao executar o teste de velocidade entre {source} e {destination}: {e}")
        return None

def test_latency(host):
    try:
        response_list = []
        for _ in range(5):
            response = verbose_ping(host, count=1, timeout=2)
            if response is not None:
                response_list.append(response)
        if response_list:
            avg_latency = sum(response_list) / len(response_list)
        else:
            avg_latency = None
        return avg_latency
    except Exception as e:
        print(f"Erro ao executar o teste de latência em {host}: {e}")
        return None

def generate_reports(pairs):
    for source, destination in pairs:
        speeds = test_speed(source, destination)
        avg_latency = test_latency(destination)

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

        # Teste de velocidade
        if speeds is not None:
            # Gráfico de velocidade
            plt.figure(figsize=(8, 6))
            plt.plot(range(1, 6), speeds, marker='o')
            plt.xlabel('Teste')
            plt.ylabel('Velocidade (Mbps)')
            plt.title('Teste de Velocidade')
            plt.grid(True)
            buf_speed = io.BytesIO()
            plt.savefig(buf_speed, format='png')
            buf_speed.seek(0)
            img_speed = Image(buf_speed)
            img_speed.drawWidth = 400
            img_speed.drawHeight = 300
            elements.append(img_speed)

            # Tabela de dados
            data = [
                ["Item", "Valor"],
                ["Origem", source],
                ["Destino", destination],
                ["Latência Média (ms)", f"{avg_latency:.2f}" if avg_latency is not None else "Erro ao obter latência"]
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
        else:
            # Mensagem de erro
            error_message = Paragraph("Erro ao executar o teste de velocidade.", ParagraphStyle(name='ErrorMessage', alignment=1, textColor='red'))
            elements.append(error_message)

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