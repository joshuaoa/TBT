{
    'name': 'Prudential Mobile Money Payment Acquirer',
    'version': '1.0',
    'category': 'Accounting/Payment Acquirers',
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'data/payment_acquirer_prudentialmomo_data.xml',
    ],
    'application': True,
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
        ],
    },
    'license': 'LGPL-3',
}
