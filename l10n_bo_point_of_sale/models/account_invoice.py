# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    amount_change = fields.Float('Cambio')
