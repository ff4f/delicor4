# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Campos Adicionales SIN',
    'version': '1.1',
    'sequence': 1,
    'summary': 'Datos adicionales requeridos por el SIN',
    'license': 'AGPL-3',
    'description': """
    """,
    'category': 'Facturación Bolivia',
    'website': '',
    'images': [],
    'depends': ['base'],
    'data': [
        'views/partner_view.xml',
        'views/company_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
