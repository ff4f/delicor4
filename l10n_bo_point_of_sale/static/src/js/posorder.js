// New orders are now associated with the current table, if any.
odoo.define('l10n_bo_point_of_sale.posorder', function (require) {
    "use strict";
    var Model = require('web.Model');
    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;
    var gui = require('point_of_sale.gui');

    models.Order = models.Order.extend({
        get_invoice_name: function (name) {
            var order_domain = [['pos_reference', '=', name]];
            var posOrderModel = new Model('pos.order');
            var invoiceModel = new Model('account.invoice');
            var valor = 'Factura llego';
            posOrderModel.call('search_read', [order_domain]).pipe(function (result) {
                _.each(result, function (data) {
                    var invoice_id = data.invoice_id[0];
                    var invoice_domain = [['id', '=', invoice_id]];
                    invoiceModel.call('search_read', [invoice_domain]).pipe(function (result) {
                        _.each(result, function (data) {
                            valor = data.number;
                        });
                    });
                });
            });
            return valor;
        },

        export_for_printing: function () {
            var factura = this.get_invoice_name(this.name);
            var receipt = _super_order.export_for_printing.apply(this, arguments);
            return receipt;
        },

    });

});