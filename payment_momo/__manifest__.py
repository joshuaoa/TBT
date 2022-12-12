# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Momo Payment Acquirer',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
This module adds a simple payment acquirer allowing to make momo payments online using Prudential Bank API.
""",
    'depends': ['payment'],
    'data': [
        'views/payment_templates.xml',
        'views/payment_momo_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_momo/static/src/js/**/*',
        ],
    },
    'license': 'LGPL-3',
}
