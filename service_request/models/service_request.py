from odoo import fields, models, api, _


class ServiceRequest(models.Model):
    _name = 'service.request'
    _description = 'Service Request'
    _rec_name = 'request_id'

    STATES = {'done': [('readonly', True)]}

    agency = fields.Many2one('res.partner', string='Agency', domain="[('is_company','=',True)]",
                             required=True, states=STATES)
    agent = fields.Many2one('res.users', string='Agent', required=True, states=STATES)
    phone = fields.Char(string='Phone', states=STATES)
    email = fields.Char(string='Email', states=STATES)
    imdg_code = fields.Char(string='IMDG code / UN No.', required=True, states=STATES)
    request_id = fields.Char(string='Request ID', required=True, copy=False, readonly=True, index=True,
                                  default=lambda self: _('New'))
    details_ids = fields.One2many('service.details','service_id', states=STATES)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('processed', 'Processed'),
        ('done', 'Done')
    ], default='draft')

    @api.model
    def create(self, values):
        if values.get('request_id', _('New')) == _('New'):
            values['request_id'] = self.env['ir.sequence'].next_by_code('service.request') or _('New')
        return super(ServiceRequest, self).create(values)

    def action_submit(self):
        self.state = 'submitted'

    def action_process(self):
        self.state = 'processed'

    def action_done(self):
        self.state = 'done'


class ServiceDetails(models.Model):
    _name = "service.details"
    _description = "Service Details"

    description = fields.Char(string="Description")
    quantity = fields.Integer(string="Quantity")
    remarks = fields.Text(string="Remarks")
    service_id = fields.Many2one('service.request')
    product_id = fields.Many2one('product.template', domain=[('type','=','service')] string="Service", required=True,)




