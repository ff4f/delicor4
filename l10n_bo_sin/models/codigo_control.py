# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from .codigo_control_gen import get_codigo_control

class CodigoControl(models.Model):
    _name = "codigo.control"
    _description = "Codigo de Control SIN"
    _order = "fecha"
    n_autorizacion = fields.Char(string=u"Nro. Autorización", size=15)
    n_factura = fields.Integer(string=u"Nro. Factura", size=10, digits=(16, 0))
    nit_ci = fields.Char(string=u"NIT/CI", size=12)
    fecha = fields.Date(string=u"Fecha")
    monto = fields.Float(string=u"Monto", digits=(12, 2))
    llave = fields.Char(string=u"Llave", size=200)
    codigo_control = fields.Char(string=u"Código Control", size=100)

    @api.multi
    def get_codigo_control(self):
        for line in self:
            line.codigo_control = get_codigo_control(line.n_autorizacion, line.n_factura, line.nit_ci, line.fecha,
                                                     line.monto, line.llave)

