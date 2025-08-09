# Teste de Envio de E-mail com PyQt5

Este projeto é uma aplicação desktop desenvolvida em Python com PyQt5 para envio de e-mails, suportando autenticação via SMTP tradicional e Microsoft OAuth2.

---

## Funcionalidades

- Interface gráfica simples para enviar e-mails.
- Configuração de servidor SMTP com suporte a SSL/TLS.
- Envio de e-mails com destinatário, cópia, assunto e corpo da mensagem.
- Suporte a envio via autenticação tradicional (usuário e senha).
- Suporte a envio via autenticação OAuth2 (Microsoft Office 365).
- Armazenamento local das configurações SMTP e OAuth2 em banco SQLite (`MAILSENDTEST.db`).
- Suporte para múltiplas janelas de configuração (SMTP e OAuth2).
- Exibição de resultado (sucesso ou erro) no painel da interface.
- Geração automática de `Message-ID` para cada e-mail enviado.

---

## Estrutura do Projeto

- `MAILSENDTEST.db`: Banco SQLite local que armazena as configurações SMTP e OAuth2.
- `Ui_FrmTesteEmail`: Interface principal para envio de e-mails.
- `MailKitPython`: Classe para gerenciamento de criação e envio de mensagens via SMTP.
- Integração com API OAuth2 da Microsoft para obtenção de token de acesso e envio via SMTP autenticado.

---

## Requisitos

- Python 3.x
- PyQt5
- requests (para OAuth2)
- sqlite3 (incluído no Python)
- smtplib, email (bibliotecas padrão Python)

---

## Como usar

1. Certifique-se de que o Python 3 está instalado no seu sistema e que as dependências estejam instaladas:

    ```powershell
    pip install PyQt5 requests
    ```

2. Execute o script principal usando o Python (no Prompt de Comando, PowerShell ou terminal):

    ```powershell
    python Principal.py
    ```

3. Configure as credenciais SMTP e OAuth2 nas janelas de configuração acessíveis pelo menu **Configurações**.

4. No formulário principal, preencha os campos necessários:

    - **De:** endereço do remetente.
    - **Para:** endereço do destinatário.
    - **Cópia:** endereços em cópia (opcional).
    - **Assunto:** assunto da mensagem.
    - **Mensagem:** corpo da mensagem.

5. Clique em **Enviar** para enviar o e-mail.

6. A resposta (sucesso ou erro) será exibida na área de resultado da aplicação.

---

## Observações

- O envio via OAuth2 requer as credenciais válidas `TenantId` e `ClientId` configuradas no banco.
- Caso o OAuth2 não esteja ativado, a aplicação usa autenticação SMTP tradicional.
- A senha do usuário é utilizada para autenticação SMTP ou para obter o token OAuth2 via fluxo de senha (Resource Owner Password Credentials Grant).
- Certifique-se de que o servidor SMTP e as portas estão corretos e acessíveis na rede.

---

