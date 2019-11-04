# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Codigo Control SIN',
    'version': '1.1',
    'summary': 'Manejo de Sucursales y Tiendas',
    'sequence': 3,
    'description': """
    """,
    'category': 'Facturación Bolivia',
    'website': '',
    'images': [],
    'depends': ['account', 'stock', 'l10n_bo_partner'],
    'data': [
        'security/ir.model.access.csv',
        'data/leyendas_data.xml',
        'views/codigo_control_view.xml',
        'views/leyenda_control_view.xml',
        'views/actividad_economica_view.xml',
        'views/dosificacion_control_view.xml',
        'views/sucursales_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
