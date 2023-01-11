from app.consts import AVAILABLE_SERVICES
from app.service import send_telegram_auth, send_email_auth, post_telegram, post_email, send_slack_auth, post_slack


class TaskHandler:
    def __init__(self, services, request_data):
        self.services = services
        self.data = request_data
        self.return_val = ""

    def services_are_valid(self):
        for service in self.services:
            if not service in AVAILABLE_SERVICES:
                return False, service
        return True, None

    def get_text_time(self):
        text = self.data.get('text')
        time = self.data.get('time')
        return text, time

    def email_data(self):
        sender = self.data.get('sender')
        recipients = self.data.get('recipients')
        title = self.data.get('title')
        return sender, recipients, title

    def slack_data(self):
        return self.data.get("slack_bots")

    def check_required_data(self):
        valid_services, service = self.services_are_valid()
        if not valid_services:
            return "Service not available: {}.".format(service), 400

        text_to_send, time = self.get_text_time()
        if not text_to_send:
            return "Text field is required.", 400

        return (text_to_send, time), 200

    def handle_telegram(self):
        checks, status = self.check_required_data()
        if status == 400:
            return checks, status

        bot_names = self.data.get('tel_bot_names')

        if not bot_names:
            return "Bot names field is required.", 400

        tel_response, tel_status = send_telegram_auth(checks[0], bot_names, checks[1])
        self.return_val = f"{self.return_val} Telegram: {tel_response}"

        return self.return_val, tel_status

    def handle_email(self):
        checks, status = self.check_required_data()
        if status == 400:
            return checks, status

        sender, recipients, title = self.email_data()

        if not all([sender, recipients, title]):
            return "Sender, recipients and title are required.", 400

        email_response, email_status = send_email_auth(checks[0], title, sender, recipients, checks[1])
        self.return_val = f"{self.return_val} Email: {email_response}"

        return self.return_val, email_status

    def handle_slack(self):
        checks, status = self.check_required_data()
        if status == 400:
            return checks, status

        slack_bots = self.slack_data()
        if not all([slack_bot.get("name") and slack_bot.get("type") for slack_bot in slack_bots]):
            return "Bot name and type are required.", 400

        slack_response, slack_status = send_slack_auth(checks[0], slack_bots, checks[1])
        self.return_val = f"{self.return_val} Slack: {slack_response}"

        return self.return_val, slack_status

    def parse_services(self):
        if 'telegram' in self.services:
            tel_response, tel_status = self.handle_telegram()
            if tel_status != 200:
                return tel_response, tel_status

        if 'email' in self.services:
            email_response, email_status = self.handle_email()

            if email_status != 200:
                return email_response, email_status

        if 'slack' in self.services:
            slack_response, slack_status = self.handle_slack()

            if slack_status != 200:
                return slack_response,slack_status

        return self.return_val, 200


class NoAuthTaskHandler(TaskHandler):

    def tel_token_group(self):
        token = self.data.get('tel_token')
        group_id = self.data.get('tel_group_id')
        return token, group_id

    def email_data(self):
        sender, recipients, title = super().email_data()
        password = self.data.get('password')
        return sender, recipients, title, password

    def slack_data(self):
        token = self.data.get('slack_token')
        channel = self.data.get('slack_channel_id')
        return token, channel

    def handle_telegram(self):
        checks, status = self.check_required_data()
        if status == 400:
            return checks, status

        token, group_id = self.tel_token_group()
        if not (token and group_id):
            return "Token and group id are required.", 400

        tel_response, tel_status = post_telegram(token, group_id, checks[0], checks[1])
        self.return_val = f"{self.return_val} Telegram: {tel_response}"

        return self.return_val, tel_status

    def handle_email(self):
        checks, status = self.check_required_data()
        if status == 400:
            return checks, status

        sender, recipients, title, password = self.email_data()

        if not all([sender, recipients, title, password]):
            return "Sender, recipients, title and password are required.", 400

        email_response, email_status = post_email(sender, password, title, recipients, checks[0], checks[1])

        self.return_val = f"{self.return_val} Email: {email_response}"
        return self.return_val, email_status

    def handle_slack(self):
        checks, status = self.check_required_data()
        if status == 400:
            return checks, status

        token, channel = self.slack_data()

        if not (token and channel):
            return "Token and channel are required.", 400

        slack_response, slack_status = post_slack(channel, checks[0], token, checks[1])

        self.return_val = f"{self.return_val} Slack: {slack_response}"
        return self.return_val, slack_status
