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
    description_1 = fields.Char(string="Description")
    quantity_1 = fields.Integer(string="Quantity")
    remarks_1 = fields.Text(string="Remarks")
    product_id_1 = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')],
                                 string="Service")
    description_2 = fields.Char(string="Description")
    quantity_2 = fields.Integer(string="Quantity")
    remarks_2 = fields.Text(string="Remarks")
    product_id_2 = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')],
                                 string="Service")
    description_3 = fields.Char(string="Description")
    quantity_3 = fields.Integer(string="Quantity")
    remarks_3 = fields.Text(string="Remarks")
    product_id_3 = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')],
                                 string="Service")
    description_4 = fields.Char(string="Description")
    quantity_4 = fields.Integer(string="Quantity")
    remarks_4 = fields.Text(string="Remarks")
    product_id_4 = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')],
                                 string="Service")
    description_5 = fields.Char(string="Description")
    quantity_5 = fields.Integer(string="Quantity")
    remarks_5 = fields.Text(string="Remarks")
    product_id_5 = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')],
                                 string="Service")
    populated = fields.Boolean(string="Populated", readonly=True)

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
        vals_first = {
            'product_id': self.product_id_1.id,
            'description': self.description_1,
            'quantity': self.quantity_1,
            'remarks': self.remarks_1
        }

        vals_second = {
            'product_id': self.product_id_2.id,
            'description': self.description_2,
            'quantity': self.quantity_2,
            'remarks': self.remarks_2
        }

        vals_third = {
            'product_id': self.product_id_3.id,
            'description': self.description_3,
            'quantity': self.quantity_3,
            'remarks': self.remarks_3
        }
        vals_fourth = {
            'product_id': self.product_id_4.id,
            'description': self.description_4,
            'quantity': self.quantity_4,
            'remarks': self.remarks_4
        }
        vals_fifth = {
            'product_id': self.product_id_5.id,
            'description': self.description_5,
            'quantity': self.quantity_5,
            'remarks': self.remarks_5
        }
        if self.quantity_2 == 0:
            self.details_ids = [(0, 0, vals_first)]
        elif self.quantity_3 == 0:
            self.details_ids = [(0, 0, vals_first), (0, 0, vals_second)]
        elif self.quantity_4 == 0:
            self.details_ids = [(0, 0, vals_first), (0, 0, vals_second), (0, 0, vals_third)]
        elif self.quantity_5 == 0:
            self.details_ids = [(0, 0, vals_first), (0, 0, vals_second), (0, 0, vals_third), (0, 0, vals_fourth)]
        else:
            self.details_ids = [(0, 0, vals_first), (0, 0, vals_second), (0, 0, vals_third), (0, 0, vals_fourth), (0, 0, vals_fifth)]
        self.populated = True

        self.state = 'processed'

    def action_done(self):
        self.state = 'done'

    def action_create_sale_order(self):
        for rec in self:
            lines = []
            for line in rec.details_ids:
                vals = {'product_id': line.product_id.id,
                        'name': line.description,
                        'product_uom_qty': line.quantity
                        }
                lines.append((0,0, vals))
            self.env['sale.order'].create(
                {
                    'partner_id': self.agent.partner_id.id,
                    'order_line': lines
                }
            )


class ServiceDetails(models.Model):
    _name = "service.details"
    _description = "Service Details"

    description = fields.Char(string="Description")
    quantity = fields.Integer(string="Quantity")
    remarks = fields.Text(string="Remarks")
    service_id = fields.Many2one('service.request', string="Services")
    product_id = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')],
                                 string="Service")


class Product(models.Model):
    _inherit = "product.product"

    product_type = fields.Selection([
        ('fixed','Fixed'),
        ('variable', 'Variable')
    ],default='fixed', string="Service Type")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('variable', 'Variable')
    ], default='fixed', string="Service Type")







