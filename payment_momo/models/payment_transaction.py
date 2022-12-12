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

    def _send_payment_request(self):
        super()._send_payment_request()
        if self.provider != 'momo':
            return

        payload = json.dumps({
            "clientId": "33D00BAF-04BD-4EE3-BCC6-59AB0AD8C28A",
            "walletType": 'mtn',
            "walletNumber": "233557666857",
        })

        payload_debit = {
            "clientId": "33D00BAF-04BD-4EE3-BCC6-59AB0AD8C28A",
            "walletType": 'mtn',
            "walletNumber": "233557666857",
            "walletName": "",
            'amount': self.amount,
            'transactionId': self.reference,
            'remarks': 'Payment for ' + self.reference,
        }

        url = 'https://digihub.prudentialbank.com.gh/MobileMoneyPaymentTest/api/Transaction/WalletNameEnquiry'
        url_debit = 'https://digihub.prudentialbank.com.gh/MobileMoneyPaymentTest/api/Transaction/DebitWallet'
        headers = {
            'Authorization': 'Basic bW9tb2FwaS51c2VyLnRidDpUZW1wMTIzJA==',
            'Username': 'momoapi.user.tbt',
            'Password': 'Temp123$',
            'Content-Type': "application/json",
        }

        try:
            enquiry_response = requests.request('POST', url, headers=headers, data=payload, timeout=60)
            enquiry_response.raise_for_status()
        except requests.exceptions.ConnectionError:
            _logger.exception("unable to reach endpoint at %s", url)
            raise ValidationError("Prudential: " + _("Could not establish the connection to the API."))
        except requests.exceptions.HTTPError as error:
            _logger.exception(
                "invalid API request at %s with data %s: %s", url, payload,
            )
            raise ValidationError("Prudential: " + _("The communication with the API failed."))
        enquiry_response_json = json.loads(enquiry_response.text)

        if enquiry_response_json["status"] == "0":
            try:
                debit_response = requests.request('POST', url_debit, headers=headers, data=payload_debit, timeout=60)
                debit_response.raise_for_status()
            except requests.exceptions.ConnectionError:
                _logger.exception("unable to reach endpoint at %s", url_debit)
                raise ValidationError("Prudential: " + _("Could not establish the connection to the API."))
            except requests.exceptions.HTTPError as error:
                _logger.exception(
                    "invalid API request at %s with data %s: %s", url_debit, payload,
                )
                raise ValidationError("Prudential: " + _("The communication with the API failed."))

            debit_response_json = json.loads(debit_response.text)
            feedback_data = {'reference': self.reference, 'response': debit_response_json}
            _logger.info(f"Debit Wallet response:\n, {debit_response.text}")

            _logger.info(f"Name Enquiry response:\n, {enquiry_response.text}")
            self._handle_feedback_data('test', feedback_data)

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'momo':
            return tx

        reference = data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider', '=', 'momo')])
        if not tx:
            raise ValidationError(
                "Momo: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_feedback_data(self, data):
        super()._process_feedback_data(data)
        if self.provider != "momo":
            return

        response_content = data.get('response')

        self.acquirer_reference = response_content.get('details').get('cb_reference')



        # Handle the payment state
        payment_state = response_content.get('status')
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

