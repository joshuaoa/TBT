odoo.define('payment_momo.payment_form', require => {
    'use strict';

    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');

    const paymentTestMixin = {

        _processDirectPayment: function (provider, acquirerId, processingValues) {
            if (provider !== 'momo') {
                return this._super(...arguments);
            }

            const walletNumber = document.getElementById('wallet_number').value;
            const walletType = document.getElementById('wallet_type').value;
            return this._rpc({
                route: '/payment/momo/payment',
                params: {
                    'reference': processingValues.reference,
                    'walletType': walletType,
                    'walletNumber': walletNumber,
                },
            }).then(() => {
                window.location = '/payment/status';
            });
        },

        _prepareInlineForm: function (provider, paymentOptionId, flow) {
            if (provider !== 'momo') {
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
