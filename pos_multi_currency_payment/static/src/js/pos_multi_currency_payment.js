odoo.define('pos_multi_currency_payment', function (require) {
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var round_di = utils.round_decimals;
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('web.rpc');

    models.load_models([
        {
            model: 'res.currency',
            fields: [],
            loaded: function (self, currencies) {
                self.currencies = currencies;
                self.currency_by_id = {};
                for (var i = 0; i < currencies.length; i++) {
                    self.currency_by_id[currencies[i]['id']] = currencies[i];
                }
            }
        }
    ]);

    screens.PaymentScreenWidget.include({
        renderElement: function () {
            var self = this;
            this._super();
            var order = this.pos.get_order();
            order.selected_currency = this.pos.currency_by_id[this.pos.currency.id];
            this.$('.select-currency').on('change', function (e) {
                var currency_id = parseInt($('.select-currency').val());
                var selected_currency = self.pos.currency_by_id[currency_id];
                var company_currency = self.pos.currency_by_id[self.pos.currency['id']];
                /*
                    Return action if have not selected currency or company currency is 0
                 */
                if (!selected_currency || company_currency['rate'] == 0) {
                    return;
                }
                order.selected_currency = selected_currency;
                var currency_covert_text = self.format_currency_no_symbol(selected_currency['rate'] / company_currency['rate']);
                // add current currency rate to payment screen
                var $currency_covert = self.el.querySelector('.currency-covert');
                if ($currency_covert) {
                    $currency_covert.textContent = '1 ' + selected_currency['name'] + ' = ' + currency_covert_text + ' ' + company_currency['name'];
                }
                var selected_paymentline = order.selected_paymentline;
                if (selected_paymentline) {
                    selected_paymentline.set_amount("0");
                    self.inputbuffer = "";
                } else {
                    order.add_paymentline(self.pos.cashregisters[0]);
                }
                var due = order.get_due();
                var amount_full_paid = due / selected_currency['rate'] / company_currency['rate'];
                var due_currency = amount_full_paid;
                var $currency_paid_full = self.el.querySelector('.currency-paid-full');
                if ($currency_paid_full) {
                    $currency_paid_full.textContent = due_currency;
                }
                self.add_currency_to_payment_line();
                self.render_paymentlines();
            });
            this.$('.update-rate').on('click', function (e) {
                var currency_id = parseInt($('.select-currency').val());
                var selected_currency = self.pos.currency_by_id[currency_id];
                self.selected_currency = selected_currency;
                if (selected_currency) {
                    self.hide();
                    self.gui.show_popup('textarea', {
                        title: _t('Input Rate'),
                        value: self.selected_currency['rate'],
                        confirm: function (rate) {
                            var selected_currency = self.selected_currency;
                            selected_currency['rate'] = parseFloat(rate);
                            self.show();
                            self.renderElement();
                            var params = {
                                name: new Date(),
                                currency_id: self.selected_currency['id'],
                                rate: parseFloat(rate),
                            }
                            return rpc.query({
                                model: 'res.currency.rate',
                                method: 'create',
                                args:
                                    [params],
                                context: {}
                            }).then(function (rate_id) {
                                return rate_id;
                            }).then(function () {
                                self.gui.close_popup();
                            }).fail(function (type, error) {
                                if (error.code === 200) {
                                    event.preventDefault();
                                    self.gui.show_popup('error', {
                                        'title': _t('!!! ERROR !!!'),
                                        'body': error.data.message,
                                    });
                                }
                            });
                        },
                        cancel: function () {
                            self.show();
                            self.renderElement();
                        }
                    });
                }

            })
        },
        add_currency_to_payment_line: function (line) {
            var order = this.pos.get_order();
            line = order.selected_paymentline;
            line.selected_currency = order.selected_currency;
        }
    })
    ;

    var _super_paymentlinne = models.Paymentline.prototype;
    models.Paymentline = models.Paymentline.extend({
        initialize: function (attributes, options) {
            _super_paymentlinne.initialize.apply(this, arguments);
            this.amount_currency = this.amount_currency || 0;
            this.currency_id = this.currency_id || null;
        },
        set_amount: function (value) {
            _super_paymentlinne.set_amount.apply(this, arguments);
            var order = this.pos.get_order();
            var company_currency = this.pos.currency_by_id[this.pos.currency['id']];
            var amount = parseFloat(value);
            if (this.selected_currency) {
                this.currency_id = this.selected_currency['id'];
                this.amount_currency = amount;
                this.amount = this.amount_currency * this.selected_currency['rate'] / company_currency['rate'] ;
                console.log(this.amount);
            } else if (order.selected_currency) {
                this.selected_currency = order.selected_currency;
                this.amount_currency = amount;
                this.amount = this.amount_currency * this.selected_currency['rate'] / company_currency['rate'] ;
                this.currency_id = this.selected_currency['id'];
            }
            this.trigger('change', this);
        },
        export_as_JSON: function () {
            var json = _super_paymentlinne.export_as_JSON.apply(this, arguments);
            if (this.currency_id) {
                json['currency_id'] = this.currency_id;
            }
            if (this.amount_currency) {
                json['amount_currency'] = this.amount_currency;
            }
            return json;
        },
        export_for_printing: function () {
            var json = _super_paymentlinne.export_for_printing.apply(this, arguments);
            if (this.currency_id) {
                json['currency_id'] = this.currency_id;
            }
            if (this.selected_currency) {
                json['selected_currency'] = this.selected_currency;
            }
            if (this.amount_currency) {
                json['amount_currency'] = this.amount_currency;
            }
            return json;
        },
        init_from_JSON: function (json) {
            var res = _super_paymentlinne.init_from_JSON.apply(this, arguments);
            if (json['currency_id']) {
                var company_currency = this.pos.currency_by_id[this.pos.currency['id']];
                this['selected_currency'] = this.pos.currency_by_id[json['currency_id']];
                this['amount_currency'] = round_di(this.amount * company_currency['rate'] / this['selected_currency']['rate'] || 0, this.pos.currency.decimals);
                this['currency_id'] = this.pos.currency_by_id[json['currency_id']]['id'];
            }
            return res;
        }
    });
})
;
