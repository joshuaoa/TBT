

{
    "name": "Service Request",
    "version": "1.0.0.0",
    "author": "Albert",
    "complexity": "easy",
    "license": "AGPL-3",
    "category": "Tools",
    "description": """
    A module that allows users to send their service requests
    """,
    "images": [],
    "depends": ['product', 'mail'],
    "data": [
                'data/sequence.xml',
                'security/ir.model.access.csv',
                'views/service_request.xml',
                'views/form_success.xml',
                'views/portal.xml',
                'views/product.xml',
                'views/product_template.xml',
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
