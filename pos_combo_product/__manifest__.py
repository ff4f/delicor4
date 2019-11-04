# -*- coding: utf-8 -*-
{
    'name': 'Pos Combo Product',
    'summary': "Point of Sale Combo Product",
    'description': 'General Ledger Filter by Account',
    'description': """
Point of Sale Combo Product.
========================
Module Contains : Allows to create ombo type product
Combo Pack : Facility to create Combo Product with list of products.
    """,

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    "support": "ipredictitsolutions@gmail.com",

    'category': 'Point of Sale',
    'version': '12.0.0.1.0',
    'depends': ['point_of_sale', 'combo_product'],

    'data': [
        'security/ir.model.access.csv',
        'views/pos_pack_template_view.xml',
    ],
    'qweb': ['static/src/xml/pos_view.xml'],

    'license': "OPL-1",
    'price': 20,
    'currency': "EUR",

    'auto_install': True,
    'installable': True,

    'images': ['static/img/main.png'],
    'live_test_url': 'https://youtu.be/W_-oDghiAO8',
}
