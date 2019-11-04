# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Facturacion Bolivia Punto de Venta',
    'version': '1.1',
    'summary': 'Extension a punto de venta para facturacion',
    'sequence': 1,
    'description': """
    """,
    'category': 'Facturación Bolivia',
    'website': '',
    'images': [],
    'depends': ['point_of_sale', 'l10n_bo_account_invoice', 'l10n_bo_sin', 'account'],
    'data': [
        'views/pos_bol_templates.xml',
        'views/report_invoice.xml',
        'views/account_report.xml',
    ],
    'qweb': [
         "static/src/xml/pos.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
