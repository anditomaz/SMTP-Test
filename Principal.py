from PyQt5 import QtCore, QtGui, QtWidgets
from Configuracao import Ui_FrmConfiguracaoSMTP
from Config_oAuth2 import Ui_FrmConfigoAuth2
import sqlite3
from PyQt5.QtWidgets import QMessageBox
import smtplib
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid
import os
import requests
import sqlite3
import sys


# ===============================================================================
# ======== Valida se a base de dados já existe; caso contrário, cria ============
# ====== Verifica se está rodando através do script/projeto ou executável =======
# ===============================================================================

if getattr(sys, 'frozen', False):
    # Quando rodando no executável (PyInstaller)
    base_dir = os.path.dirname(sys.executable)
else:
    # Quando rodando no script Python normal
    base_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_dir, "MAILSENDTEST.db")

if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CONFIGURACAOI (
        ServidorSMTP TEXT,
        Porta INTEGER,
        SSL BOOLEAN,
        TLS BOOLEAN,
        UsuarioAutenticacao TEXT,
        Senha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CONFIG_OAUTH2 (
        ATIVADO BOOLEAN,
        Dominio TEXT,
        ClientId TEXT,
        TenantId TEXT,
        RedirectUrl TEXT
    )
    """)

    conn.commit()
    conn.close()

# =======================================================================
# =======================================================================


class MailKitPython:
    def __init__(self):
        self.server = None
        self.port = 587
        self.use_ssl = False
        self.use_tls12 = False
        self.username = None
        self.password = None
        self.message = EmailMessage()
        self._request_read_receipt = False
        self.msg_id = make_msgid()

    @property
    def RequestReadReceipt(self):
        return self._request_read_receipt

    @RequestReadReceipt.setter
    def RequestReadReceipt(self, value):
        self._request_read_receipt = value

    @property
    def GetMessageId(self):
        return self.msg_id

    def ServerInfo(self, host, port, is_ssl, is_tls12=False):
        self.server = host
        self.port = port
        self.use_ssl = is_ssl
        self.use_tls12 = is_tls12

    def LoginInfo(self, username, password):
        self.username = username
        self.password = password

    def CreateMail(self, from_addr, to_addr, subject, priority):
        self.message['From'] = from_addr
        self.message['To'] = to_addr
        self.message['Subject'] = subject
        self.message['X-Priority'] = str(priority)
        self.message['Message-ID'] = self.msg_id

    def AddCC(self, cc):
        self.message['Cc'] = cc

    def AddBCC(self, bcc):
        self.message['Bcc'] = bcc

    def AddReplyTo(self, reply_to):
        self.message['Reply-To'] = reply_to

    def AddBody(self, is_html, body_text):
        subtype = "html" if is_html else "plain"
        self.message.set_content(body_text, subtype=subtype)

    def AddAlternativeBody(self, body_text):
        self.message.add_alternative(body_text, subtype="html")

    def AddAttachment(self, file_path):
        ctype, encoding = mimetypes.guess_type(file_path)
        maintype, subtype = ctype.split('/', 1) if ctype else ('application', 'octet-stream')

        with open(file_path, 'rb') as f:
            self.message.add_attachment(f.read(),
                                        maintype=maintype,
                                        subtype=subtype,
                                        filename=os.path.basename(file_path))

    def AddLinkedResource(self, file_path):
        cid = make_msgid()
        with open(file_path, 'rb') as f:
            self.message.get_payload()[0].add_related(f.read(), maintype='image', subtype='png', cid=cid)
        return cid

    def Send(self):
        try:
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.server, self.port)
            else:
                server = smtplib.SMTP(self.server, self.port)
                if self.use_tls12:
                    server.starttls()

            server.login(self.username, self.password)
            server.send_message(self.message)
            server.quit()
            return self.msg_id
        except Exception as e:
            raise Exception(f"Erro ao enviar e-mail: {e}")

class Ui_FrmTesteEmail(object):
    def setupUi(self, FrmTesteEmail):
        FrmTesteEmail.setObjectName("FrmTesteEmail")
        FrmTesteEmail.setFixedSize(758, 671)
        FrmTesteEmail.setStyleSheet("background-color: rgb(189, 189, 189);")
        self.centralwidget = QtWidgets.QWidget(FrmTesteEmail)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(15, 1, 731, 621))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(373, 9, 41, 16))
        self.label_3.setObjectName("label_3")
        self.EdtFrom = QtWidgets.QLineEdit(self.groupBox)
        self.EdtFrom.setGeometry(QtCore.QRect(33, 28, 331, 20))
        self.EdtFrom.setObjectName("EdtFrom")
        self.EdtTo = QtWidgets.QLineEdit(self.groupBox)
        self.EdtTo.setGeometry(QtCore.QRect(33, 68, 331, 20))
        self.EdtTo.setObjectName("EdtTo")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(33, 52, 31, 16))
        self.label_2.setObjectName("label_2")
        self.EdtCopia = QtWidgets.QTextEdit(self.groupBox)
        self.EdtCopia.setGeometry(QtCore.QRect(373, 27, 331, 61))
        self.EdtCopia.setObjectName("EdtCopia")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(33, 11, 31, 16))
        self.label.setObjectName("label")
        self.EdtAssunto = QtWidgets.QLineEdit(self.groupBox)
        self.EdtAssunto.setGeometry(QtCore.QRect(32, 114, 671, 20))
        self.EdtAssunto.setObjectName("EdtAssunto")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(32, 96, 51, 16))
        self.label_4.setObjectName("label_4")
        self.EdtMensagem = QtWidgets.QTextEdit(self.groupBox)
        self.EdtMensagem.setGeometry(QtCore.QRect(30, 159, 671, 171))
        self.EdtMensagem.setObjectName("EdtMensagem")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(30, 141, 71, 16))
        self.label_5.setObjectName("label_5")
        self.EdtEnviar = QtWidgets.QPushButton(self.groupBox)
        self.EdtEnviar.setGeometry(QtCore.QRect(30, 338, 671, 23))
        self.EdtEnviar.setStyleSheet("background-color: rgb(132, 132, 132);")
        self.EdtEnviar.setObjectName("EdtEnviar")
        self.EdtResultado = QtWidgets.QPlainTextEdit(self.groupBox)
        self.EdtResultado.setGeometry(QtCore.QRect(30, 370, 671, 241))
        self.EdtResultado.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255);")
        self.EdtResultado.setObjectName("EdtResultado")
        FrmTesteEmail.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FrmTesteEmail)
        self.statusbar.setObjectName("statusbar")
        FrmTesteEmail.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(FrmTesteEmail)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 758, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuConfigura_es = QtWidgets.QMenu(self.menuBar)
        self.menuConfigura_es.setObjectName("menuConfigura_es")
        FrmTesteEmail.setMenuBar(self.menuBar)
        self.actionAutentica_o_oAuth2 = QtWidgets.QAction(FrmTesteEmail)
        self.actionAutentica_o_oAuth2.setObjectName("actionAutentica_o_oAuth2")
        self.actionConfigura_es = QtWidgets.QAction(FrmTesteEmail)
        self.actionConfigura_es.setObjectName("actionConfigura_es")
        self.actionConfigura_es_SMTP = QtWidgets.QAction(FrmTesteEmail)
        self.actionConfigura_es_SMTP.setObjectName("actionConfigura_es_SMTP")
        self.menuConfigura_es.addAction(self.actionAutentica_o_oAuth2)
        self.menuConfigura_es.addSeparator()
        self.menuConfigura_es.addAction(self.actionConfigura_es_SMTP)
        self.menuBar.addAction(self.menuConfigura_es.menuAction())

        self.retranslateUi(FrmTesteEmail)
        QtCore.QMetaObject.connectSlotsByName(FrmTesteEmail)

    def retranslateUi(self, FrmTesteEmail):
        _translate = QtCore.QCoreApplication.translate
        FrmTesteEmail.setWindowTitle(_translate("FrmTesteEmail", "Teste E-mail"))
        self.label_3.setText(_translate("FrmTesteEmail",
                                        "<html><head/><body><p><span style=\" font-weight:600;\">Cópia</span></p></body></html>"))
        self.label_2.setText(_translate("FrmTesteEmail",
                                        "<html><head/><body><p><span style=\" font-weight:600;\">Para</span></p></body></html>"))
        self.label.setText(_translate("FrmTesteEmail",
                                      "<html><head/><body><p><span style=\" font-weight:600;\">De</span></p></body></html>"))
        self.label_4.setText(_translate("FrmTesteEmail",
                                        "<html><head/><body><p><span style=\" font-weight:600;\">Assunto</span></p></body></html>"))
        self.label_5.setText(_translate("FrmTesteEmail",
                                        "<html><head/><body><p><span style=\" font-weight:600;\">Mensagem</span></p></body></html>"))
        self.EdtEnviar.setText(_translate("FrmTesteEmail", "Enviar"))
        self.menuConfigura_es.setTitle(_translate("FrmTesteEmail", "Configurações"))
        self.actionAutentica_o_oAuth2.setText(_translate("FrmTesteEmail", "Configurações - SMTP"))
        self.actionConfigura_es.setText(_translate("FrmTesteEmail", "Configurações"))
        self.actionConfigura_es_SMTP.setText(_translate("FrmTesteEmail", "Autenticação Microsoft oAuth2"))


class FrmPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FrmTesteEmail()
        self.ui.setupUi(self)

        self.ui.actionAutentica_o_oAuth2.triggered.connect(self.abrir_configuracoes)
        self.ui.actionConfigura_es_SMTP.triggered.connect(self.abrir_configuracaoauth2)
        self.ui.EdtEnviar.clicked.connect(self.enviar_email)

    def abrir_configuracoes(self):
        self.janela_config = QtWidgets.QMainWindow()
        self.ui_config = Ui_FrmConfiguracaoSMTP()
        self.ui_config.setupUi(self.janela_config)
        self.janela_config.show()

    def abrir_configuracaoauth2(self):
        self.janela_config = QtWidgets.QMainWindow()
        self.ui_config = Ui_FrmConfigoAuth2()
        self.ui_config.setupUi(self.janela_config)
        self.janela_config.show()

    def enviar_email(self):
        try:
            conn = sqlite3.connect("MAILSENDTEST.db")
            cursor = conn.cursor()

            # Verifica se OAuth2 está ativado
            cursor.execute("SELECT ATIVADO, TenantId, ClientId FROM CONFIG_OAUTH2 LIMIT 1")
            resultado_oauth = cursor.fetchone()
            ativado = resultado_oauth[0] if resultado_oauth else 0
            tenant_id = resultado_oauth[1] if resultado_oauth else None
            client_id = resultado_oauth[2] if resultado_oauth else None

            # Pega as configurações SMTP
            cursor.execute(
                "SELECT ServidorSMTP, Porta, SSL, TLS, UsuarioAutenticacao, Senha FROM CONFIGURACAOI LIMIT 1")
            resultado_smtp = cursor.fetchone()

            if not resultado_smtp:
                QMessageBox.warning(self, "Erro", "Configurações SMTP não encontradas.")
                return

            servidor, porta, ssl, tls, usuario, senha = resultado_smtp
            conn.close()

            from_addr = self.ui.EdtFrom.text()
            to_addr = self.ui.EdtTo.text()
            assunto = self.ui.EdtAssunto.text()
            corpo = self.ui.EdtMensagem.toPlainText()
            copia = self.ui.EdtCopia.toPlainText()

            if ativado:  # Se OAuth2 está ativado
                import requests
                import base64
                import smtplib
                from email.mime.text import MIMEText

                if not tenant_id or not client_id:
                    QMessageBox.critical(self, "Erro", "Tenant ID ou Client ID não configurados.")
                    return

                token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
                data = {
                    "client_id": client_id,
                    "scope": "https://outlook.office365.com/.default",
                    "username": usuario,
                    "password": senha,
                    "grant_type": "password",
                }

                self.ui.EdtResultado.appendPlainText("Solicitando token OAuth2...")

                response = requests.post(token_url, data=data)

                if response.status_code != 200:
                    self.ui.EdtResultado.appendPlainText(
                        f"Erro ao obter token: {response.status_code} - {response.text}")
                    return

                access_token = response.json()["access_token"]

                def generate_oauth2_string(email, token):
                    auth_string = f"user={email}\x01auth=Bearer {token}\x01\x01"
                    return base64.b64encode(auth_string.encode()).decode()

                msg = MIMEText(corpo)
                msg["Subject"] = assunto
                msg["From"] = from_addr
                msg["To"] = to_addr
                if copia.strip():
                    msg["Cc"] = copia.strip()

                auth_string = generate_oauth2_string(usuario, access_token)

                server = smtplib.SMTP(servidor, int(porta))
                server.starttls()
                server.docmd("AUTH", "XOAUTH2 " + auth_string)
                server.sendmail(from_addr, [to_addr] + ([copia.strip()] if copia.strip() else []), msg.as_string())
                server.quit()

                self.ui.EdtResultado.appendPlainText("E-mail enviado com sucesso via OAuth2.")

            else:  # SMTP tradicional
                mail = MailKitPython()
                mail.ServerInfo(host=servidor, port=int(porta), is_ssl=bool(ssl), is_tls12=bool(tls))
                mail.LoginInfo(username=usuario, password=senha)
                mail.CreateMail(from_addr=from_addr, to_addr=to_addr, subject=assunto, priority=1)

                if copia.strip():
                    mail.AddCC(copia.strip())

                mail.AddBody(is_html=False, body_text=corpo)

                msg_id = mail.Send()
                self.ui.EdtResultado.appendPlainText(f"E-mail enviado com sucesso. Message-ID: {msg_id}")

        except Exception as e:
            self.ui.EdtResultado.appendPlainText(f"Erro ao enviar e-mail: {e}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    janela = FrmPrincipal()
    janela.show()
    sys.exit(app.exec_())
