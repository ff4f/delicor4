# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import qrcode
from .numero_a_letra import to_word
import base64
import io
from odoo.exceptions import Warning
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import datetime

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('tax_line_ids.amount', 'tax_line_ids.amount_rounding', 'invoice_line_ids.price_subtotal',
                 'currency_id', 'company_id', 'date_invoice', 'tax_line_ids')
    def _compute_amount_sin(self):
        amount_iva = 0
        amount_des = 0
        amount_exe = 0
        amount_ice = 0
        amount_open = 0
        for line in self.tax_line_ids:
            if line.tax_id.option_lcv == 'iva':
                amount_iva += line.amount
        for line_inv in self.invoice_line_ids:
            if line_inv.price_unit > 0:
                amount_open += line_inv.quantity * line_inv.price_unit
            # if self.type == 'in_invoice':
            #     for line_tax in line_inv.invoice_line_tax_ids:
            #         if line_tax.option_lcv == 'des':
            #             amount_des += line_inv.price_subtotal
            #         if line_tax.option_lcv == 'exe':
            #             amount_exe += line_inv.price_subtotal
            # else:
            amount_exe += line_inv.amount_exe
            amount_ice += line_inv.amount_ice_iehd
            amount_des += line_inv.discount_amt
        self.amount_iva = amount_iva
        self.amount_exe = amount_exe
        self.amount_ice_iehd = amount_ice
        self.amount_des = amount_des
        self.amount_open = amount_open
        self.amount_imp = amount_open - amount_des - amount_exe - amount_ice

    warehouse_id = fields.Many2one("stock.warehouse", string=u"Sucursal", readonly=True,
                                   states={'draft': [('readonly', False)]})
    qr_image = fields.Binary("Codigo QR", help="Imagen QR de factura", readonly=True,
                             states={'draft': [('readonly', False)]}, copy=False)
    nit_ci = fields.Char(string=u"NIT/CI", size=12, readonly=True, states={'draft': [('readonly', False)]}, copy=True,
                         default='0')
    razon_social = fields.Char(string=u"Razón Social", size=100, readonly=True, states={'draft': [('readonly', False)]},
                               copy=True, default='S/N')
    dosificacion = fields.Many2one("dosificacion.control", string=u"Certificado", readonly=True,
                                   states={'draft': [('readonly', False)]},
                                   help="Seleccionat Dosificación en función de dos tipo Manual, o computarizada")
    type_dosif = fields.Selection(related="dosificacion.type", string=u"Tipo Dosificación")
    n_autorizacion = fields.Char(string=u"Nro. Autorización")
    n_factura = fields.Integer(string=u"Nro. Factura", size=10, digits=(16, 0), copy=False, default=0)
    codigo_control = fields.Char(string=u"Código Control", size=100, default='0', copy=False)
    date_end = fields.Date(string="Límite emisión", related="dosificacion.date_end",
                           help="Fecha Límite de emision para la dosificación asignada")
    amount_text = fields.Char(string=u"Monto Literal")
    state_sin = fields.Selection([
        ('A', 'ANULADA'),
        ('V', u'VÁLIDA'),
        ('E', 'EXTRAVIADA'),
        ('N', 'NO UTILIZADA'),
        ('C', 'EMITIDA EN CONTINGENCIA'),
        ('L', u'LIBRE CONSIGNACIÓN'),
    ], "Estado SIN", help="Estado SIN", readonly=True, copy=False)
    n_dui = fields.Char(string=u"Nro. de DUI", size=16, default='0')
    tipo_com = fields.Selection([
        ('1', u'Compras para mercado interno con destino y actividades gravadas'),
        ('2', u'Compras para mercado interno con destino a actividades no gravadas'),
        ('3', u'Compras sujetas a proporcionalidad'),
        ('4', u'Compras para exportaciones'),
        ('5', u'Compras tanto para el mercado interno como para exportaciones'),
    ], "Tipo de Compra", help="Tipo de Compra", readonly=True, states={'draft': [('readonly', False)]})

    amount_iva = fields.Monetary(string='Importe IVA',
                                 store=True, readonly=True, compute='_compute_amount_sin',
                                 currency_field='company_currency_id', track_visibility='always')
    amount_des = fields.Monetary(string='Importe Descuento',
                                 currency_field='company_currency_id',
                                 store=True, readonly=True, compute='_compute_amount_sin')
    amount_exe = fields.Monetary(string='Importe Exento',
                                 currency_field='company_currency_id', store=True, readonly=True,
                                 compute='_compute_amount_sin')
    amount_ice_iehd = fields.Monetary(string='Importe ICE/IEHD',
                                      currency_field='company_currency_id', store=True, readonly=True,
                                      compute='_compute_amount_sin')
    amount_open = fields.Monetary(string='Total Factura',
                                  currency_field='company_currency_id', store=True, readonly=True,
                                  compute='_compute_amount_sin')

    amount_imp = fields.Monetary(string='Importe Base para Impuesto',
                                 currency_field='company_currency_id', store=True, readonly=True,
                                 compute='_compute_amount_sin', help="Import base para crédito o débito fiscal")

    note_credit_debit = fields.Boolean(string='Nota de Credito Debito', default=False, copy=False, readonly=True)

    date_time = fields.Datetime(string='Fecha/Hora')

    @api.constrains('n_factura', 'date_invoice')
    def _check_nivel_factura(self):
        if self.type_dosif == 'automatica':
            if self.n_factura != 0:
                val = self.search_count(
                    [('date_invoice', '>', self.date_invoice), ('company_id', '=', self.company_id.id),
                     ('n_factura', '>', self.n_factura)])
                if val > 1:
                    raise ValidationError(_(
                        "La factura que esta tratando de generar tiene fecha menor a una factura ya valida en el sistema"))

    @api.onchange('partner_id')
    def onchange_partner_id_sin(self):
        for invoice in self:
            if invoice.partner_id:
                if invoice.partner_id.razon_social:
                    invoice.razon_social = invoice.partner_id.razon_social
                else:
                    invoice.razon_social = 'S/N'
                if invoice.partner_id.nit_ci:
                    invoice.nit_ci = invoice.partner_id.nit_ci
                else:
                    invoice.nit_ci = '0'

    @api.onchange('warehouse_id')
    def onchange_warehouse_id(self):
        for invoice in self:
            if invoice.warehouse_id:
                # invoice.write({'dosificacion': invoice.warehouse_id.dosificacion.id, 'n_autorizacion': invoice.warehouse_id.dosificacion.n_autorizacion})
                invoice.dosificacion = invoice.warehouse_id.dosificacion.id
                invoice.n_autorizacion = invoice.warehouse_id.dosificacion.n_autorizacion

    @api.model
    def create(self, vals):
        if vals.get('codigo_control') and vals.get('type') == 'in_invoice':
            if len(vals.get('codigo_control')) <= 5:
                vals.update(codigo_control='0')
            elif len(vals.get('codigo_control')) > 5 and len(vals.get('codigo_control')) <= 12:
                cc_res = vals.get('codigo_control')[:-1]
                vals.update(codigo_control=cc_res)
        return super(AccountInvoice, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'codigo_control' in vals and self.type == 'in_invoice':
            if len(vals.get('codigo_control')) <= 5:
                vals.update(codigo_control='0')
            elif len(vals.get('codigo_control')) > 5 and len(vals.get('codigo_control')) <= 12:
                cc_res = vals.get('codigo_control')[:-1]
                vals.update(codigo_control=cc_res)
        return super(AccountInvoice, self).write(vals)

    @api.multi
    def action_invoice_open(self):
        # Validar la factura y que realize las validaciones necesarias
        res = super(AccountInvoice, self).action_invoice_open()
        for invoice in self:
            if invoice.type in ('out_invoice', 'out_refund') and invoice.type_dosif == 'automatica':
                dosif = invoice.dosificacion
                # Solo aplicable a ventas
                if not invoice.warehouse_id:
                    raise Warning(_(
                        'Debe seleccionar una sucursal'))
                # Obtener datos para hacer dosificacion
                nit_ci_em = invoice.warehouse_id.company_id.nit_ci
                n_factura = str(dosif.n_factura_actual)
                n_autorizacion = dosif.n_autorizacion
                if not dosif:
                    raise Warning(_(
                        'Certificado de Autorización no Seleccionado'))
                # fecha = invoice.date_invoice

                monto = invoice.amount_open
                monto_invoice = invoice.amount_total - invoice.amount_des
                descuento = invoice.amount_des
                ice_iehd = invoice.amount_ice_iehd
                exe = invoice.amount_exe
                monto_iva_valido = invoice.amount_total
                nit_ci = invoice.nit_ci
                razon = invoice.razon_social

                if not invoice.date_invoice:
                    raise ValidationError(_(
                        'Debe registrar la fecha de la factura'))

                if not nit_ci and not razon:
                    raise ValidationError(_(
                        'Debe registrar NIT/CI o Razón Social para facturar'))
                elif not invoice.partner_id.nit_ci and not invoice.partner_id.razon_social:
                    invoice.partner_id.write(
                        {'nit_ci': nit_ci, 'razon_social': razon})
                else:
                    invoice.write(
                        {'nit_ci': invoice.partner_id.nit_ci, 'razon_social': invoice.partner_id.razon_social})

                if invoice.date_invoice > dosif.date_end:
                    raise ValidationError(_(
                        'Fecha limite de dosificación superado, registre una nueva dosificación'))

                if nit_ci == '0' and (
                        razon == 'S/N' or razon == 's/n' or razon == 'sin nombre') and monto > invoice.company_id.amount_valid:
                    raise ValidationError(_(
                        'El monto de la factura no esta permitido para las facturas con\nRazon Social = S/N y NIT o CI = 0'))

                fecha = invoice.date_invoice.strftime('%d/%m/%Y')
                cod_control = dosif.get_codigo_control(n_factura, nit_ci, invoice.date_invoice, monto)
                monto_qr = "{:.2f}".format(monto, 2)
                monto_invoice_qr = "{:.2f}".format(monto_invoice, 2)
                if descuento > 0:
                    monto_descuento = "{:.2f}".format(descuento, 2)
                else:
                    monto_descuento = 0

                if ice_iehd > 0:
                    monto_ice_iehd = "{:.2f}".format(ice_iehd, 2)
                else:
                    monto_ice_iehd = 0

                if exe > 0:
                    monto_exe = "{:.2f}".format(exe, 2)
                else:
                    monto_exe = 0

                qr_string = str(nit_ci_em) + '|' + str(n_factura) + '|' + str(n_autorizacion) + '|' + str(
                    fecha) + '|' + str(monto_qr) + '|' + str(monto_invoice_qr) + '|' + str(
                    cod_control) + '|' + str(
                    nit_ci) + '|' + str(monto_ice_iehd) + '|0|' + str(monto_exe) + '|' + str(monto_descuento) + ''

                qr = qrcode.QRCode()
                qr.add_data(qr_string.encode('utf-8'))  # you can put here any attribute SKU in my case
                qr.make(fit=True)
                img = qr.make_image()
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                img_str = base64.b64encode(buffer.getvalue())
                # Siguiente factura
                dosif.plus_factura()
                # Generar valor en texto para la factura
                moneda = ''
                if invoice.currency_id.name == 'BOB':
                    moneda = ' BOLIVIANOS'
                if invoice.currency_id.name == 'USD':
                    moneda = ' DOLARES AMERICANOS'
                texto = to_word(invoice.amount_total) + moneda
                txt = str(texto).upper()
                invoice.write({'amount_text': txt,
                               'n_factura': n_factura,
                               'codigo_control': cod_control,
                               'qr_image': img_str,
                               'state_sin': 'V',
                               'date_time': datetime.datetime.now()})

            else:
                invoice.state_sin = 'V'
                moneda = ''
                if invoice.currency_id.name == 'BOB':
                    moneda = ' BOLIVIANOS'
                if invoice.currency_id.name == 'USD':
                    moneda = ' DOLARES AMERICANOS'
                texto = to_word(invoice.amount_total) + moneda
                txt = str(texto).upper()
                invoice.amount_text = txt
        return res

    @api.multi
    def invoice_print_bol(self):
        """ Impresion de factura con normativa en Bolivia
        """
        self.ensure_one()
        self.sent = True
        return self.env['report'].get_action(self, 'l10n_bo_account_invoice.report_invoice_bol')

    @api.model
    def _refund_tax_lines_account_change(self, lines, taxes_to_change):
        for invoice in self:
            tax_lines = invoice.tax_line_ids
            taxes_to_change_dc = {
                line.tax_id.id: line.tax_id.credit_debit_account_id.id
                for line in tax_lines.filtered(lambda l: l.tax_id.credit_debit_account_id != l.tax_id.account_id)
            }
            if not taxes_to_change and not taxes_to_change_dc:
                res = super(AccountInvoice, self)._refund_tax_lines_account_change(lines, taxes_to_change)
            elif taxes_to_change_dc and invoice.note_credit_debit:
                res = super(AccountInvoice, self)._refund_tax_lines_account_change(lines, taxes_to_change_dc)
            else:
                res = super(AccountInvoice, self)._refund_tax_lines_account_change(lines, taxes_to_change)
            return res

    # Load all unsold PO lines
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if not self.purchase_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.purchase_id.partner_id.id
            self.nit_ci = self.purchase_id.partner_id.nit_ci
            self.razon_social = self.purchase_id.partner_id.razon_social

        new_lines = self.env['account.invoice.line']
        for line in self.purchase_id.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
            data = self._prepare_invoice_line_from_po_line(line)
            new_line = new_lines.new(data)
            new_line._set_additional_fields(self)
            new_lines += new_line

        self.invoice_line_ids += new_lines
        self.payment_term_id = self.purchase_id.payment_term_id
        self.env.context = dict(self.env.context, from_purchase_order_change=True)
        self.purchase_id = False
        return {}

    @api.model
    def line_get_convert(self, line, part):
        res = super(AccountInvoice, self).line_get_convert(line, part)
        # make sure the account move line gets the invoice line id
        res.update({'invoice_line_id': line.get('invl_id', False)})
        return res

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        discount_total = 0.0
        # Calculate total discount and modify existing move_lines to
        # add discount amounts
        for line in self.invoice_line_ids:
            # check for discount on the invoice line
            if line.discount_amt:
                # browse move lines
                for move_line in move_lines:
                    # identify the moveline related to the invoice line
                    if move_line[2].get('invoice_line_id', False) == line.id:
                        # adjust value in the existing move_line by
                        # the discount amount
                        if self.type == 'out_refund':
                            debit = move_line[2].get('debit', 0.0)
                            debit += line.discount_amt
                            move_line[2].update({'debit': debit})
                        elif self.type == 'out_invoice':
                            credit = move_line[2].get('credit', 0.0)
                            credit += line.discount_amt
                            move_line[2].update({'credit': credit})

                        # add discount so we can write an extra move
                        # line for the discount
                        discount_total += line.discount_amt
        # create the extra move line for the discount
        if discount_total:
            # prepare vals for discount move line
            discount_line = self.move_line_get_discount(discount_total)
            # append move line to existing record
            move_lines.insert(0, (0, 0, discount_line))

        return move_lines

    @api.model
    def move_line_get_discount(self, discount_total):
        # Fetch Discount Account from company
        acc_discount_id = self.company_id.account_discount_id.id
        if not acc_discount_id:
            raise ValidationError(_("Please set Discount Account in "
                                    "company configuration!"))
        return {
            'type': 'src',
            'name': 'Discount',
            'price_unit': discount_total,
            'debit': self.type == "out_invoice" and discount_total or False,
            'credit': self.type == "out_refund" and discount_total or False,
            'quantity': 1,
            'price': discount_total,
            'account_id': acc_discount_id,
            'product_id': False,
            'uos_id': False,
            'account_analytic_id': False,
        }


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    invoice_line_id = fields.Many2one('account.invoice.line', 'Invoice Line')

    # discount_amount = fields.Float(string='Desc. Monto', digits=dp.get_precision('Product Price'), default=0.0,
    #                               help='Importe de los descuentos, bonificaciones y rebajas otorgadas.')

    amount_ice_iehd = fields.Float(string='ICE/IEHD', digits=dp.get_precision('Product Price'), default=0.0,
                                   help='Valor correspondiente al ICE, IEHD, Tasas y/o Contribuciones incluidas en la venta')

    amount_exe = fields.Float(string='Exento', digits=dp.get_precision('Product Price'), default=0.0,
                              help='Importe correspondiente a ventas por exportaciones de bienes y operaciones exentas.')

    # @api.onchange('discount_amt', 'amount_ice_iehd', 'amount_exe')
    # def onchange_discount_amount(self):
    #     for line in self:
    #         if line.quantity and line.price_unit:
    #             total_amount = line.discount_amt + line.amount_ice_iehd + line.amount_exe
    #             line.discount = (100 * total_amount) / (line.quantity * line.price_unit)

    @api.one
    @api.depends('price_unit', 'invoice_line_tax_ids', 'quantity', 'amount_ice_iehd', 'amount_exe', 'discount_amt',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        total_amount = self.discount_amt + self.amount_ice_iehd + self.amount_exe
        if self.quantity and self.price_unit:
            self.discount = (100 * total_amount) / (self.quantity * self.price_unit)
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id,
                                                          partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price

        total_1 = price_subtotal_signed + self.amount_ice_iehd + self.amount_exe
        self.price_subtotal = price_subtotal_signed = total_1

        self.price_total = taxes['total_included'] if taxes else self.price_subtotal

        total_1 = self.price_total + self.amount_ice_iehd + self.amount_exe
        self.price_total = total_1

        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(price_subtotal_signed, self.invoice_id.company_id.currency_id,
                                                      self.company_id or self.env.user.company_id,
                                                      date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign
