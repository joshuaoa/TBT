# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import requests
import json



from odoo import _, api, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'prudentialcard':
            return tx

        reference = data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider', '=', 'prudentialcard')])
        if not tx:
            raise ValidationError(
                "Prudential: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_feedback_data(self, data):
        super()._process_feedback_data(data)
        if self.provider != "prudentialcard":
            return

        response_content = data.get('response')
        self.acquirer_reference = response_content.get('OrderID')

        # Handle the payment state
        payment_state = response_content.get('Status')
        if not payment_state:
            raise ValidationError("Prudential: " + _("Received data with missing payment state."))

        if payment_state == "00":
            self._set_pending()
        else:
            _logger.warning("received data with invalid payment state: %s", payment_state)
            self._set_error(
                "Prudential: " + _("Received data with invalid payment state: %s", payment_state)
            )

    def action_register_payment(self):
        self._set_done()
    

