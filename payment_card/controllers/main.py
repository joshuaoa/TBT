# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

import logging
import xml.etree.ElementTree as ET

import requests






_logger = logging.getLogger(__name__)


class PaymentCardController(http.Controller):

    @http.route('/payment/card/payment', type='json', auth='public')
    def card_payment(self, reference):
        tx_sudo = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])

        base_url = tx_sudo.acquirer_id.base_url
        merchant_id = tx_sudo.acquirer_id.prudential_card_merchant_id
        amount = int(round(tx_sudo.amount))
        currency_code = 936

        payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<TKKPG>\n<Request>\n<Operation>CreateOrder</Operation>\n<Language>EN</Language>\n<Order>\n<Merchant>{merchant_id}</Merchant>\n<Amount>{amount}</Amount>\n<Currency>{currency_code}</Currency>\n<Description>{reference}</Description>\n<ApproveURL>https://www.temabondedterminal.com</ApproveURL>\n<CancelURL>https://www.temabondedterminal.com</CancelURL>\n<DeclineURL>https://www.temabondedterminal.com</DeclineURL>\n<OrderType>Purchase</OrderType>\n</Order>\n</Request>\n</TKKPG>"
        headers = {
            "Content-Type": "application/xml"
        }
        header_redirect = {
            "Content-Type": "application/x-www-form-urlencoded;"
        }

        try:
            response = requests.request('POST', base_url, headers=headers, data=payload, verify='/home/odoo/src/user/payment_card/static/description/ca.pem'
                                    , cert=('/home/odoo/src/user/payment_card/static/description/cert.pem','/home/odoo/src/user/payment_card/static/description/key.pem'))
            response.raise_for_status()
            _logger.info(response.text)
        except requests.exceptions.ConnectionError:
            _logger.exception("unable to reach endpoint at %s", base_url)
            raise ValidationError("Prudential: " + "Could not establish the connection to the API.")
        except requests.exceptions.HTTPError as error:
            _logger.exception(
                "invalid API request at %s with data %s: %s", base_url, payload,
            )
            raise ValidationError("Prudential: " + "The communication with the API failed.")

            # Handling XML response
        root = ET.fromstring(response.content)

        response_json = {}

        for child in root:
            children = child.getchildren()
            for elem in children:
                if len(elem.getchildren()) == 0: 
                    response_json[elem.tag] = elem.text
                else:
                    elements = elem.getchildren()
                    for element in elements:
                        response_json[element.tag] = element.text

        _logger.info(response_json)

        # Getting values from response
        url = response_json.get('URL')
        order_id = response_json.get('OrderID')
        session_id = response_json.get('SessionID')
        status_code = response_json.get('Status')

        # Redirect url
        redirect_url = str(url) + f"?ORDERID={order_id}&SESSIONID={session_id}"
        redirect_payload = {
            'OrderID':order_id,
            'SessionID':session_id,
        }

        if status_code == "00":
            try:
                redirect_response = requests.post('https://acs2test.quipugmbh.com',headers=header_redirect,data=redirect_payload, verify='/home/odoo/src/user/payment_card/static/description/ca.pem'
                                    , cert=('/home/odoo/src/user/payment_card/static/description/cert.pem','/home/odoo/src/user/payment_card/static/description/key.pem'))
                redirect_response.raise_for_status()
            except requests.exceptions.ConnectionError:
                _logger.exception("unable to reach endpoint at https://acs2test.quipugmbh.com")
                raise ValidationError("Prudential: " + "Could not establish the connection to the API.")
            except requests.exceptions.HTTPError as error:
                _logger.exception(
                    f"invalid API request at https://acs2test.quipugmbh.com with data : {redirect_payload}"
                )
                raise ValidationError("Prudential: " + "The communication with the API failed.")
            
            if redirect_response.status_code == 200:
                feedback = {
                            'reference':reference,
                            'response': response_json
                            }
                request.env['payment.transaction'].sudo()._handle_feedback_data('prudentialcard', feedback)
                return {
                        'redirect_url': redirect_url,
            
                }
        else:
            raise ValidationError("Prudential: Could not complete transaction")





        


    
    
    





