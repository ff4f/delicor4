# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution

# Developer(s): Luis Ernesto García Medina
#               (ernesto.r.2.em@gmail.com)
########################################################################
{
    'name': 'TPV return product',
    'author': '@Neto_odoo',
    'category': 'Point of sale',
    'sequence': 50,
    'summary': "TPV return product",
    'website': 'http://www.twitter.com/neto_odoo',
    'version': '1.0',
    'description': """
TPV return product
        """,
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'pos_assets.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/pos_order_view.xml',
        'views/pos_order_return_view.xml',
        'report/statement_report.xml'
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'installable': True,
    'application': False,
}