odoo.define('payment_card.payment_form', require => {
    'use strict';

    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');

    const paymentTestMixin = {

        _processDirectPayment: function (provider, acquirerId, processingValues) {
            if (provider !== 'prudentialcard') {
                return this._super(...arguments);
            }

            return this._rpc({
                route: '/payment/card/payment',
                params: {
                    'reference': processingValues.reference,
                },
            }).then((data) => {
                window.location = data.redirect_url;
            })
        },

        _prepareInlineForm: function (provider, paymentOptionId, flow) {
            if (provider !== 'prudentialcard') {
                return this._super(...arguments);
            } else if (flow === 'token') {
                return Promise.resolve();
            }
            this._setPaymentFlow('direct');
            return Promise.resolve()
        },
    };
    checkoutForm.include(paymentTestMixin);
    manageForm.include(paymentTestMixin);
});
