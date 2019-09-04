# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Facturación Electronica Bolivia',
    'version': '1.1',
    'summary': 'Registro de datos SIN en facturas de venta y compras',
    'sequence': 4,
    'description': """
    """,
    'category': 'Facturación Bolivia',
    'website': '',
    'images': [],
    'depends': ['l10n_bo_sin', 'account', 'stock', 'purchase',
                'sale_order_line_discount_amount'],
    'data': [
        'views/company_view.xml',
        'views/account_invoice_view.xml',
        'views/report_invoice.xml',
        'views/report_invoice_cd.xml',
        'views/account_report.xml',
        'views/account_tax_view.xml',
        'wizard/account_invoice_refund_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
