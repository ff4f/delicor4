# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from . import numero_a_letra

class ReportInvoicePosPrintBol(models.AbstractModel):
    _name = 'report.l10n_bo_point_of_sale.report_invoice_print_pos_bol'

    @api.model
    def _get_report_values(self, docids, data=None):
        ids = self.ids
        invoice = self.env['account.invoice'].browse(docids)
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
        texto = numero_a_letra.to_word(invoice.amount_total) + moneda
        txt = str(texto).upper()
        return txt