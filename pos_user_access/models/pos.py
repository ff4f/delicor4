# -*- coding: utf-8 -*-


from odoo import fields, models,tools,api

class res_users(models.Model):
    _inherit = 'res.users' 
    
    wv_qty = fields.Boolean("Quantity",default=True)
    wv_discount = fields.Boolean("Discount",default=True)
    wv_price = fields.Boolean("Price",default=True)
    wv_plusminus = fields.Boolean("Allow +/- Button",default=True)
    wv_payment = fields.Boolean("Allow Payment",default=True)
    wv_customer = fields.Boolean("Change Customer",default=True)
    remove_order = fields.Boolean("Remove Order",default=True)
    add_new_order = fields.Boolean("Add new order.",default=True)
    remove_orderline = fields.Boolean("Remove Order Line",default=True)
    show_numpad = fields.Boolean("Show Numpad",default=True)






    