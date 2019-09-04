# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import re
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # _sql_constraints = [
    #     ('razon_name_unique_per_company', 'unique (razon_social, company_id)',
    #      "Razon Social debe ser único por compañia."),
    #     ('nit_ci_unique', 'unique (nit_ci, company_id)', "NIT/CI debe ser unico por compañia")
    # ]

    @api.constrains('razon_social', 'company_id')
    def _check_razon_unico(self):
        if self.razon_social:
            val = self.search_count([('razon_social', '=', self.razon_social), ('company_id', '=', self.company_id.id),
                                     ('user_ids', '=', False)])
            if val > 1 and self.razon_social != 'S/N' and not self.user_ids:
                raise ValidationError(_("La Razon Social ya esta registrado para su compañia."))

    @api.constrains('nit_ci', 'company_id')
    def _check_nitci_unico(self):
        if self.nit_ci:
            val = self.search_count(
                [('nit_ci', '=', self.nit_ci), ('company_id', '=', self.company_id.id), ('user_ids', '=', False)])
            if val > 1 and (self.nit_ci != '0' or not self.nit_ci):
                raise ValidationError(_("El NIT o CI ya esta registrado para su compañia."))

    @api.onchange('nit_ci')
    def onchange_nit_ci(self):
        for partner in self:
            if partner.nit_ci:
                x = partner.nit_ci
                res = re.sub("\D", "", x)
                partner.nit_ci = res

    @api.onchange('razon_social')
    def onchange_razon_social_upper(self):
        for partner in self:
            if self.env.user.has_group('l10n_bo_utils.group_uppercase') and partner.razon_social:
                partner.razon_social = partner.razon_social.upper()

    @api.onchange('name')
    def onchange_name_upper(self):
        for partner in self:
            if self.env.user.has_group('l10n_bo_utils.group_uppercase') and partner.razon_social:
                name_mayus = partner.name.upper()
                partner.name = name_mayus
