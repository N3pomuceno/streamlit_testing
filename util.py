import email
import smtplib
import io
import os
# import logging
# from dotenv import load_dotenv

# load_dotenv()

# logging.basicConfig(level=logging.DEBUG)

# HOST = 'smtp.gmail.com'
# PORT = 587
# USERNAME = os.getenv('APP_SECRET_UFF_MAIL')
# PASSWORD = os.getenv('APP_SECRET_UFF_PASSWORD')
# RECEIVER = os.getenv('APP_SECRET_UFF_RECEIVER')


def dataframe_para_csv(df):
    """Converte um DataFrame em CSV na memória (sem salvar em disco)."""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    return csv_buffer.getvalue()


def check_login(usn, pwd, host, port):
    with smtplib.SMTP(host, port) as smtp_cli:
        smtp_cli.set_debuglevel(10)
        smtp_cli.starttls()
        try:
            smtp_cli.login(usn, pwd)
            return True
        except Exception as e:
            print("Error: ", e)
            return False


def send_email(usn, pwd, sbj, to, body, csv_content, filename, host, port):
    msg = email.message.EmailMessage()
    msg['subject'] = sbj
    msg['From'] = usn
    msg['To'] = to
    msg.set_content(body)

    # Anexar o CSV gerado em memória
    msg.add_attachment(csv_content.encode('utf-8'), maintype='text', subtype='csv', filename=filename)  

    with smtplib.SMTP(host, port) as smtp_cli:
        smtp_cli.set_debuglevel(10)
        smtp_cli.starttls()
        smtp_cli.login(usn, pwd)
        smtp_cli.ehlo()
        smtp_cli.send_message(msg, usn, to.split(','))


# print(check_login(USERNAME, PASSWORD))
# print(send_email(USERNAME, PASSWORD, 'Teste de dados', USERNAME, 'Dados_Teste', None))
