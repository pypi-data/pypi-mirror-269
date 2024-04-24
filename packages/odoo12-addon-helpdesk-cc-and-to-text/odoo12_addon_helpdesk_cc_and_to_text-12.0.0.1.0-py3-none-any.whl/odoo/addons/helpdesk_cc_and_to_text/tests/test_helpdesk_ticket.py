from odoo.tests.common import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install", "helpdesk")
class TestHelpdeskTicket(TransactionCase):
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()
        self.helpdesk_ticket = self.env["helpdesk.ticket"]
        self.author_id = self.env["res.partner"].search([], limit=1)

    def test_clean_email_cc(self):
        ticket = self.helpdesk_ticket

        # Test case with valid cc emails
        cc_emails = "<test1@example.com>,'test2' <test2@example.com>,test3@example.com"
        cleaned_cc = ticket.clean_email_cc(cc_emails)
        self.assertEqual(
            cleaned_cc, "test1@example.com,test2@example.com,test3@example.com"
        )

        # Test case with invalid cc emails
        cc_emails_invalid = (
            "'test1' <test1@example.com>,'test2' <test2@example.com>,invalidemail"
        )
        cleaned_cc_invalid = ticket.clean_email_cc(cc_emails_invalid)
        self.assertEqual(cleaned_cc_invalid, "test1@example.com,test2@example.com")

        # Test case with empty cc emails
        cc_emails_empty = ""
        cleaned_cc_empty = ticket.clean_email_cc(cc_emails_empty)
        self.assertEqual(cleaned_cc_empty, "")

    @mute_logger("odoo.sql_db")
    def test_message_new(self):
        ticket = self.helpdesk_ticket

        # Test case with custom_values provided
        custom_values = {"email_to": "test@example.com"}
        message = {
            "to": "test@example.com",
            "cc": "",
            "subject": "prueba",
            "body": "prueba",
            "author_id": self.author_id.id,
        }
        ticket_rec = ticket.with_context(message_new_test=True).message_new(
            message, custom_values
        )
        self.assertEqual(ticket_rec.email_to, "test@example.com")
        self.assertEqual(ticket_rec.email_cc, "")

        # Test case without custom_values
        message_no_custom = {
            "to": "test@example.com",
            "cc": "",
            "subject": "prueba",
            "body": "prueba",
            "author_id": self.author_id.id,
        }
        ticket_no_custom = ticket.with_context(message_new_test=True).message_new(
            message_no_custom
        )
        self.assertEqual(ticket_no_custom.email_to, "test@example.com")
        self.assertEqual(ticket_no_custom.email_cc, "")

        # Test case with custom_values and invalid cc
        custom_values_invalid_cc = {"email_to": "test@example.com"}
        message_invalid_cc = {
            "to": "test@example.com",
            "cc": "invalidemail",
            "subject": "prueba",
            "body": "prueba",
            "author_id": self.author_id.id,
        }
        ticket.with_context(message_new_test=True).message_new(
            message_invalid_cc, custom_values_invalid_cc
        )
