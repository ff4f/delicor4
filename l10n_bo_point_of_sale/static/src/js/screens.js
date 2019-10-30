odoo.define('l10n_bo_point_of_sale.screens', function (require) {

    var screens = require('point_of_sale.screens');

    screens.ReceiptScreenWidget.include({
        handle_auto_print: function () {
            if (this.should_auto_print()) {
                if (this.should_close_immediately()) {
                    this.click_next();
                }
            } else {
                this.lock_screen(false);
            }
        },
        should_close_immediately: function () {
            var order = this.pos.get_order();
            var invoiced_finalized = order.is_to_invoice() ? order.finalized : true;
            return this.pos.config.iface_print_skip_screen && invoiced_finalized;
        },
    });
    screens.PaymentScreenWidget.include({
        finalize_validation: function () {
            var self = this;
            var order = this.pos.get_order();
            var value_bob = order.get_total_with_tax();
            var sn = order.attributes.client.razon_social;
            if (value_bob > 3000 && ((sn == 'S/N') || (sn == 's/n'))) {
                alert('No puede validar el pedido con monto mayor a 3,000.00 Bs.');
            }
            else {
                var change = order.get_change();
                order.amount_change = change;
                self._super();
            }

        },

    });
});
