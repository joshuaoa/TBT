# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

import logging


from odoo.addons.payment import utils as payment_utils
import requests
import json





_logger = logging.getLogger(__name__)


class PaymentTestController(http.Controller):

    @http.route('/payment/momo/payment', type='json', auth='public')
    def test_simulate_payment(self, reference, **kw):
        wallet_number = str(kw.get('walletNumber'))
        wallet_type = str(kw.get('walletType'))

        tx_sudo = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        username = tx_sudo.acquirer_id.prudential_momo_username
        client_id = tx_sudo.acquirer_id.prudential_momo_client_id
        password = tx_sudo.acquirer_id.prudential_momo_password
        auth_token = tx_sudo.acquirer_id.prudential_momo_auth_token
        payload = json.dumps({
            "clientId": client_id,
            "walletType": wallet_type,
            "walletNumber": wallet_number,
        })

        url = 'https://digihub.prudentialbank.com.gh/MobileMoneyPaymentTest/api/Transaction/WalletNameEnquiry'
        url_debit = 'https://digihub.prudentialbank.com.gh/MobileMoneyPaymentTest/api/Transaction/DebitWallet'
        headers = {
            'Authorization': auth_token,
            'Username': username,
            'Password': password,
            'Content-Type': "application/json",
        }
        try:
            enquiry_response = requests.request('POST', url, headers=headers, data=payload, timeout=60)
            enquiry_response.raise_for_status()
            _logger.info(f"Name Enquiry response:\n {enquiry_response.text}")
            enquiry_response_json = json.loads(enquiry_response.text)
        except requests.exceptions.ConnectionError:
            _logger.exception("unable to reach endpoint at", url)
            raise ValidationError("Prudential: " + "Could not establish the connection to the API.")
        except requests.exceptions.HTTPError as error:
            _logger.exception(
                f"invalid API request at {url} with data {payload}: {error.reponse.text}"
            )
            raise ValidationError("Prudential: " + "The communication with the API failed.")

        payload_debit = json.dumps({
            "clientId": client_id,
            "walletType": wallet_type,
            "walletNumber": wallet_number,
            "walletName": enquiry_response_json["accountName"],
            'amount': tx_sudo.amount,
            'transactionId': tx_sudo.reference,
            'remarks': f"Payment for {tx_sudo.reference}",
        })

        if enquiry_response_json["status"] == "0":
            _logger.info(f"Values for debit: {payload_debit}")
            try:
                debit_response = requests.request('POST', url_debit, headers=headers, data=payload_debit)
                debit_response.raise_for_status()
                debit_response_json = json.loads(debit_response.text)
            except requests.exceptions.ConnectionError:
                _logger.exception("unable to reach endpoint at", url_debit)
                raise ValidationError("Prudential: " + "Could not establish the connection to the API.")
            except requests.exceptions.HTTPError as error:
                _logger.exception(
                    f"invalid API request at {url_debit} with data {payload_debit}: {error.reponse.text}"
                )
                raise ValidationError("Prudential: " + "The communication with the API failed.")

            feedback = {
                'reference': reference,
                'response': debit_response_json
            }
            if debit_response_json["status"] == "0":
                _logger.info(f"Debit Wallet request succeeded with response:\n {debit_response.text}")
                request.env['payment.transaction'].sudo()._handle_feedback_data('momo', feedback)
            elif debit_response_json["status"] == "1":
                _logger.info(f"Debit Wallet request failed with response:\n {debit_response.text}")
                raise ValidationError("Prudential: " + "Could not complete transaction")
        else:
            _logger.info("Name enquiry failed")
            raise ValidationError("Prudential: " + "Could not verify wallet Number")





