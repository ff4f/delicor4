# -*- coding: utf-8 -*-

from operator import itemgetter
import time

from odoo import api, fields, models, _

class StockWarehouse(models.Model):
    _name = 'stock.warehouse'
    _inherit = 'stock.warehouse'
    _description = 'Sucursales'

    dosificacion = fields.Many2one("dosificacion.control", string=u"Certificado Activación(Facturas)", domain=[('sucursal_id', '=', False), ('type_inv', '=', 'invoice')])
    dosificacion_dc = fields.Many2one("dosificacion.control", string=u"Certificado Activación(Notas Crédito/Débito)", domain=[('sucursal_id', '=', False), ('type_inv', '=', 'notes')])
    is_begin = fields.Boolean('Es casa matríz')
    # Verificar que se pueda restringir la actualizacion de un dosificación
    @api.multi
    def write(self, vals):
        # Dont allow changing the company_id when account_move_line already exist
        if vals.get('dosificacion', False):
            dosificacion = self.env['dosificacion.control'].browse(vals['dosificacion'])
            for warehouse in self:
                dosificacion.sucursal_id = warehouse.id
        if vals.get('dosificacion_dc', False):
            dosificacion = self.env['dosificacion.control'].browse(vals['dosificacion_dc'])
            for warehouse in self:
                dosificacion.sucursal_id = warehouse.id
        return super(StockWarehouse, self).write(vals)