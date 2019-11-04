odoo.define('l10n_bo_point_of_sale.DB', function (require) {
    "use strict";

    var PosDB = require('point_of_sale.DB');

    PosDB.include({
        init: function (options) {
            this.invoice_id = 0;
            this._super(options);
        }
    });
});
