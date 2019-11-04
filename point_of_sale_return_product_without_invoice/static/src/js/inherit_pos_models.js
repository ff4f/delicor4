odoo.define('point_of_sale_return_product_without_invoice.models', function (require) {
"use strict";

var models = require('point_of_sale.models');

var utils = require('web.utils');
var round_pr = utils.round_precision;

var _super_posmodel = models.PosModel.prototype;
models.PosModel = models.PosModel.extend({
    initialize: function (session, attributes) {
        var self = this;
        var product_model = _.find(this.models, function (model) {
            return model.model === 'product.product';
        });
        product_model.fields.push('is_returnable');
        return _super_posmodel.initialize.apply(this, arguments);
    },
});


models.Orderline = models.Orderline.extend({
    
    get_all_prices: function(){
        var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
        var taxtotal = 0;

        var product =  this.get_product();
        var taxes_ids = product.taxes_id;
        var taxes =  this.pos.taxes;
        var taxdetail = {};
        var product_taxes = [];

        

        _(taxes_ids).each(function(el){
            product_taxes.push(_.detect(taxes, function(t){
                return t.id === el;
            }));
        });
        if (product.is_returnable == true) {
            product_taxes = [];
        }

        var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
        _(all_taxes.taxes).each(function(tax) {
            if (!product.is_returnable == true) {
                taxtotal += tax.amount;
            }
            
            taxdetail[tax.id] = tax.amount;
        });
        console.log(all_taxes);
        

        return {
            "priceWithTax": all_taxes.total_included,
            "priceWithoutTax": all_taxes.total_excluded,
            "tax": taxtotal,
            "taxDetails": taxdetail,
        };
    },
});

});