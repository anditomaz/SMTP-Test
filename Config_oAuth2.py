from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FrmConfigoAuth2(object):
    def setupUi(self, FrmConfigoAuth2):
        FrmConfigoAuth2.setObjectName("FrmConfigoAuth2")
        FrmConfigoAuth2.setFixedSize(552, 441)
        FrmConfigoAuth2.setStyleSheet("background-color: rgb(189, 189, 189);")
        self.centralwidget = QtWidgets.QWidget(FrmConfigoAuth2)
        self.centralwidget.setObjectName("centralwidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(170, 35, 221, 17))
        self.radioButton.setObjectName("radioButton")
        self.EdtDominio = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtDominio.setGeometry(QtCore.QRect(142, 106, 281, 20))
        self.EdtDominio.setObjectName("EdtDominio")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(142, 89, 51, 16))
        self.label.setObjectName("label")
        self.EdtClientId = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtClientId.setGeometry(QtCore.QRect(102, 158, 371, 20))
        self.EdtClientId.setObjectName("EdtClientId")
        self.EdtClientId.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(102, 141, 51, 16))
        self.label_2.setObjectName("label_2")
        self.EdtTenantId = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtTenantId.setGeometry(QtCore.QRect(102, 200, 371, 20))
        self.EdtTenantId.setObjectName("EdtTenantId")
        self.EdtTenantId.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(102, 183, 61, 16))
        self.label_3.setObjectName("label_3")
        self.EdtRedirectUrl = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtRedirectUrl.setGeometry(QtCore.QRect(103, 242, 371, 20))
        self.EdtRedirectUrl.setObjectName("EdtRedirectUrl")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(103, 225, 81, 16))
        self.label_4.setObjectName("label_4")
        self.BtnSalvar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnSalvar.setGeometry(QtCore.QRect(399, 269, 75, 23))
        self.BtnSalvar.setObjectName("BtnSalvar")
        FrmConfigoAuth2.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FrmConfigoAuth2)
        self.statusbar.setObjectName("statusbar")
        FrmConfigoAuth2.setStatusBar(self.statusbar)

        self.retranslateUi(FrmConfigoAuth2)
        QtCore.QMetaObject.connectSlotsByName(FrmConfigoAuth2)

        self.BtnSalvar.clicked.connect(self.salvar_dados)
        self.radioButton.toggled.connect(self.atualizar_estado_campos)

        self.carregar_dados()
        self.atualizar_estado_campos()

    def atualizar_estado_campos(self):
        ativado = self.radioButton.isChecked()
        self.EdtDominio.setEnabled(ativado)
        self.EdtClientId.setEnabled(ativado)
        self.EdtTenantId.setEnabled(ativado)
        self.EdtRedirectUrl.setEnabled(ativado)
        self.BtnSalvar.setEnabled(ativado)

    def salvar_dados(self):
        import sqlite3
        from PyQt5.QtWidgets import QMessageBox

        ativado = int(self.radioButton.isChecked())
        dominio = self.EdtDominio.text()
        client_id = self.EdtClientId.text()
        tenant_id = self.EdtTenantId.text()
        redirect_url = self.EdtRedirectUrl.text()

        try:
            conn = sqlite3.connect("MAILSENDTEST.db")
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM CONFIG_OAUTH2")
            existe = cursor.fetchone()[0] > 0

            if existe:
                cursor.execute("""
                    UPDATE CONFIG_OAUTH2
                    SET ATIVADO = ?, Dominio = ?, ClientId = ?, TenantId = ?, RedirectUrl = ?
                """, (ativado, dominio, client_id, tenant_id, redirect_url))
            else:
                cursor.execute("""
                    INSERT INTO CONFIG_OAUTH2 (ATIVADO, Dominio, ClientId, TenantId, RedirectUrl)
                    VALUES (?, ?, ?, ?, ?)
                """, (ativado, dominio, client_id, tenant_id, redirect_url))

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

            cursor.execute("SELECT ATIVADO, Dominio, ClientId, TenantId, RedirectUrl FROM CONFIG_OAUTH2 LIMIT 1")
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                ativado, dominio, client_id, tenant_id, redirect_url = resultado
                self.radioButton.setChecked(bool(ativado))
                self.EdtDominio.setText(dominio)
                self.EdtClientId.setText(client_id)
                self.EdtTenantId.setText(tenant_id)
                self.EdtRedirectUrl.setText(redirect_url)
        except Exception as e:
            QMessageBox.warning(None, "Aviso", f"Erro ao carregar dados: {e}")

    def retranslateUi(self, FrmConfigoAuth2):
        _translate = QtCore.QCoreApplication.translate
        FrmConfigoAuth2.setWindowTitle(_translate("FrmConfigoAuth2", "Configurar oAuth2"))
        self.radioButton.setText(_translate("FrmConfigoAuth2", "Ativar Autenticação oAuth2 - Microsoft"))
        self.label.setText(_translate("FrmConfigoAuth2", "<html><head/><body><p><span style=\" font-weight:600;\">Domínio</span></p></body></html>"))
        self.label_2.setText(_translate("FrmConfigoAuth2", "<html><head/><body><p><span style=\" font-weight:600;\">ClientId</span></p></body></html>"))
        self.label_3.setText(_translate("FrmConfigoAuth2", "<html><head/><body><p><span style=\" font-weight:600;\">TenantId</span></p></body></html>"))
        self.label_4.setText(_translate("FrmConfigoAuth2", "<html><head/><body><p><span style=\" font-weight:600;\">Redirect Url</span></p></body></html>"))
        self.BtnSalvar.setText(_translate("FrmConfigoAuth2", "Salvar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FrmConfigoAuth2 = QtWidgets.QMainWindow()
    ui = Ui_FrmConfigoAuth2()
    ui.setupUi(FrmConfigoAuth2)
    FrmConfigoAuth2.show()
    sys.exit(app.exec_())
