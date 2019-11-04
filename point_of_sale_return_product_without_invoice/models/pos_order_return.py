# -*- encoding: utf-8 -*-
#
# Module written to Odoo, Open Source Management Solution

# Developer(s): Luis Ernesto García Medina
#               (ernesto.r.2.em@gmail.com)
########################################################################

from odoo import models, api, fields, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)

class PosOrderReturn(models.Model):
    _name = 'pos.order.return'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char()
    state = fields.Selection([('invoiced', 'Invoiced'),
        ('return', 'Return'), ('delivery', 'Delivery')], default = 'delivery')
    product_id = fields.Many2one('product.product')
    quantity = fields.Float()
    limit_date_return = fields.Date()
    order_line_ids = fields.One2many('pos.order.line', 'order_return_id')
    invoice_id = fields.Many2one('account.invoice')
    journal_id = fields.Many2one('account.journal', string='Payment Mode')


    @api.multi
    def action_view_invoice(self):
        return {
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.invoice_form').id,
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.invoice_id.id,
        }


    def _action_create_invoice_line(self, line=False, invoice_id=False):
        InvoiceLine = self.env['account.invoice.line']
        inv_name = line.product_id.name_get()[0][1]
        inv_line = {
            'invoice_id': invoice_id,
            'product_id': line.product_id.id,
            'quantity': line.qty,
            'name': inv_name,
        }
        # Oldlin trick
        invoice_line = InvoiceLine.sudo().new(inv_line)
        invoice_line._onchange_product_id()
        invoice_line.invoice_line_tax_ids = [(6, False, line.tax_ids_after_fiscal_position.filtered(lambda t: t.company_id.id == line.order_id.company_id.id).ids)]
        # We convert a new id object back to a dictionary to write to
        # bridge between old and new api
        inv_line = invoice_line._convert_to_write({name: invoice_line[name] for name in invoice_line._cache})
        inv_line.update(price_unit=line.price_unit, discount=line.discount)
        return InvoiceLine.sudo().create(inv_line)

    @api.multi
    def gen_return(self):
        self.ensure_one()
        if not self.journal_id:
            raise UserError(_('Para poder reembolsar debe establecer un diario.'))
        if fields.Date.today() > self.limit_date_return:
            raise UserError(_('No es posible reembolsar después de 30 días.'))
        order = self.order_line_ids[0].order_id
        currency = order.pricelist_id.currency_id
        amount = self.order_line_ids[0].price_subtotal_incl * -1
        data = {'payment_date': fields.Date.context_today(self),
                'payment_name': _('return')}
        # add_payment expect a journal key
        data['journal'] = self.journal_id.id
        data['amount'] = currency.round(amount) if currency else amount
        if not float_is_zero(amount, precision_rounding=currency.rounding or 0.01):
            order.add_payment(data)
        if order.test_paid():
            order.action_pos_order_paid()
        self.write({'state': 'return'})

    @api.multi
    def gen_invoice(self):
        Invoice = self.env['account.invoice']
        for oreturn in self:
            oreturn.order_line_ids.ensure_one()
            order = oreturn.order_line_ids.order_id
            local_context = dict(self.env.context, force_company=order.company_id.id, company_id=order.company_id.id)
            invoice = Invoice.new(order._prepare_invoice())
            invoice._onchange_partner_id()
            invoice.fiscal_position_id = order.fiscal_position_id

            inv = invoice._convert_to_write({name: invoice[name] for name in invoice._cache})
            new_invoice = Invoice.with_context(local_context).sudo().create(inv)
            message = _("This invoice has been created from the return order: <a href=# data-oe-model=pos.order.return data-oe-id=%d>%s</a>") % (oreturn.id, oreturn.name)
            new_invoice.message_post(body=message)
            oreturn.write({'invoice_id': new_invoice.id, 'state': 'invoiced'})
            # Invoice += new_invoice

            self.with_context(local_context)._action_create_invoice_line(oreturn.order_line_ids, new_invoice.id)

            new_invoice.with_context(local_context).sudo().compute_taxes()
