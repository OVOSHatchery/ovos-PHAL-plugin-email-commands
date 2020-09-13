from mycroft.skills import MycroftSkill
from mycroft.messagebus.message import Message
from mail_monitor import EmailMonitor


class EmailMonitorSkill(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.email_config = self.config_core.get("email", {})

    def initialize(self):
        if "mail" not in self.email_config or "password" not in \
                self.email_config or "whitelist" not in self.email_config or\
                not self.email_config["whitelist"]:
            self.speak_dialog("error")
            raise RuntimeError
        else:
            try:
                self.mail_client = EmailMonitor(**self.email_config)
                self.mail_client.on_new_email = self.handle_new_email
                self.mail_client.setDaemon(True)
                self.mail_client.start()
            except:
                self.speak_dialog("error")
                raise

    def get_intro_message(self):
        self.speak_dialog("intro")

    def handle_new_email(self, email):
        self.log.debug(str(email))
        self.bus.emit(Message("recognizer_loop:utterance",
                              {"utterances": [email['payload']]},
                              {"source": email['email'],
                               "destinatary": "skills"}))

    def shutdown(self):
        self.mail_client.stop()


def create_skill():
    return EmailMonitorSkill()
