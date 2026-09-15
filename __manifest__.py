{  # noqa: B018
    'name': 'Retail Automation',
    'version': '18.0.1.0.0',
    'summary': 'Retail automation solution for small businesses',

    'description': 
     """
     Retail Automation

     A scalable retail management solution designed to help small
     businesses manage products, orders, inventory, customers, and
     sales workflows.
     """,

    'author': 'Caleb Mutua',
    'category': 'Sales',
    'license': 'LGPL-3',

    'depends': ['base','product',],

    'data': [
         "security/ir.model.access.csv",
         "views/retail_brand_views.xml",
         "views/product_template_views.xml",
        ],

    'demo': [],

    'installable': True,
    'application': True,
    'auto_install': False,
}