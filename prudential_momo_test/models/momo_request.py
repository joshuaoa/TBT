from odoo import fields, models, api, _
import logging
import requests
from requests.auth import HTTPBasicAuth
import json
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)



class MomoRequest(models.Model):
    _name = 'momo.request'
    _description = 'Description'

    response = fields.Text(string="Response")
    response_json = fields.Text(string="Response Json")
    status_code = fields.Char(string="Status Code")
    base_url = fields.Char(string="Base Url")

    def action_send_name_enquiry_request(self):
        url = 'https://digihub.prudentialbank.com.gh/MobileMoneyPaymentTest/api/Transaction/WalletNameEnquiry'
        username = "momoapi.user.tbt"
        password = "Temp123$"
        auth = HTTPBasicAuth(username, password)

        payload = json.dumps({
            "clientId": "33D00BAF-04BD-4EE3-BCC6-59AB0AD8C28A",
            "walletType": "mtn",
            "walletNumber": "233557666857",
        })

        headers = {
            "Username": "momoapi.user.tbt",
            "Password": "Temp123$",
            "Content-Type": "application/json"
        }

        # response = requests.post(url, data=payload, auth=auth)
        response = requests.request("POST", url, headers=headers, data=payload)
        _logger.info(response.json)

        self.base_url = url
        self.response = response.text
        self.status_code = response.status_code
        self.response_json = response.json
