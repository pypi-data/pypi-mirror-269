from twilio.rest import Client

class SMSSender:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, body, from_number, to_number):
        message = self.client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        return message.sid
