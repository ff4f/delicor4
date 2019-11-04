// New orders are now associated with the current table, if any.
odoo.define('l10n_bo_point_of_sale.posorder', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;
    var _super = models.Order;
    models.Order = models.Order.extend({
        initialize: function () {
            _super_order.initialize.apply(this, arguments);
            this.amount_change = this.amount_change || 1;
            this.save_to_db();
        },
        export_as_JSON: function () {
            var json = _super.prototype.export_as_JSON.apply(this, arguments);
            json.amount_change = this.amount_change;
            return json;
        },

    });

});