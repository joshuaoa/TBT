import json
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class Notification(http.Controller):

    @http.route('/notification_web', type="http", auth="user", website=True )
    def notification_web(self, sortby=None, **kw):
        searchbar_sortings = {
            'date': {'label': _('Notification Date'), 'order': 'notification_date desc'},
            'id': {'label': _('ID'), 'order': 'notification_id'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        Notifications = http.request.env['custom.notification']
        current_user_id = request.env.user.id
        return http.request.render('custom_notification.view_notification', {
                'notifications': Notifications.search([('user_ids','=',current_user_id),('state','in',['posted']),('active','=',True)], order= order),
                'page_name' : 'notification',
                'searchbar_sortings': searchbar_sortings,
                'sortby': sortby,
            })

    @http.route('/notification_web/<model("custom.notification"):notification>/', type="http", auth="user", website=True)
    def display_notification_details(self, notification):
        return http.request.render('custom_notification.display_notification_details', {
            'notification': notification,
            'page_name': 'notification'
        })


class NotificationPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        current_user_id = request.env.user.id
        values = super()._prepare_home_portal_values(counters)
        values['notification_count'] = http.request.env['custom.notification'].search_count([('user_ids','=',current_user_id),('state','in',['posted']),('active','=',True)])
        return values
