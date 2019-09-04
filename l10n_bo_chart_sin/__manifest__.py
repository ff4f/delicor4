# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 Cubic ERP - Teradata SAC. (https://cubicerp.com).

{
    "name": "Bolivia - Contabilidad",
    "version": "2.0",
    "description": """
*Plan de cuentas requerido por el SIN
*Configuración de Impuestos para registro de facturas y gastos
    """,
    "author": "Odoo ERP Bolivia",
    "website": "",
    'category': 'Localizacion',
    "depends": ["account"],
    "data": [
        "data/l10n_bo_chart_data.xml",
        "data/account_data.xml",
        "data/account_tax_data.xml",
        "data/account_chart_template_data.yml",
    ],
}
