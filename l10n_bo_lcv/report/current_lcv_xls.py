# -*- coding: utf-8 -*-
import datetime
import calendar
from odoo import models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class LcvReportXls(models.AbstractModel):
    _name = 'report.l10n_bo_lcv.lcv_report_xls.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def get_lines(self, object):
        lines = []
        days = calendar.monthrange(object.year, int(object.period))
        warehouse_id = object.warehouse_id.id
        date_init = datetime.date(year=object.year, month=int(object.period), day=1)
        date_end = datetime.date(year=object.year, month=int(object.period), day=int(days[1]))
        if object.type == 'ventas':
            invoices = self.env['account.invoice'].search(
                [('warehouse_id', '=', warehouse_id), ('date_invoice', '>=', date_init),
                 ('date_invoice', '<=', date_end), ('state', 'in', ('open', 'paid')), ('type', '=', 'out_invoice')],
                order="n_factura ASC")
        elif object.type == 'compras':
            invoices = self.env['account.invoice'].search(
                [('date_invoice', '>=', date_init),
                 ('date_invoice', '<=', date_end), ('state', 'in', ('open', 'paid')), ('type', '=', 'in_invoice')],
                order="n_factura ASC")

        valor = 1
        for invoice in invoices:
            vals = {
                'number_file': valor,
                'date_invoice': invoice.date_invoice,
                'n_factura': invoice.n_factura or '',
                'n_autorizacion': invoice.n_autorizacion or '',
                'state_sin': invoice.state_sin,
                'nit_ci': invoice.nit_ci or '',
                'razon_social': invoice.razon_social or '',
                'amount_total': invoice.amount_total or 0.0,
                'subtotal': invoice.amount_untaxed,
                'amount_tax': invoice.amount_tax,
                'amount_exe': invoice.amount_exe,
                'amount_des': invoice.amount_des,
                'amount_iva': invoice.amount_iva,
                'amount_open': invoice.amount_open,
                'amount_ice_iehd': invoice.amount_ice_iehd,
                'codigo_control': invoice.codigo_control,
                'n_dui': invoice.n_dui,
                'tipo_com': invoice.tipo_com,
            }
            valor += 1
            lines.append(vals)
        return lines

    def generate_xlsx_report(self, workbook, data, object):
        if object.type == 'ventas':
            sheet = workbook.add_worksheet('Libro de Ventas Estandar')
        elif object.type == 'compras':
            sheet = workbook.add_worksheet('Libro de Compras Estandar')

        format1 = workbook.add_format(
            {'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'vcenter',
             'bold': True})
        format11 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True,
             'bold': True})
        format10 = workbook.add_format(
            {'font_size': 10, 'align': 'right', 'right': True, 'left': True, 'bottom': False, 'top': False,
             'bold': False})
        format10_2 = workbook.add_format(
            {'font_size': 10, 'align': 'right'})
        format10_3 = workbook.add_format(
            {'font_size': 10, 'align': 'left'})
        format21 = workbook.add_format(
            {'font_size': 9, 'align': 'center', 'right': True, 'left': True, 'bottom': True, 'top': True,
             'bold': False})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        font_size_number_8 = workbook.add_format(
            {'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8, 'num_format': '#.##'})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')

        format21.set_align('center')
        format21.set_align('vcenter')

        cell_format1 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        cell_format1.set_num_format('#,##0.00')
        sheet.set_row(5, 60)
        tam_col = [5, 10, 10, 15, 5, 12, 25, 15, 15, 15, 15, 15, 15, 15, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                   12, 12, 12, 12, 12, 12]

        sheet.set_column('A:A', tam_col[0])
        sheet.set_column('B:B', tam_col[1])
        sheet.set_column('C:C', tam_col[2])
        sheet.set_column('D:D', tam_col[3])
        sheet.set_column('E:E', tam_col[4])
        sheet.set_column('F:F', tam_col[5])
        sheet.set_column('G:G', tam_col[6])
        sheet.set_column('H:H', tam_col[7])
        sheet.set_column('I:I', tam_col[8])
        sheet.set_column('J:J', tam_col[9])
        sheet.set_column('K:K', tam_col[10])
        sheet.set_column('L:L', tam_col[11])
        sheet.set_column('M:M', tam_col[12])
        sheet.set_column('N:N', tam_col[13])
        sheet.set_column('O:O', tam_col[14])
        sheet.set_column('P:P', tam_col[15])
        sheet.set_column('Q:Q', tam_col[16])
        sheet.set_column('R:R', tam_col[17])
        sheet.set_column('S:S', tam_col[18])
        sheet.set_column('T:T', tam_col[19])

        sheet.merge_range('B3:C3', u'PERIODO:', format10_2)
        sheet.merge_range('D3:E3', u'AÑO:', format10_2)
        sheet.write('F3:F3', object.year, format10_3)
        sheet.write('I3:I3', u'MES', format10_2)
        sheet.write('J3:J3', object.period, format10_3)

        sheet.merge_range('B4:D4', u'NOMBRE O RAZÓN SOCIAL:', format10_2)
        sheet.merge_range('E4:G4', object.company_id.razon_social, format10_3)
        sheet.write('I4:I4', u'NIT:', format10_2)
        sheet.merge_range('J4:K4', object.company_id.nit_ci, format10_3)
        if object.type == 'ventas':
            sheet.merge_range('F2:J2', 'LIBRO DE VENTAS', format1)
            sheet.write(5, 0, u'N°', format21)
            sheet.write(5, 1, u'FECHA DE LA\nFACTURA', format21)
            sheet.write(5, 2, u'N° DE LA \nFACTURA', format21)
            sheet.write(5, 3, u'N° DE AUTORIZACIÓN', format21)
            sheet.write(5, 4, u'ESTADO', format21)
            sheet.write(5, 5, u'NIT/CI \nCLIENTE', format21)
            sheet.write(5, 6, u'NOMBRE O \nRAZÓN SOCIAL', format21)
            sheet.write(5, 7, u'IMPORTE TOTAL \nDE LA VENTA', format21)
            sheet.write(5, 8, u'IMPORTE \nICE/IEHD/IPJ/TASAS/OTROS \nNO SUJETOS AL IVA', format21)
            sheet.write(5, 9, u'EXPORTACIONES Y \nOPERACIONES EXENTAS', format21)
            sheet.write(5, 10, u'VENTAS GRAVADAS \nA TASA CERO', format21)
            sheet.write(5, 11, u'SUBTOTAL', format21)
            sheet.write(5, 12, u'DESCUENTOS \nBONIFICACIONES \nY REBAJAS SUJETAS \nAL IVA', format21)
            sheet.write(5, 13, u'IMPORTE BASE \nPARA DÉBITO \nFISCAL', format21)
            sheet.write(5, 14, u'DÉBITO \nFISCAL', format21)
            sheet.write(5, 15, u'CÓDIGO DE \nCONTROL', format21)
            prod_row = 6
            prod_col = 0
            get_line = self.get_lines(object)
            amount_total = 0
            subtotal = 0
            amount_total2 = 0
            amount_tax = 0
            for each in get_line:
                fecha = each['date_invoice'].strftime('%d/%m/%Y')
                sheet.write(prod_row, prod_col, each['number_file'], font_size_8)
                sheet.write(prod_row, prod_col + 1, str(fecha), font_size_8)
                sheet.write(prod_row, prod_col + 2, each['n_factura'], font_size_8)
                sheet.write(prod_row, prod_col + 3, each['n_autorizacion'], font_size_8)
                sheet.write(prod_row, prod_col + 4, each['state_sin'], font_size_8)
                sheet.write(prod_row, prod_col + 5, each['nit_ci'], font_size_8)
                sheet.write(prod_row, prod_col + 6, each['razon_social'], font_size_8)
                sheet.write_number(prod_row, prod_col + 7, each['amount_open'], cell_format1)
                sheet.write_number(prod_row, prod_col + 8, each['amount_ice_iehd'], cell_format1)
                sheet.write_number(prod_row, prod_col + 9, each['amount_exe'], cell_format1)
                sheet.write_number(prod_row, prod_col + 10, 0, cell_format1)
                sheet.write_number(prod_row, prod_col + 11, each['amount_open'] - each['amount_ice_iehd'] - each['amount_exe'], cell_format1)
                sheet.write_number(prod_row, prod_col + 12, each['amount_des'], cell_format1)
                sheet.write_number(prod_row, prod_col + 13, each['amount_open'] - each['amount_ice_iehd'] - each['amount_exe']- each['amount_des'], cell_format1)
                sheet.write_number(prod_row, prod_col + 14, each['amount_iva'], cell_format1)
                sheet.write(prod_row, prod_col + 15, each['codigo_control'], font_size_8)
                amount_total += float(each['amount_open'])
                subtotal += float(each['subtotal'])
                amount_total2 += float(each['amount_open'])
                amount_tax += float(each['amount_iva'])
                prod_row += 1

            sheet.write(prod_row, 6, u'TOTAL', format21)
            sheet.write_number(prod_row, 7, amount_total, cell_format1)
            sheet.write_number(prod_row, 8, 0, cell_format1)
            sheet.write_number(prod_row, 9, 0, cell_format1)
            sheet.write_number(prod_row, 10, 0, cell_format1)
            sheet.write_number(prod_row, 11, subtotal, cell_format1)
            sheet.write_number(prod_row, 12, 0, cell_format1)
            sheet.write_number(prod_row, 13, amount_total2, cell_format1)
            sheet.write_number(prod_row, 14, amount_tax, cell_format1)

        elif object.type == 'compras':
            sheet.merge_range('F2:J2', 'LIBRO DE COMPRAS', format1)
            sheet.write(5, 0, u'N°', format21)
            sheet.write(5, 1, u'FECHA DE LA \nFACTURA O DUI', format21)
            sheet.write(5, 2, u'NIT PROVEEDOR', format21)
            sheet.write(5, 3, u'NOMBRE O RAZÓN SOCIAL', format21)
            sheet.write(5, 4, u'N° DE LA FACTURA', format21)
            sheet.write(5, 5, u'N° DE DUI', format21)
            sheet.write(5, 6, u'N° DE AUTORIZACIÓN', format21)
            sheet.write(5, 7, u'IMPORTE TOTAL \nDE LA COMPRA', format21)
            sheet.write(5, 8, u'IMPORTE \nNO SUJETO A \n CRÉDITO FISCAL', format21)
            sheet.write(5, 9, u'SUBTOTAL', format21)
            sheet.write(5, 10, u'DESCUENTOS \nBONIFICACIONES \nY REBAJAS SUJETAS \nAL IVA', format21)
            sheet.write(5, 11, u'IMPORTE BASE \nPARA CRÉDITO FISCAL', format21)
            sheet.write(5, 12, u'CRÉDITO FISCAL', format21)
            sheet.write(5, 13, u'CÓDIGO DE CONTROL', format21)
            sheet.write(5, 14, u'TIPO DE COMPRA', format21)
            prod_row = 6
            prod_col = 0
            get_line = self.get_lines(object)
            amount_total = 0
            subtotal = 0
            amount_total2 = 0
            amount_tax = 0
            amount_exe = 0
            amount_des = 0
            amount_iva = 0
            for each in get_line:
                fecha = each['date_invoice'].strftime('%d/%m/%Y')
                sheet.write(prod_row, prod_col, each['number_file'], font_size_8)
                sheet.write(prod_row, prod_col + 1, str(fecha), font_size_8)
                sheet.write(prod_row, prod_col + 2, each['nit_ci'], font_size_8)
                sheet.write(prod_row, prod_col + 3, each['razon_social'], font_size_8)
                sheet.write(prod_row, prod_col + 4, each['n_factura'], font_size_8)
                sheet.write(prod_row, prod_col + 5, each['n_dui'] or '0', font_size_8)
                sheet.write(prod_row, prod_col + 6, each['n_autorizacion'] or '', font_size_8)
                sheet.write_number(prod_row, prod_col + 7, each['amount_open'], cell_format1)
                sheet.write_number(prod_row, prod_col + 8, each['amount_exe'], cell_format1)
                sheet.write_number(prod_row, prod_col + 9, each['amount_open'] - each['amount_exe'], cell_format1)
                sheet.write_number(prod_row, prod_col + 10, each['amount_des'], cell_format1)
                sheet.write_number(prod_row, prod_col + 11,
                                   each['amount_open'] - each['amount_des'] - each['amount_exe'], cell_format1)
                sheet.write_number(prod_row, prod_col + 12, each['amount_iva'], cell_format1)
                sheet.write(prod_row, prod_col + 13, each['codigo_control'], font_size_number_8)
                sheet.write(prod_row, prod_col + 14, each['tipo_com'] or '', font_size_number_8)
                amount_total += float(each['amount_open'])
                subtotal += float(each['subtotal'])
                amount_total2 += float(each['amount_open'])
                amount_tax += float(each['amount_tax'])
                amount_exe += float(each['amount_exe'])
                amount_des += float(each['amount_des'])
                amount_iva += float(each['amount_iva'])
                prod_row += 1

            sheet.write(prod_row + 1, 6, u'TOTAL', format21)
            sheet.write_number(prod_row + 1, 7, amount_total, cell_format1)
            sheet.write_number(prod_row + 1, 8, amount_exe, cell_format1)
            sheet.write_number(prod_row + 1, 9, amount_total - amount_exe, cell_format1)
            sheet.write_number(prod_row + 1, 10, amount_des, cell_format1)
            sheet.write_number(prod_row + 1, 11, amount_total - amount_exe - amount_des, cell_format1)
            sheet.write_number(prod_row + 1, 12, amount_iva, cell_format1)
