from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.users'

    gpha_id = fields.Char(string="GPHA ID", related='partner_id.gpha_id')
    # agency = fields.Many2one('res.partner', string="Agency")
