

{
    "name": "Custom Notification",
    "version": "1.0.0.0",
    "author": "Albert",
    "complexity": "easy",
    "license": "AGPL-3",
    "category": "Tools",
    "description": """
    A module for sending notifications to portal users
    """,
    "images": [],
    "depends": [
                "website"
                ],
    "data": [
                'security/security.xml',
                'security/ir.model.access.csv',
                'data/sequence.xml',
                'views/notification.xml',
                'views/portal_view.xml',
            ],
    "application": True,
    "installable": True,
    "auto_install": False,

}
