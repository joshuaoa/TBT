from odoo import fields, models, api


class ResUser(models.Model):
    _inherit = 'res.users'

    @api.model
    def signup(self, values, token=None):
        """ signup a user, to either:
            - create a new user (no token), or
            - create a user for a partner (with token, but no user for partner), or
            - change the password of a user (with token, and existing user).
            :param values: a dictionary with field values that are written on user
            :param token: signup token (optional)
            :return: (dbname, login, password) for the signed up user
        """

        if token:
            partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
            partner_user = partner.user_ids and partner.user_ids[0] or False
            if partner_user:
                values['gpha_id'] = values.get('gpha_id')
                values['agency'] = values.get('agency')
        else:
            values['gpha_id'] = values.get('gpha_id')
            values['agency'] = values.get('agency')
        return super(ResUser, self).signup(values,token)

