# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution

# Developer(s): Luis Ernesto García Medina
#               (ernesto.r.2.em@gmail.com)
########################################################################

from odoo import models, api, fields, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_returnable = fields.Boolean()
