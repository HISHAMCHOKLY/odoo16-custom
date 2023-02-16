# -*- coding: utf-8 -*-
{
    'name': "pos_refund",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/pos_order_view.xml',
        # 'views/assets.xml',
        'views/refund_view.xml',

    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_refund/static/src/js/CategoryControlButton.js',
            'pos_refund/static/src/js/CategoryScreen.js',
            'pos_refund/static/src/xml/CategoryControlButton.xml',
            'pos_refund/static/src/xml/CategoryScreen.xml',
            'pos_refund/static/src/scss/pos.scss',
        ],
    },
    # 'assets': {'point_of_sale.assets': ['pos_refund/static/src/xml/templates.xml']},
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
