# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution

# Developer(s): Luis Ernesto García Medina
#               (ernesto.r.2.em@gmail.com)
########################################################################

from odoo import models, api, fields, _
from datetime import datetime, timedelta

import logging

_logger = logging.getLogger(__name__)


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    order_return_id = fields.Many2one('pos.order.return')


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def action_view_return(self):
        return_ids = []
        for order in self:
            for line in order.lines:
                if line.order_return_id:
                    return_ids.append(line.order_return_id.id)
        return {
            'name': _('Returns'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'pos.order.return',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', return_ids)],
        }

    @api.model
    def _order_fields(self, ui_order):
        product_obj = self.env['product.product']
        AccountJournal = self.env['account.journal']
        return_obj = self.env['pos.order.return']
        result = super(PosOrder, self)._order_fields(ui_order)
        lines = result.get('lines', [])
        today = fields.Date.today()
        delta = timedelta(days=30)
        for line in lines:
            product_id = product_obj.browse(line[2].get("product_id"))
            if product_id.is_returnable:
                cash_id = AccountJournal.search([('type', '=', 'cash')])
                return_id = return_obj.create(
                    {'name': 'Order return ' + product_id.name + ' ' + result.get('name', ''),
                     'product_id': product_id.id,
                     'quantity': line[2].get('qty',0),
                     'limit_date_return': today + delta,
                     'journal_id': cash_id[0].id})
                line[2].update({"order_return_id": return_id.id})
        result.update({'lines': lines})
        return result

    def _action_create_invoice_line(self, line=False, invoice_id=False):
        if not line.product_id.is_returnable:
            return super(PosOrder, self)._action_create_invoice_line(line, invoice_id)
    

class CashBoxIn(models.TransientModel):
    _inherit = 'cash.box.in'

    receive_id = fields.Many2one("res.users")
    sender_id = fields.Many2one("res.users")
    auth_id = fields.Many2one("res.users")
    number = fields.Char(required=True, index=True, copy=False, default='New')

    @api.model
    def create(self, vals):
        if vals.get('number', 'New') == 'New':
            vals['number'] = self.env['ir.sequence'].next_by_code('cash.box.in') or '/'
        return super(CashBoxIn, self).create(vals)

    @api.multi
    def print_in_payment(self):
        return self.env.ref('point_of_sale_return_product_without_invoice.report_ticket_payment_action').report_action(self)

class CashBoxOut(models.TransientModel):
    _inherit = 'cash.box.out'

    receive_id = fields.Many2one("res.users")
    sender_id = fields.Many2one("res.users")
    auth_id = fields.Many2one("res.users")
    number = fields.Char(required=True, index=True, copy=False, default='New')

    @api.model
    def create(self, vals):
        if vals.get('number', 'New') == 'New':
            vals['number'] = self.env['ir.sequence'].next_by_code('cash.box.out') or '/'
        return super(CashBoxOut, self).create(vals)

    @api.multi
    def print_out_payment(self):
        return self.env.ref('point_of_sale_return_product_without_invoice.report_ticket_payment_action_out').report_action(self)

