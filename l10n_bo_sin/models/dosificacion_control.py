# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from .codigo_control_gen import get_codigo_control
from odoo.exceptions import Warning


class DosificacionControl(models.Model):
    _name = "dosificacion.control"
    _description = "Registro de dosificaciones"
    _order = "date_end"
    name = fields.Char(string="Nombre Certificado", copy=False)
    active = fields.Boolean('Active', default=True)
    date_init = fields.Date(string="Valido desde fecha", copy=False, required=True)
    date_end = fields.Date(string="Fecha límite", help="Fecha límite de emisión para la dosificación", copy=False, required=True)
    sucursal_id = fields.Many2one("stock.warehouse", string="Sucursal", readonly=True, copy=False)
    n_autorizacion = fields.Char(string=u"Nro. Autorización", size=15, required=True, default='0')
    n_factura_inicial = fields.Integer(string=u"Nro. Inicial", size=10, default=1, digits=(16, 0), copy=False)
    n_factura_final = fields.Integer(string=u"Nro. Limite", size=10, default=1000, digits=(16, 0), copy=False)
    n_factura_actual = fields.Integer(string=u"Nro. Actual", size=10, default=1, digits=(16, 0), copy=False)
    company_id = fields.Many2one("res.company", string=u"Compañia", default=lambda self: self.env.user.company_id)
    llave = fields.Char(string=u"Llave", required=True, copy=False)
    actividad = fields.Many2one("actividad.economica", string=u"Actividad Económica")
    leyenda = fields.Many2one("leyenda.control", string=u"Leyenda Asignada")
    type = fields.Selection([
        ('manual', 'Manual'),
        ('automatica', 'Computarizada'),
    ], required=True, string="Modalidad Facturación", default='automatica',
        help="Puede usar los dos modos Manual y Computarizada")

    type_inv = fields.Selection([
        ('invoice', 'Factura'),
        ('notes', 'Notas de Crédito/Débito'),
    ], required=True, string="Tipo de Documento Fiscal", default='invoice',
        help="Seleccionar las opcion de la Dosificación generada")

    @api.multi
    def get_codigo_control(self, n_factura, nit_ci, fecha, monto):
        for line in self:
            codigo_control = get_codigo_control(line.n_autorizacion, n_factura, nit_ci, fecha, monto, line.llave)
        return codigo_control

    @api.multi
    def plus_factura(self):
        for dosi in self:
            dosi.n_factura_actual += 1

    @api.onchange('n_factura_final', 'n_factura_inicial')
    def onchange_n_factura_final(self):
        if self.n_factura_final <= self.n_factura_inicial:
            raise Warning(
                _("Número factura final tiene que ser mayor de Inicial"))
