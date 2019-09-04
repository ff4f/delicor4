# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class LeyendaControl(models.Model):
    _name = "leyenda.control"
    _description = "Leyendas Control SIN"
    _order = "name"
    type = fields.Selection([
        ('genericas', 'Genéricas'),
        ('prestacion_servicio', 'Prestación de Servicios'),
        ('venta_producto', 'Venta de Productos'),
        ('salud', 'Salud'),
        ('servicio_banca', 'Servicios Bancarios y Financieros'),
        ('medios', 'Medios de Cominicación'),
    ], required=True, default='genericas',
        help="Seleccionar un tipo de Leyenda para ser categorizado")
    name = fields.Char(string="Descripción")
