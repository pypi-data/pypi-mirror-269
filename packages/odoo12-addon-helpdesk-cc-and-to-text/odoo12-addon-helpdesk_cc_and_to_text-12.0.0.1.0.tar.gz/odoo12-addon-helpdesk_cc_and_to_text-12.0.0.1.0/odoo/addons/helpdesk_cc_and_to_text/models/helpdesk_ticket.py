from odoo import api, fields, models
import re


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    email_to = fields.Char("To", help="Message recipients (emails)")
    email_cc = fields.Char("Cc", help="Carbon copy message recipients")

    def clean_email_cc(self, email_cc):
        # The pattern looks for anything XXXX@XXXX.XXX
        patron = r"[\w\.-]+@[\w\.-]+"

        # Find all matches using findall instead of a loop
        matches = re.findall(patron, email_cc)

        # Join all matches with comma separator
        cleaned_cc = ",".join(matches)

        return cleaned_cc

    @api.model
    def message_new(self, msg, custom_values=None):
        """Override message_new from mail gateway so we can set correct
        default values.
        """
        if custom_values is None:
            custom_values = {}

        defaults = {
            "email_to": msg.get("to", ""),
            "email_cc": self.clean_email_cc(msg.get("cc", "")),
        }
        defaults.update(custom_values)

        # Write default values coming from msg
        ticket = super().message_new(msg, custom_values=defaults)

        return ticket
