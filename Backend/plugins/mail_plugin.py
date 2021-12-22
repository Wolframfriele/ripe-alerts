import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pluginplay.interfaces.plugin as plugin


class MailPlugin(plugin.PluginInterface):
    DESCRIPTION = "A plugin which sends an alert to all entered email addresses"
    NAME = "mailplugin"
    DEFAULT_CONFIG = {
        "alert_addresses": [],
        "sender_address": "",
        "username": "",
        "password": "",
        # We add the gmail connection as default for simplicity
        "smtp_server": "smtp.gmail.com",
        "port": 587,
        "protocol": "starttls",
        "auth": True
    }

    def __init__(self, config: dict):
        # print(config)
        self.alert_addresses = config.get("alert_addresses")
        self._sender_address = config.get("sender_address")
        self._username = config.get("username")
        self._password = config.get("password")
        self._smtp_server = config.get("smtp_server")
        self._port = config.get("port")
        self._protocol = config.get("protocol")
        self._auth = config.get("auth")
        self._context = ssl.create_default_context()

    def receiver(self, data: str) -> None:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Alert testing"
        message["From"] = self._sender_address
        message["to"] = ", ".join(self.alert_addresses)

        text = f"""\
        You've got an alert!\n\n{data}"""

        html = f"""\
        You've got an alert! <br><br> {data}"""

        message.attach(MIMEText(text, "plain"))
        message.attach(MIMEText(html, "html"))

        system = smtplib.SMTP
        connection_settings = {"host": self._smtp_server, "port": self._port}
        if self._protocol == "ssl":
            system = smtplib.SMTP_SSL
            connection_settings["context"] = self._context

        with system(**connection_settings) as server:
            if self._protocol == "starttls":
                server.starttls(context=self._context)
            if self._auth:
                server.login(self._username, self._password)
            server.sendmail(self._sender_address, self.alert_addresses, message.as_string())
