# -*- coding: utf-8 -*-

from odoo import models, api, tools, _
import logging
try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class account_payment(models.Model):
    _inherit = "account.payment"

    def _check_fill_line(self, amount_str):
        return amount_str and (amount_str + ' ') or ''

    @api.multi
    def do_print_checks(self):
        if self:
            check_layout = self[0].company_id.account_check_printing_layout
            # A config parameter is used to give the ability to use this check format even in other countries than US, as not all the localizations have one
            if check_layout != 'disabled' and (self[0].journal_id.company_id.country_id.code == 'BO' or bool(self.env['ir.config_parameter'].sudo().get_param('account_check_printing_force_bo_format'))):
                self.write({'state': 'sent'})
                return self.env.ref('l10n_bo_check_printing.%s' % check_layout).report_action(self)
        return super(account_payment, self).do_print_checks()

class ResCurrency(models.Model):
    _inherit = "res.currency"

    @api.multi
    def amount_to_text(self, amount):
        self.ensure_one()
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
                        amt_value=_num2words(integer_value, lang=lang.iso_code),
                        amt_word="",
                        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' + tools.ustr('{amt_value} {amt_word}').format(
                        amt_value=str(fractional_value) + "/100",
                        amt_word="",
                        )
        return amount_words + " " + self.currency_unit_label
