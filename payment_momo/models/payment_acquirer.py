# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('momo', 'Momo')], ondelete={'momo': 'set default'})
    prudential_momo_client_id = fields.Char(
        string="Client ID", required_if_provider='momo', groups='base.group_system')
    prudential_momo_username = fields.Char(
        string="Username", required_if_provider='momo')
    prudential_momo_password = fields.Char(
        string="Password", required_if_provider='momo', groups='base.group_system')
    prudential_momo_auth_token = fields.Char(
        string="Auth Token", required_if_provider='momo', groups='base.group_system')

    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'momo':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_momo.payment_method_momo').id
