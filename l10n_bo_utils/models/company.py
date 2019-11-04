# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import re
class ResCompany(models.Model):
    _inherit = "res.company"
    _sql_constraints = [
        ('razon_name_unique', 'unique (razon_social)', u"Razon Social en compañía debe ser único."),
        ('nit_ci_unique', 'unique (nit_ci)', u"NIT/CI debe ser único.")
    ]

    @api.onchange('nit_ci')
    def onchange_nit_ci(self):
        for company in self:
            if company.nit_ci:
                x = company.nit_ci
                res = re.sub("\D", "", x)
                company.nit_ci = res

    @api.onchange('razon_social')
    def onchange_razon_social(self):
        for company in self:
            if self.env.user.has_group('l10n_bo_utils.group_uppercase') and company.razon_social:
                company.razon_social = company.razon_social.upper()
