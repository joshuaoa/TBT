# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models



class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('prudentialcard', 'Prudential Card')], ondelete={'prudentialcard': 'set default'})
    base_url = fields.Char(string="Base Url",required_if_provider='prudentialcard', groups='base.group_system')
    prudential_card_merchant_id = fields.Char(
        string="Merchant ID", required_if_provider='prudentialcard', groups='base.group_system')
    
    def _get_default_payment_method_id(self):
        self.ensure_one()
        if self.provider != 'prudentialcard':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_card.payment_method_prudentialcard').id
