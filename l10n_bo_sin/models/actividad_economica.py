# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ActividadEconomica(models.Model):
    _name = "actividad.economica"
    _description = "Actividades Economicas"
    _order = "name"
    name = fields.Char(string=u"Código-Nombre", help=u"Nombre y Actividad Economica del contribuyente")
