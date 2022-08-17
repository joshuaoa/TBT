from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gpha_id = fields.Char(string="GPHA ID")
    agency = fields.Many2one('res.partner', string="Agency")
    vat = fields.Char(string='TIN', index=True,
                      help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
    parent_id = fields.Many2one('res.partner', string='Related Company', related='agency', readonly=False, store=True, index=True)
