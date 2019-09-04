# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class PosOrder(models.Model):
    _inherit = "pos.order"

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a pos order.
        """
        ret = super(PosOrder, self)._prepare_invoice()
        for order in self:
            if order.partner_id.razon_social == '':
                order.partner_id.razon_social = order.partner_id.name
            warehouse = self.env['stock.warehouse'].search([('lot_stock_id', '=', order.config_id.stock_location_id.id)])

        ret['warehouse_id'] = warehouse[0].id
        ret['dosificacion'] = warehouse[0].dosificacion.id
        ret['n_autorizacion'] = warehouse[0].dosificacion.n_autorizacion
        ret['nit_ci'] = order.partner_id.nit_ci
        ret['razon_social'] = order.partner_id.razon_social
        ret['comment'] = order.config_id.receipt_footer
        return ret