odoo.define('pos_user_access.pos_user_access', function (require) {
"use strict";

var models = require('point_of_sale.models');
var chrome = require('point_of_sale.chrome');
var core = require('web.core');
var PosPopWidget = require('point_of_sale.popups');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var gui = require('point_of_sale.gui');
var screens = require('point_of_sale.screens');
var _t = core._t;
    models.load_fields('res.users',['show_numpad','remove_orderline','add_new_order','remove_order','wv_customer','wv_payment','wv_plusminus','wv_price','wv_qty','wv_discount']);
    chrome.UsernameWidget.include({
        click_username: function(){
            var self = this;
            this.gui.select_user({
                'security':     true,
                'current_user': this.pos.get_cashier(),
                'title':      _t('Change Cashier'),
            }).then(function(user){
                self.pos.set_cashier(user);
                if(user.wv_qty){
                    $(".mode-button[data-mode='quantity']").removeAttr("disabled");
                    $(".mode-button[data-mode='quantity']").html("Qty");
                }
                else{
                    $(".mode-button[data-mode='quantity']").attr("disabled", "disabled");
                    $(".mode-button[data-mode='quantity']").html("");
                }
                if(user.wv_discount){
                    $(".mode-button[data-mode='discount']").removeAttr("disabled");
                    $(".mode-button[data-mode='discount']").html("Disc"); 
                }
                else{
                    $(".mode-button[data-mode='discount']").attr("disabled", "disabled");
                    $(".mode-button[data-mode='discount']").html("");   
                }
                if(user.wv_price){
                    $(".mode-button[data-mode='price']").removeAttr("disabled");
                    $(".mode-button[data-mode='price']").html("Price"); 
                }
                else{
                    $(".mode-button[data-mode='price']").attr("disabled", "disabled");
                    $(".mode-button[data-mode='price']").html("");     
                }
                if(user.wv_plusminus){
                    $(".numpad-minus").removeAttr("disabled");
                    $(".numpad-minus").html("+/-");  
                }
                else{
                    $(".numpad-minus").attr("disabled", "disabled");
                    $(".numpad-minus").html("");
                }
                if(user.show_numpad){
                    $(".custome .number-char").removeAttr("disabled");
                    // $(".number-char").html();
                    $(".custome .number-char" ).each(function() {
                      $( this ).html($(this).data('number'));
                    });
                }
                else{
                    $(".custome .number-char").attr("disabled", "disabled");
                    $(".custome .number-char").html("");           
                }
                if(user.wv_payment){
                    $(".button.pay").removeAttr("disabled");
                    $(".button.pay").html("<div class='pay-circle'><i class='fa fa-chevron-right' /> </div>Payment");
                }
                else{
                    $(".button.pay").attr("disabled", "disabled");
                    $(".button.pay").html("");
                }
                if(user.wv_customer){
                    $(".button.set-customer").removeAttr("disabled");
                    $(".button.set-customer").html('<i class="fa fa-user"></i> Customer');           
                }
                else{
                    $(".button.set-customer").attr("disabled", "disabled");
                    $(".button.set-customer").html("");
                }
                if(user.remove_orderline){
                    $(".numpad-backspace").removeAttr("disabled");
                    $(".numpad-backspace").html('<img height="21" src="/point_of_sale/static/src/img/backspace.png" style="pointer-events: none;" width="24">');
                }
                else{
                    $(".numpad-backspace").attr("disabled", "disabled");
                    $(".numpad-backspace").html("");  
                }
                // if(user.remove_order){
                //     $(".deleteorder-button").removeAttr("disabled");
                //     $(".deleteorder-button").html("");
                // }
                // else{
                //     $(".deleteorder-button").attr("disabled", "disabled");
                //     $(".deleteorder-button").html("");
                // }
                // if(user.add_new_order){
                //     $(".neworder-button").removeAttr("disabled");
                //     $(".neworder-button").html("");
                // }
                // else{
                //     $(".neworder-button").attr("disabled", "disabled");
                //     $(".neworder-button").html("");
                // }
                self.renderElement();
            });
        },
    });
    chrome.OrderSelectorWidget.include({
        neworder_click_handler: function(event, $el) {
            if (! this.pos.get_cashier().add_new_order) {
                this.gui.show_popup('error',{
                    'title': _t('Warning'),
                    'body':  _t('Please contact to your manager.'),
                });
            }
            else {
                return this._super();
            }
        },
        deleteorder_click_handler: function(event, $el) {
            if (! this.pos.get_cashier().remove_order) {
                this.gui.show_popup('error',{
                    'title': _t('Warning'),
                    'body':  _t('Please contact to your manager.'),
                });
            }
            else {
                return this._super();
            }
        },
    });

});

