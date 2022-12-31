# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Prudential Card Payment Acquirer',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
This module adds a simple payment acquirer allowing to make card payments online using Prudential Bank API.
""",
    'depends': ['payment'],
    'data': [
        'views/payment_templates.xml',
        'views/payment_transaction.xml',
        'data/payment_acquirer_data.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_card/static/src/js/**/*',
        ],
    },
    'license': 'LGPL-3',
}
