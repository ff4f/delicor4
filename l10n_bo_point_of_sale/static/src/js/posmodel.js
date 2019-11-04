odoo.define('l10n_bo_point_of_sale.PosModel', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var partner_model = _.find(this.models, function (model) {
                return model.model === 'res.partner';
            });
            partner_model.fields.push('nit_ci', 'razon_social');
            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });
});