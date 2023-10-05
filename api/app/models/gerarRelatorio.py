import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.controllers.mensagens import erro_msg, normal_msg
import os

class RelatorioDeProgresso():
    def __init__(self, aluno, turma, email):
        self.aluno = aluno
        self.turma = turma
        self.email = email
        self.nome_do_arquivo = email  # O nome do arquivo será o email do usuário
        self.rota_do_arquivo = os.path.join('api', 'app', 'static', 'reports', self.nome_do_arquivo)

    def gerar_relatorio(self, data):
        pdf_file = f"{self.rota_do_arquivo}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)

        # Carregue a imagem de fundo
        imagem_de_fundo = "api\\app\\static\\reports\\ARduck.png"
        c.drawImage(imagem_de_fundo, 400, 600, 100, 100)

        # Título do relatório
        c.setFont("Helvetica", 16)
        c.drawString(100, 750, f"Relatório de {self.aluno} da turma {self.turma}")

        y = 700  # Posição vertical inicial para os dados

        for colecao in data['colecoes']:
            nome_colecao = colecao['nome']
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, y, f"Coleção: {nome_colecao}")
            y -= 20

            for trilha in colecao['trilhas']:
                nome_trilha = trilha['nome']
                c.setFont("Helvetica", 12)
                c.drawString(120, y, f"Trilha: {nome_trilha}")
                y -= 15

                teoria_status = trilha.get('teoria', 'Inconcluído')
                c.setFont("Helvetica", 10)
                c.drawString(140, y, f"Teoria: {teoria_status}")
                y -= 12

                atividade_pratica_status = trilha.get('atividade_pratica', 'Inconcluído')
                c.drawString(140, y, f"Atividade Prática: {atividade_pratica_status}")
                y -= 12

                quizzes = trilha.get('quiz', [])
                if quizzes:
                    c.setFont("Helvetica", 10)
                    c.drawString(140, y, "Quiz:")
                    y -= 10
                    quizzes_str = ', '.join(quiz if quiz is not None else '' for quiz in quizzes)
                    c.drawString(160, y, quizzes_str)
                    y -= 12

                y -= 20  # Espaço entre trilhas

        c.save()
        print(f"Relatório salvo em {pdf_file}")

    def enviar_email_com_anexo(self, destinatario_email):

        smtp_server = 'smtp.outlook.com'  # Insira o servidor SMTP do seu provedor de email
        smtp_port = 587  # Porta SMTP padrão para TLS
        smtp_username = 'otavio.zordan@outlook.com'  # Seu endereço de email
        smtp_password = 'Marocas2'  # Sua senha de email

        try:
            assunto = f'Relatório de progresso do usuário {self.aluno}'

            mensagem = f"""
            Prezado Professor,

            Espero que este email encontre você bem. Estou enviando o relatório de progresso do aluno {self.aluno} da turma {self.turma}, que demonstra o desempenho dele nas trilhas de aprendizado.

            O relatório inclui informações detalhadas sobre o progresso do aluno em cada coleção e trilha, incluindo o status da teoria, atividade prática e resultados dos quizzes.

            Este relatório pode ser uma ferramenta valiosa para avaliar o progresso do aluno e identificar áreas que podem precisar de mais atenção ou apoio.

            Se você tiver alguma dúvida ou precisar de mais informações, não hesite em entrar em contato.

            Atenciosamente,
            ARduck,
            Gerador de Relatórios Automaticos.
            """

            # Crie a mensagem de email
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = destinatario_email
            msg['Subject'] = assunto

            # Corpo do email
            msg.attach(MIMEText(mensagem, 'plain'))

            # Anexe o PDF ao email
            with open(f"{self.rota_do_arquivo}.pdf", 'rb') as attachment:
                pdf_part = MIMEApplication(attachment.read(), _subtype="pdf")
                pdf_part.add_header('content-disposition', 'attachment', filename=f"{self.rota_do_arquivo}.pdf")
                msg.attach(pdf_part)

            # Envie o email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, destinatario_email, msg.as_string())
            normal_msg(f"E-mail enviado para {destinatario_email}")

        except Exception as e:
            erro_msg("Erro ao envair e-mail", e)

        finally:
            server.quit()


#relatorio = RelatorioDeProgresso(aluno="Otávio", turma="A", email="otavio@example.com")
#relatorio.gerar_relatorio(data=exemplo)
#relatorio.enviar_email_com_anexo(destinatario_email="professor@example.com")