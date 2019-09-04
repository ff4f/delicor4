# Copyright (C) 2018 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    account_discount_id = fields.Many2one(
        'account.account',
        string="Cuenta de descuento",
        help="Cuenta contable donde se registrara el descuento de las facturas"
    )
    amount_valid = fields.Monetary(string='Importe Facturas', default=0,
                                   help='Importe maximo permitido para factura con NIT o CI = 0 y Razon Social= S/N')
