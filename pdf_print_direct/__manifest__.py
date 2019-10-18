# -*- encoding: utf-8 -*-

{
    "name": "Impresión directa PDF",
    "version": "1.0",
    "depends": ["web"],
    "author": "Daniel Yang",
    'website': 'http://www.odoo.com',
    "category": "web",
    "description": """
    Imprimir pdf usando la libreria Print.js.
    Aviso: solo funciona con informes en pdf.
    """,
    "data": [
        'views/assets.xml',
    ],
    "init_xml": [],
    'update_xml': [],
    'demo_xml': [],
    "qweb": [
    ],
    
    'installable': True,
    'active': False,
}