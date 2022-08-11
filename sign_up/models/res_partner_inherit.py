from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gpha_id = fields.Char(string="GPHA ID")
    agency = fields.Many2one('res.partner', string="Agency")
