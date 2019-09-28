# -*- coding: utf-8 -*-

from odoo import fields, models, api, registry, _
from .codigo_control_gen import get_codigo_control
from odoo.exceptions import Warning


class DosificacionControl(models.Model):
    _name = "dosificacion.control"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Registro de dosificaciones"
    _order = "date_end"
    name = fields.Char(string="Nombre Certificado", copy=False)
    active = fields.Boolean('Active', default=True)
    date_init = fields.Date(string="Valido desde fecha", copy=False, required=True)
    date_end = fields.Date(string="Fecha límite", help="Fecha límite de emisión para la dosificación", copy=False,
                           required=True)
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
    tiempo_alerta = fields.Integer(string='Tiempo Aviso',
                                   help='Tiempo de aviso para alertar el vencimiento de la dosificación registrada')

    @api.model
    def run_alerta(self, use_new_cursor=False, company_id=False):

        try:
            #if use_new_cursor:
            cr = registry(self._cr.dbname).cursor()
            self = self.with_env(self.env(cr=cr))

            group = self.env.ref('account.group_account_manager')
            usuario = group.users
            body_html = "<p><h3>Alerta Series dosificación</h3></p>" \
                        "<table style='width:80%;border: 1px solid black;border-collapse: collapse;'>" \
                        "<tr>" \
                        "<td><strong>Dosificación</strong></td>" \
                        "<td><strong>Fecha de caducidad</strong></td>" \
                        "<td><strong>Link</strong></td>" \
                        "</tr>"
            body_tr = ""

            sql_query = """select *
                            from (
                                   select
                                     *,
                                     (fecha_actual + (foo.tiempo_alerta :: text || ' day') :: INTERVAL) as fecha_alerta
                                   from (select
                                           t0.id,
                                           t0.name,
                                           t0.date_end,
                                           coalesce(t0.tiempo_alerta, 0)        as tiempo,
                                           (now() - interval '4 hours') :: DATE as fecha_actual,
                                           t0.tiempo_alerta
                                         from dosificacion_control t0) as foo
                                 ) as foo2
                            where foo2.fecha_alerta > foo2.date_end
                                                                    """

            self.env.cr.execute(sql_query)
            val = 0
            for line in self.env.cr.dictfetchall():
                body_tr = body_tr + """
                                            <tr>
                                            <td>""" + str(line.get('name')) + """</td>
                                            <td>""" + str(line.get('date_end')) + """</td>
                                            <td><a href=# data-oe-model=dosificacion.control data-oe-id=""" + str(
                    line.get('id')) + """>""" + str(line.get('name')) + """</a></td>
                                            </tr>
                                    """
                val = 1

            body_html_send = body_html + body_tr + "</table>"
            if val > 0:
                for us in usuario:
                    new_msg = self.message_post(body=body_html_send, message_type='comment', subtype='mail.mt_comment',
                                                needaction_partner_ids=[(4, us.partner_id.id)])
                    new_msg.sudo().write({'needaction_partner_ids': [(4, us.partner_id.id)]})
                cr.commit()
        finally:
            if use_new_cursor:
                try:
                    self._cr.close()
                except Exception:
                    pass

        return True

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
