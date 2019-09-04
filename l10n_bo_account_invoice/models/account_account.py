# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountAccount(models.Model):
    _inherit = "account.account"
    option_discount = fields.Boolean(string=u"Descuento Aplicable LCV", help=u'En caso de que el descuento se\n aplica al LCV al usar esta cuenta')