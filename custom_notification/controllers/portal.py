import json
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class Notification(http.Controller):

    @http.route('/notification_web', type="http", auth="user", website=True)
    def notification_web(self, **kw):
        Notifications = http.request.env['custom.notification']
        current_user_id = request.env.user.id
        return http.request.render('custom_notification.view_notification', {
                'notifications': Notifications.search([('user_ids','=',current_user_id),('state','in',['posted']),('active','=',True)], order='notification_date desc')
            })

    @http.route('/notification_web/<model("custom.notification"):notification>/', type="http", auth="user", website=True)
    def display_notification_details(self, notification):
        return http.request.render('custom_notification.display_notification_details', {
            'notification': notification,
        })


class NotificationPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        current_user_id = request.env.user.id
        values = super()._prepare_home_portal_values(counters)
        values['notification_count'] = http.request.env['custom.notification'].search_count([('user_ids','=',current_user_id),('state','in',['posted']),('active','=',True)])
        return values
