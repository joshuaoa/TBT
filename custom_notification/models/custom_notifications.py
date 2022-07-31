from odoo import fields, models, api, _


class CustomNotification(models.Model):
    _name = 'custom.notification'
    _description = 'Custom Notification'
    _rec_name = 'notification_id'

    STATES = {'posted': [('readonly', True)]}

    user_ids = fields.Many2many('res.users', 'notification_user_rel', 'notification_id', 'user_id', string="Users", states=STATES)
    title = fields.Char(string="Title", states=STATES)
    notes = fields.Text(string="Notes", states=STATES)
    notification_date = fields.Date(string="Date", default=fields.Date.today(), states=STATES)
    active = fields.Boolean("Active", default=True)
    notification_id = fields.Char(string='Notification ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
    ], default='draft')

    @api.model
    def create(self, values):
        if values.get('notification_id', _('New')) == _('New'):
            values['notification_id'] = self.env['ir.sequence'].next_by_code('custom.notification') or _('New')
        return super(CustomNotification, self).create(values)

    def action_post(self):
        self.state = 'posted'



