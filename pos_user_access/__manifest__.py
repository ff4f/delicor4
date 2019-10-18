# -*- coding: utf-8 -*-

{
    'name': "Pos change user wise access",
    'version': '1',
    'summary': """
        Pos change user wise access module allows you to give access in point of sale.

        """,
    'author': 'WebVeer',
    'category': 'Point of Sale',
    
    'website': '',

    'depends': ['point_of_sale'],
    'data': [
            'views/pos.xml',
            'views/templates.xml',
        ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': ['static/description/numpad.jpg'],
    'price': 49,
    'currency': 'EUR',
    'installable': True,
}
