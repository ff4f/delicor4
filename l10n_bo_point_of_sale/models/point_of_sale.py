# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class PosOrder(models.Model):
    _inherit = "pos.order"

    amount_change = fields.Float('Cambio')

    @api.model
    def _order_fields(self, ui_order):
        fields = super(PosOrder, self)._order_fields(ui_order)
        fields['amount_change'] = ui_order.get('amount_change', 0)
        return fields

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
        ret['amount_change'] = order.amount_change
        return ret

    def _action_create_invoice_line(self, line=False, invoice_id=False):
        invoice_line_id = super(PosOrder, self)._action_create_invoice_line(line=line,invoice_id=invoice_id)
        monto_desc = ((line.discount/100)*line.price_unit)*line.qty
        invoice_line_id.write({'discount_amt': monto_desc})
        return invoice_line_id