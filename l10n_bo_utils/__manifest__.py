# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Utilidades Datos Maestros',
    'version': '1.0',
    'summary': 'Send Invoices and Track Payments',
    'sequence': 2,
    'description': """
    """,
    'category': 'Facturación Bolivia',
    'website': '',
    'images': [],
    'depends': ['base', 'product', 'l10n_bo_partner'],
    'data': [
        'security/uppercase_security.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
