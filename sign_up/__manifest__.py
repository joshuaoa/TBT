

{
    "name": "Sign Up",
    "version": "1.0.0.0",
    "author": "Albert",
    "complexity": "easy",
    "license": "AGPL-3",
    "category": "Tools",
    "description": """
    Adds additional fields when signing up for website
    """,
    "images": [],
    "depends": [
        "auth_signup",
        "base"
    ],
    "data": [
        'views/sign_up.xml',
        # 'views/res_users.xml',
        'views/res_partner.xml',
    ],
    "application": True,
    "installable": True,
    "auto_install": False,

}
