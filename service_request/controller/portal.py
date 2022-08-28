from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class WebsiteForm(http.Controller):

    @http.route('/view_requests', type='http', auth='user', website=True)
    def view_requests(self, sortby=None, **kw):
        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
            'id': {'label': _('ID'), 'order': 'request_id'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        Requests = http.request.env['service.request']
        current_user_id = request.env.user.id
        return http.request.render('service_request.view_requests', {
            'requests': Requests.search([('create_uid','=',current_user_id),],order= order),
            'page_name': 'request',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

    @http.route('/service_requests', type='http', auth="user", website=True)
    def service_request(self):
        products = request.env['product.template'].sudo().search([])
        agencies = request.env['res.partner'].sudo().search([])
        agents = request.env['res.users'].sudo().search([])

        values = {}
        values.update({
            'products': products,
            'agencies': agencies,
            'agents':agents,
            'page_name': 'new_request',
        })
        return request.render("service_request.online_request_form", values)

    @http.route('/submit/request', type='http', auth="user", website=True)
    def submit_request(self, **kw):
        request_ids = request.env['service.request'].sudo().create(kw)
        for service in request_ids: service.state = 'submitted'
        return request.render("service_request.tmp_customer_form_success", {
            'request_ids': request_ids})


class ServicePortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        user_id = request.env.user.id
        values = super(ServicePortal, self)._prepare_home_portal_values(counters)
        values['service_request_count'] = http.request.env['service.request'].search_count([('create_uid','=',user_id),])
        return values