import json
from odoo import http
from odoo.http import request


class Notification(http.Controller):

    @http.route('/notification_web', type="http", auth="user", website=True)
    def notification_web(self, **kw):
        Notifications = http.request.env['custom.notification']
        current_user_id = request.env.user.id
        return http.request.render('custom_notification.view_notification', {
                'notifications': Notifications.search([('user_ids','=',current_user_id),('state','in',['posted']),('active','=',True)])
            })

