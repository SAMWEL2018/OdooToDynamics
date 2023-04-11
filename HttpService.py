import json

import requests

from composeEmail import ComposeEmail
from logsConfigs import log as appLog
from OrderTrackerNumber import findCurrentOrderIndex, OrderTrackingUpdate, SkippedOrder
from configs import Configs


class HttpService:

    def post_Request(self, invoiceJson):
        cfg = Configs()

        headers = {
            'Authorization': 'Basic RDM2NVxMWURJQUguQk9DSEVSRTpUN3F2dENiVnMvVTdVNVpUbDZUYXJ4YXRwVnpMS2M2bVlTOUxoYTc2Y2tRPQ==',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", cfg.live_sale_order_url, headers=headers, data=invoiceJson)
            code = response.status_code

            if code == 201 or code == 200:
                print('')
                # appLog(1, "Dynamics API response : " + response.text)

            else:
                # appLog(3, "Dynamics API response : " + response.text)
                emailSend = ComposeEmail()
                emailSend.SendErrorOnEmail("Error ", response.text)

            return response.json()

        except requests.exceptions.HTTPError as e:
            print('Connection error on Sale order URL: ', e)

    def getAllItems(self):
        cfg = Configs()

        payload = {}
        headers = {
            'Authorization': 'Basic RDM2NVxMWURJQUguQk9DSEVSRTpUN3F2dENiVnMvVTdVNVpUbDZUYXJ4YXRwVnpMS2M2bVlTOUxoYTc2Y2tRPQ=='
        }

        try:

            response = requests.request("GET", cfg.live_items_url, headers=headers, data=payload)

            return response.json()
        except requests.exceptions.RequestException as e:
            print('error while transacting on Items url : ', e)
