# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [
        ('default_code_uniq', 'unique (default_code, company_id)', u"Código de producto debe ser unico por compañia!"),
    ]

    @api.onchange('name')
    def onchange_name_product(self):
        for product in self:
            if self.env.user.has_group('l10n_bo_utils.group_uppercase') and product.name:
                product.name = product.name.upper()

    @api.onchange('default_code')
    def onchange_default_code_product(self):
        for product in self:
            if self.env.user.has_group('l10n_bo_utils.group_uppercase') and product.default_code:
                product.default_code = product.default_code.upper()

class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'
    _description = 'Productos'

    _sql_constraints = [
        ('default_code_uniq', 'unique (default_code,company_id)', "Código de producto variante debe ser unico por compañia!"),
    ]

    @api.onchange('name')
    def onchange_name_product(self):
        for product in self:
            if self.env.user.has_group('l10n_bo_utils.group_uppercase') and product.name:
                product.name = product.name.upper()

    @api.onchange('default_code')
    def onchange_default_code_product(self):
        for product in self:
            if self.env.user.has_group('l10n_bo_utils.group_uppercase') and product.default_code:
                product.default_code = product.default_code.upper()