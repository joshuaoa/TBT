import base64
import binascii
import hashlib
import hmac
import json
import logging
import pprint

import werkzeug
from werkzeug import urls

from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools.pycompat import to_text

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_adyen.const import CURRENCY_DECIMALS

_logger = logging.getLogger(__name__)


class PrudentialMomoController(http.Controller):

    @http.route('/payment/prudentialmomo/acquirer_info', type='json', auth='public')
    def prudentialmomo_acquirer_info(self, acquirer_id):
        acquirer_sudo = request.env['payment.acquirer'].sudo().browse(acquirer_id).exists()
        return {
            'state': acquirer_sudo.state,
            'Username': acquirer_sudo.momo_username,
            'Password': acquirer_sudo.momo_password,
        }

    @http.route('/payment/prudential/payment_methods', type='json', auth='public')
    def prudentialmomo_payment_methods(self, acquirer_id, partner_id=None):
        acquirer_sudo = request.env['payment.acquirer'].sudo().browse(acquirer_id)
        transaction_sudo = request.env['payment.transaction'].sudo().browse(acquirer_id)
        amount = transaction_sudo.amount
        partner_sudo = partner_id and request.env['res.partner'].sudo().browse(partner_id).exists()
        # lang_code = (request.context.get('lang') or 'en-US').replace('_', '-')
        # shopper_reference = partner_sudo and f'ODOO_PARTNER_{partner_sudo.id}'
        data = {
            'clientId': partner_sudo,
            'walletType': 'mtn',
            'senderName': partner_sudo,
            'senderNumber': partner_sudo.phone,
            'amount': amount,
            'transactionId': transaction_sudo.reference,
            'remarks': 'Payment for ' + transaction_sudo.reference,
            'channel': 'Web',
        }
        response_content = acquirer_sudo._prudentialmomo_make_request(
            endpoint='/DebitWallet',
            payload=data,
            method='POST'
        )
        _logger.info("paymentMethods request response:\n%s", pprint.pformat(response_content))
        return response_content

