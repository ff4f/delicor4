# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        ret = super(SaleOrder, self)._prepare_invoice()
        ret['warehouse_id'] = self.warehouse_id.id
        ret['dosificacion'] = self.warehouse_id.dosificacion.id
        ret['n_autorizacion'] = self.warehouse_id.dosificacion.n_autorizacion
        ret['nit_ci'] = self.partner_id.nit_ci
        ret['razon_social'] = self.partner_id.razon_social
        return ret