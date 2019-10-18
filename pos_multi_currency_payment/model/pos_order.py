# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
import logging

_logger = logging.getLogger(__name__)


class pos_order(models.Model):
    _inherit = "pos.order"

    def _payment_fields(self, ui_paymentline):
        payment_fields = super(pos_order, self)._payment_fields(ui_paymentline)
        if ui_paymentline.get('currency_id', None):
            payment_fields['currency_id'] = ui_paymentline.get('currency_id')
        if ui_paymentline.get('amount_currency', None):
            payment_fields['amount_currency'] = ui_paymentline.get('amount_currency')
        return payment_fields

    def _prepare_bank_statement_line_payment_values(self, data):
        value = super(pos_order, self)._prepare_bank_statement_line_payment_values(data)
        if data.get('currency_id', None):
            value['currency_id'] = data['currency_id']
        if data.get('amount_currency', None):
            value['amount_currency'] = data['amount_currency']
        # if data.get('payment_name', False) == 'return': v12 no need
        #     value.update({
        #         'currency_id': self.env.user.company_id.currency_id.id if self.env.user.company_id.currency_id else None ,
        #         'amount_currency': data['amount']
        #     })
        return value
