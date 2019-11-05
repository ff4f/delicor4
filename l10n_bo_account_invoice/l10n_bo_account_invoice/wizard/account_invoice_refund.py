# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError
import datetime


class AccountInvoiceRefund(models.TransientModel):
    _inherit = "account.invoice.refund"

    date_invoice_origin = fields.Date(string='Fecha Factura Original', default=fields.Date.context_today, required=True,
                                      readonly=True)
    nota_credito_debito = fields.Boolean(string=u'Nota de Crédito/Débito')

    @api.model
    def default_get(self, fields):
        res = super(AccountInvoiceRefund, self).default_get(fields)
        res_ids = self._context.get('active_ids')
        inv = self.env['account.invoice'].browse(res_ids[0])
        mes_factura = inv.date_invoice.month
        mes_rectificado = datetime.date.today().month
        res_b = False
        if mes_factura != mes_rectificado:
            res_b = True
        res.update({
            'date_invoice_origin': inv.date_invoice,
            'nota_credito_debito': res_b,
        })
        return res

    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        mes_factura = self.date_invoice_origin.month
        mes_rectificado = self.date_invoice.month
        if mes_factura != mes_rectificado:
            self.nota_credito_debito = True
        else:
            self.nota_credito_debito = False

    @api.multi
    def compute_refund(self, mode='refund'):
        inv_obj = self.env['account.invoice']
        inv_tax_obj = self.env['account.invoice.tax']
        inv_line_obj = self.env['account.invoice.line']
        context = dict(self._context or {})
        xml_id = False

        for form in self:
            created_inv = []
            date = False
            description = False
            for inv in inv_obj.browse(context.get('active_ids')):
                if inv.state in ['draft', 'cancel']:
                    raise UserError(_('No se puede crear una nota de crédito para una factura  borrador/cancelada.'))
                if inv.reconciled and mode in ('cancel', 'modify'):
                    raise UserError(_(
                        'No se puede crear una nota de crédito para la factura que ya se ha conciliado, la factura debe ser primero sin conciliar, luego solo puede agregar una nota de crédito para esta factura.'))
                if not inv.warehouse_id and inv.type == 'out_invoice':
                    raise UserError(_('La Factura no tiene asignada una sucursal'))
                date = form.date or False
                description = form.description or inv.name
                if form.nota_credito_debito and inv.warehouse_id:
                    inv.write({'note_credit_debit': True})
                refund = inv.refund(form.date_invoice, date, description, inv.journal_id.id)
                if form.nota_credito_debito and inv.warehouse_id:
                    if not inv.warehouse_id.dosificacion_dc and inv.type == 'out_invoice':
                        raise UserError(_('Debe registrar una dosificación de notas de credito debito!'))
                    refund.write({
                        'warehouse_id': inv.warehouse_id.id,
                        'dosificacion': inv.warehouse_id.dosificacion_dc.id,
                        'n_autorizacion': inv.warehouse_id.dosificacion_dc.n_autorizacion,
                        'nit_ci': inv.partner_id.nit_ci,
                        'razon_social': inv.partner_id.razon_social,
                        'note_credit_debit': True,
                    })
                    inv.write({'note_credit_debit': True})
                elif inv.warehouse_id:
                    inv.write({'state_sin': 'A'})
                    refund.write({
                        'warehouse_id': inv.warehouse_id.id,
                        'nit_ci': inv.partner_id.nit_ci,
                        'razon_social': inv.partner_id.razon_social,
                        'state_sin': 'A',
                    })
                else:
                    inv.write({'state_sin': 'A'})
                created_inv.append(refund.id)
                if mode in ('cancel', 'modify'):
                    movelines = inv.move_id.line_ids
                    to_reconcile_ids = {}
                    to_reconcile_lines = self.env['account.move.line']
                    for line in movelines:
                        if line.account_id.id == inv.account_id.id:
                            to_reconcile_lines += line
                            to_reconcile_ids.setdefault(line.account_id.id, []).append(line.id)
                        if line.reconciled:
                            line.remove_move_reconcile()
                    refund.action_invoice_open()
                    for tmpline in refund.move_id.line_ids:
                        if tmpline.account_id.id == inv.account_id.id:
                            to_reconcile_lines += tmpline
                    to_reconcile_lines.filtered(lambda l: l.reconciled == False).reconcile()
                    if mode == 'modify':
                        invoice = inv.read(inv_obj._get_refund_modify_read_fields())
                        invoice = invoice[0]
                        del invoice['id']
                        invoice_lines = inv_line_obj.browse(invoice['invoice_line_ids'])
                        invoice_lines = inv_obj.with_context(mode='modify')._refund_cleanup_lines(invoice_lines)
                        tax_lines = inv_tax_obj.browse(invoice['tax_line_ids'])
                        tax_lines = inv_obj._refund_cleanup_lines(tax_lines)
                        # En caso de crear la tercera factura para entregar al cliente
                        invoice.update({
                            'type': inv.type,
                            'date_invoice': form.date_invoice,
                            'state': 'draft',
                            'number': False,
                            'invoice_line_ids': invoice_lines,
                            'tax_line_ids': tax_lines,
                            'date': date,
                            'origin': inv.origin,
                            'fiscal_position_id': inv.fiscal_position_id.id,
                            'warehouse_id': inv.warehouse_id.id,
                            'dosificacion': inv.warehouse_id.dosificacion.id,
                            'n_autorizacion': inv.warehouse_id.dosificacion.n_autorizacion,
                            'nit_ci': inv.partner_id.nit_ci,
                            'razon_social': inv.partner_id.razon_social
                        })
                        for field in inv_obj._get_refund_common_fields():
                            if inv_obj._fields[field].type == 'many2one':
                                invoice[field] = invoice[field] and invoice[field][0]
                            else:
                                invoice[field] = invoice[field] or False
                        inv_refund = inv_obj.create(invoice)
                        body = _(
                            'Correción de <a href=# data-oe-model=account.invoice data-oe-id=%d>%s</a><br>Motivo: %s') % (
                                   inv.id, inv.number, description)
                        inv_refund.message_post(body=body)
                        if inv_refund.payment_term_id.id:
                            inv_refund._onchange_payment_term_date_invoice()
                        created_inv.append(inv_refund.id)
                xml_id = inv.type == 'out_invoice' and 'action_invoice_out_refund' or \
                         inv.type == 'out_refund' and 'action_invoice_tree1' or \
                         inv.type == 'in_invoice' and 'action_invoice_in_refund' or \
                         inv.type == 'in_refund' and 'action_invoice_tree2'
        if xml_id:
            result = self.env.ref('account.%s' % (xml_id)).read()[0]
            if mode == 'modify':
                # When refund method is `modify` then it will directly open the new draft bill/invoice in form view
                if inv_refund.type == 'in_invoice':
                    view_ref = self.env.ref('account.invoice_supplier_form')
                else:
                    view_ref = self.env.ref('account.invoice_form')
                result['views'] = [(view_ref.id, 'form')]
                result['res_id'] = inv_refund.id
            else:
                invoice_domain = safe_eval(result['domain'])
                invoice_domain.append(('id', 'in', created_inv))
                result['domain'] = invoice_domain
            return result
        return True
