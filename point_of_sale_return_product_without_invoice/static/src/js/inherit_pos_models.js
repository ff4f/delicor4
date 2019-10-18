odoo.define('point_of_sale_return_product_without_invoice.models', function (require) {
"use strict";

var models = require('point_of_sale.models');



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
});