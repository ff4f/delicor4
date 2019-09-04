# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'LCV Impuestos Bolivia',
    'version': '1.1',
    'summary': 'Libro de compras, ventas y bancarización',
    'sequence': 30,
    'description': """
    """,
    'category': 'Facturación Bolivia',
    'website': '',
    'images': [],
    'depends': ['l10n_bo_sin', 'stock', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/lcv_impuestos_view.xml',
        'wizard/lcv_export_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
