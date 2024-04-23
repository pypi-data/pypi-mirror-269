import pytest
from notifylibrary.email_sender import EmailSender

from notifylibrary.email_sender import EmailSender
from unittest.mock import patch, MagicMock

def test_send_mail_success():
    # Setup the mocks
    smtp_instance_mock = MagicMock()
    with patch('smtplib.SMTP', return_value=smtp_instance_mock) as mock_smtp:
        email_sender = EmailSender(smtp_server="smtp.example.com", port=587, username="user", password="pass")

        # Call the method
        email_sender.send_mail("Test Subject", "Hello, World", "from@example.com", ["to@example.com"])

        # Validate call
        mock_smtp.assert_called_once_with("smtp.example.com", 587)
        smtp_instance_mock.login.assert_called_once_with("user", "pass")
        smtp_instance_mock.sendmail.assert_called_once()


def test_send_mail_failure(mocker):
    # Mock the smtplib client to raise an exception
    mocker.patch('smtplib.SMTP', side_effect=Exception("Failed to connect"))
    email_sender = EmailSender(smtp_server="smtp.example.com", port=587, username="user", password="pass")

    # Test sending an email and expect an exception
    with pytest.raises(Exception) as excinfo:
        email_sender.send_mail("Test Subject", "Hello, World", "from@example.com", ["to@example.com"])
    assert str(excinfo.value) == "Failed to connect"
