# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _

from .numero_a_letra import to_word

from odoo.exceptions import Warning

class ReportInvoiceBol(models.AbstractModel):
    _name = 'report.l10n_bo_account_invoice.report_invoice_bol'

    @api.model
    def _get_report_values(self, docids, data=None):
        invoice = self.env['account.invoice'].browse(docids)
        if not invoice.date_invoice:
            raise Warning(_(
                'La factura tiene que estar valida para imprimir'))

        res = self.get_number_base(invoice)
        return {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': self.env['account.invoice'].browse(docids),
            'data': data,
            'get_number_base': res,
        }

    @api.multi
    def get_number_base(self, invoice):
        moneda = ''
        if invoice.currency_id.name == 'BOB':
            moneda = ' BOLIVIANOS'
        if invoice.currency_id.name == 'USD':
            moneda = ' DOLARES AMERICANOS'
        texto = to_word(invoice.amount_total) + moneda
        txt = str(texto).upper()
        return txt