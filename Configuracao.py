from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FrmConfiguracaoSMTP(object):
    def setupUi(self, FrmConfiguracaoSMTP):
        FrmConfiguracaoSMTP.setObjectName("FrmConfiguracaoSMTP")
        FrmConfiguracaoSMTP.setFixedSize(551, 440)
        FrmConfiguracaoSMTP.setStyleSheet("background-color: rgb(189, 189, 189);")
        self.centralwidget = QtWidgets.QWidget(FrmConfiguracaoSMTP)
        self.centralwidget.setObjectName("centralwidget")
        self.EdtServidorSMTP = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtServidorSMTP.setGeometry(QtCore.QRect(106, 76, 261, 20))
        self.EdtServidorSMTP.setObjectName("EdtServidorSMTP")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(106, 58, 91, 16))
        self.label.setObjectName("label")
        self.EdtPorta = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtPorta.setGeometry(QtCore.QRect(376, 76, 61, 20))
        self.EdtPorta.setObjectName("EdtPorta")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(376, 59, 41, 16))
        self.label_2.setObjectName("label_2")
        self.RdSSL = QtWidgets.QRadioButton(self.centralwidget)
        self.RdSSL.setGeometry(QtCore.QRect(181, 112, 101, 17))
        self.RdSSL.setObjectName("RdSSL")
        self.RdSSL.setText("SSL")
        self.RdSSL.setAutoExclusive(False)
        self.RdTLS = QtWidgets.QRadioButton(self.centralwidget)
        self.RdTLS.setGeometry(QtCore.QRect(281, 112, 71, 17))
        self.RdTLS.setObjectName("RdTLS")
        self.RdTLS.setText("TLS")
        self.RdTLS.setAutoExclusive(False)
        self.EdtUsuarioAutenticacao = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtUsuarioAutenticacao.setGeometry(QtCore.QRect(178, 178, 171, 20))
        self.EdtUsuarioAutenticacao.setObjectName("EdtUsuarioAutenticacao")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(178, 160, 131, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(178, 204, 41, 16))
        self.label_4.setObjectName("label_4")
        self.EdtSenha = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtSenha.setGeometry(QtCore.QRect(178, 222, 171, 20))
        self.EdtSenha.setObjectName("EdtSenha")
        self.EdtSenha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.BtnSalvar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnSalvar.setGeometry(QtCore.QRect(273, 248, 75, 23))
        self.BtnSalvar.setObjectName("BtnSalvar")
        FrmConfiguracaoSMTP.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FrmConfiguracaoSMTP)
        self.statusbar.setObjectName("statusbar")
        FrmConfiguracaoSMTP.setStatusBar(self.statusbar)

        self.retranslateUi(FrmConfiguracaoSMTP)
        QtCore.QMetaObject.connectSlotsByName(FrmConfiguracaoSMTP)

        self.BtnSalvar.clicked.connect(self.salvar_dados)
        self.carregar_dados()

    def salvar_dados(self):
        import sqlite3
        from PyQt5.QtWidgets import QMessageBox

        servidor = self.EdtServidorSMTP.text()
        porta = self.EdtPorta.text()
        ssl = self.RdSSL.isChecked()
        tls = self.RdTLS.isChecked()
        usuario = self.EdtUsuarioAutenticacao.text()
        senha = self.EdtSenha.text()

        try:
            conn = sqlite3.connect("MAILSENDTEST.db")
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM CONFIGURACAOI")
            existe = cursor.fetchone()[0] > 0

            if existe:
                cursor.execute("""
                    UPDATE CONFIGURACAOI
                    SET ServidorSMTP = ?, Porta = ?, SSL = ?, TLS = ?, UsuarioAutenticacao = ?, Senha = ?
                """, (servidor, porta, ssl, tls, usuario, senha))
            else:
                cursor.execute("""
                    INSERT INTO CONFIGURACAOI (ServidorSMTP, Porta, SSL, TLS, UsuarioAutenticacao, Senha)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (servidor, porta, ssl, tls, usuario, senha))

            conn.commit()
            conn.close()

            QMessageBox.information(None, "Sucesso", "Configuração salva com sucesso!")
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao salvar: {e}")

    def carregar_dados(self):
        import sqlite3
        from PyQt5.QtWidgets import QMessageBox

        try:
            conn = sqlite3.connect("MAILSENDTEST.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT ServidorSMTP, Porta, SSL, TLS, UsuarioAutenticacao, Senha FROM CONFIGURACAOI LIMIT 1")
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                servidor, porta, ssl, tls, usuario, senha = resultado
                self.EdtServidorSMTP.setText(servidor)
                self.EdtPorta.setText(str(porta))
                self.RdSSL.setChecked(bool(ssl))
                self.RdTLS.setChecked(bool(tls))
                self.EdtUsuarioAutenticacao.setText(usuario)
                self.EdtSenha.setText(senha)

        except Exception as e:
            QMessageBox.warning(None, "Aviso", f"Erro ao carregar dados: {e}")

    def retranslateUi(self, FrmConfiguracaoSMTP):
        _translate = QtCore.QCoreApplication.translate
        FrmConfiguracaoSMTP.setWindowTitle(_translate("FrmConfiguracaoSMTP", "Configuração SMTP"))
        self.label.setText(_translate("FrmConfiguracaoSMTP", "<html><head/><body><p><span style=\" font-weight:600;\">Servidor SMTP</span></p></body></html>"))
        self.label_2.setText(_translate("FrmConfiguracaoSMTP", "<html><head/><body><p><span style=\" font-weight:600;\">Porta</span></p></body></html>"))
        self.RdSSL.setText(_translate("FrmConfiguracaoSMTP", "Servidor SSL"))
        self.RdTLS.setText(_translate("FrmConfiguracaoSMTP", "TLS 1.2"))
        self.label_3.setText(_translate("FrmConfiguracaoSMTP", "<html><head/><body><p><span style=\" font-weight:600;\">Usuário Autenticação</span></p></body></html>"))
        self.label_4.setText(_translate("FrmConfiguracaoSMTP", "<html><head/><body><p><span style=\" font-weight:600;\">Senha</span></p></body></html>"))
        self.BtnSalvar.setText(_translate("FrmConfiguracaoSMTP", "Salvar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrmConfiguracaoSMTP = QtWidgets.QMainWindow()
    ui = Ui_FrmConfiguracaoSMTP()
    ui.setupUi(FrmConfiguracaoSMTP)
    FrmConfiguracaoSMTP.show()
    sys.exit(app.exec_())
