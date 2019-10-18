# -*- encoding: UTF-8 -*-
from openerp import api, models


class POSOrder(models.Model):
    _name = "pos.order"
    _inherit = "pos.order"
    _description = "Point of Sale"
    _order = "id desc"

    @api.multi
    def create_picking(self):
        res = super(POSOrder, self).create_picking()
        move_obj = self.env['stock.move']
        move_list = []
        picking_id = self.picking_id.id
        picking_type = self.picking_type_id
        location_id = self.location_id.id
        destination_id = picking_type.default_location_dest_id.id
        for combo in self.lines:
            if combo.product_id.is_combo:
                for product in combo.product_id.combo_product_id:
                    pos_qty = product.product_quantity * combo.qty
                    move_list.append(move_obj.create({
                        'name': self.name,
                        'product_uom': product.product_id.uom_id.id,
                        'picking_id': picking_id,
                        'picking_type_id': picking_type.id,
                        'product_id': product.product_id.id,
                        'product_uom_qty': abs(pos_qty),
                        'state': 'draft',
                        'location_id': location_id if pos_qty >= 0 else destination_id,
                        'location_dest_id': destination_id if pos_qty >= 0 else location_id,
                    }))
        self._force_picking_done(self.picking_id)
        for move in move_list:
            move._action_assign()
            move.filtered(lambda m: m.product_id.tracking == 'none')._action_done()
        return res
