# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from odoo import _, api, models
from odoo.exceptions import UserError, ValidationError

# from odoo.addons.payment import utils as payment_utils
# from odoo.addons.payment_ogone.controllers.main import OgoneController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.acquirer_id.provider != 'prudentialmomo':
            return res

        rendering_values = {
            'clientId':self.partner_id.name,
            'walletType': 'mtn',
            'senderName': self.partner_id.name,
            'senderNumber': self.partner_id.phone,
            'amount': self.amount,
            'transactionId': self.reference,
            'remarks': 'Payment for ' + self.reference,
        }
        return rendering_values

    def _send_payment_request(self):
        """ Override of payment to send a payment request to Adyen.

        Note: self.ensure_one()

        :return: None
        :raise: UserError if the transaction is not linked to a token
        """
        super()._send_payment_request()
        if self.provider != 'prudentialmomo':
            return

        data = {
            'clientId': self.partner_id.name,
            'walletType': 'mtn',
            'senderName': self.partner_id.name,
            'senderNumber': self.partner_id.phone,
            'amount': self.amount,
            'transactionId': self.reference,
            'remarks': 'Payment for ' + self.reference,
        }
        response_content = self.acquirer_id._prudentialmomo_make_request(
            endpoint='/DebitWallet',
            payload=data,
            method='POST'
        )

        # Handle the payment request response
        _logger.info("payment request response:\n%s", pprint.pformat(response_content))
        self._handle_feedback_data('prudentialmomo', response_content)

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'prudentialmomo':
            return tx

        reference = data.get('transactionId')
        if not reference:
            raise ValidationError("Prudential: " + _("Received data with missing merchant reference"))

        tx = self.search([('reference', '=', reference), ('provider', '=', 'prudentialmomo')])

        if not tx:
            raise ValidationError(
                "Prudential: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_feedback_data(self, data):
        super()._process_feedback_data(data)
        if self.provider != 'prudentialmomo':
            return

        # Handle the acquirer reference
        if 'transactionId' in data:
            self.acquirer_reference = data.get('transactionId')

        # Handle the payment state
        payment_state = data.get('status')
        if not payment_state:
            raise ValidationError("Prudential: " + _("Received data with missing payment state."))

        if payment_state == "0":
            self._set_done()
        elif payment_state == "1":
            _logger.warning("An error occurred on transaction with reference",
                            self.reference)
            self._set_error(
                _("An error occurred during the processing of your payment. Please try again.")
            )
        elif payment_state == "2":
            _logger.warning("The transaction with reference raise an Exception and was cancelled",
                            self.reference)
            self._set_canceled()
        else:
            _logger.warning("received data with invalid payment state: %s", payment_state)
            self._set_error(
                "Prudential: " + _("Received data with invalid payment state: %s", payment_state)
            )