import logging
import re

import requests


from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)

class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('prudentialmomo', 'Prudential Momo')], ondelete={'prudentialmomo': 'set default'})
    momo_username = fields.Char(
        string="Username", required_if_provider='prudentialmomo')
    momo_password = fields.Char(
        string="Password", required_if_provider='prudentialmomo', groups='base.group_system')
    base_url = fields.Char(
        string="Base Url", required_if_provider='prudentialmomo')

    def _prudentialmomo_get_api_url(self):
        self.ensure_one()

        if self.state == 'enabled':
            return self.base_url
        else:
            return self.base_url

    def _prudentialmomo_make_request( self, endpoint, payload=None, method='POST'):
        url = self.base_url + endpoint

        self.ensure_one()

        headers = {
            'Username': self.momo_username,
            'Password': self.momo_password,
        }
        try:
            response = requests.request(method, url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            _logger.exception("unable to reach endpoint at %s", url)
            raise ValidationError("Prudential: " + _("Could not establish the connection to the API."))
        except requests.exceptions.HTTPError as error:
            _logger.exception(
                "invalid API request at %s with data %s: %s", url, payload, error.response.text
            )
            raise ValidationError("Prudential: " + _("The communication with the API failed."))
        return response.json()

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'prudentialmomo':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_prudential_mobile_money.payment_method_prudentialmomo').id





