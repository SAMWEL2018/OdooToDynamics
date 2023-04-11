import xmlrpc.client as cl

import requests.exceptions

from DataFetch import Fetch
from DynamicHeaderObject import PostH
from DynamicsJsnObject import PostInvoice
from HttpService import HttpService
from composeEmail import ComposeEmail
from configs import Configs
from OrderTrackerNumber import findCurrentOrderIndex, OrderTrackingUpdate, SkippedOrder
import logsConfigs as applog
from Dbqueries import query
import pymysql

UNEXPECTED_STATUS_CODE = 417
CREATED_STATUS_CODE = 201
REQUEST_TIMEOUT_CODE = 408
NOTFOUND_STATUS_CODE=404


class OrderProcessing:

    def __init__(self):
        self.fetch = Fetch()
        self.invoice = PostInvoice()
        self.http = HttpService()
        self.header = PostH()
        self.cfg = Configs()
        self.emailSend = ComposeEmail()
        self.query = query()

    def processOrder(self, id, is_retry):
        # id = int(findCurrentOrderIndex())
        ordered = self.fetch.posHeader(id)
        if ordered is not None and "ERROR" not in str(ordered):
            print('ordered: ', ordered['id'])
            pos_reference = ordered['pos_reference']
            self.header.externalDocumentNumber = pos_reference
            lineStmt = self.fetch.getLines(id)

            # exact item info
            itemlist = []
            for info in lineStmt:
                product_name = info['full_product_name']
                RefNo = self.fetch.getReferenceNo(product_name)
                print('reference ', RefNo)

                if RefNo is not None:
                    Item_id = self.fetch.getItemid(RefNo)
                    print('iTEM ID', Item_id)

                    try:
                        self.query.Postlines(ordered['id'], pos_reference, product_name, RefNo, info['qty'],
                                             info['price_unit'], Item_id)
                        print('post to db')
                    except Exception as e:
                        print('not posted: ',e)

                    if Item_id is not None:
                        item = {
                            "itemId": Item_id,
                            "quantity": info['qty'],
                            "unitPrice": info['price_unit'],

                        }
                        itemlist.append(item)
                        self.header.salesOrderLines = itemlist

                        # Exact payment for each item
                        print("Invoice Header :", self.header.getJson())

                    else:
                        description = 'Possibly error occurence on order due to missing reference no ' + RefNo + ' ' \
                                                                                                                 ' that odoo is having that lacks in dynamics on a product, check order : '
                        SkippedOrder((str(id)))

                        self.emailSend.SendErrorOnEmail(description, pos_reference)
                        self.query.PostAllOrders(ordered['id'], pos_reference, 0)
                        OrderTrackingUpdate(str(id + 1))
                        return "Product has no Itemid in dynamics therefore terminating post: +%s"% product_name, 417
                else:
                    res = "Reference no from one of the product " + product_name + " in the order is Empty! Check order : "
                    SkippedOrder((str(id)))

                    self.emailSend.SendErrorOnEmail(res, pos_reference)
                    self.query.PostAllOrders(ordered['id'], pos_reference, 0)
                    OrderTrackingUpdate(str(id + 1))
                    # appLog(2,"Response from API: "+res)
                    return "product reference no found: %s "% product_name, UNEXPECTED_STATUS_CODE
            try:
                res = self.http.post_Request(self.header.getJson())
                if "error" not in str(res):
                    if is_retry:
                        self.query.PostAllOrders(ordered['id'], pos_reference, 1)
                        applog.log(1,"Posted Sales Order : "+self.header.getJson())
                        print('Retry Posted')
                        return "Order created successfully", CREATED_STATUS_CODE
                    applog.log(1, "Posted Sales Order : " + self.header.getJson())
                    self.query.PostAllOrders(ordered['id'], pos_reference, 1)
                    OrderTrackingUpdate(str(id + 1))
                    print('Order Posted')
                    return 'Order created successfully ', CREATED_STATUS_CODE
                else:

                    SkippedOrder((str(id)))
                    OrderTrackingUpdate(str(id + 1))
                    self.query.PostAllOrders(ordered['id'], pos_reference, 0)
                    print('not posted')
                    return 'Order Not Posted, http error, Contact Admin', REQUEST_TIMEOUT_CODE

                    # print('Exception on dynamics side, check the order')
            except requests.exceptions.RequestException as e:
                print("Exception In Posting the order", e)
                return "Http on posting to dynamics, Contact Admin", NOTFOUND_STATUS_CODE
        else:
            print("No new Order", ordered)
            applog.log(1, "Checking next: " + 'No new order')
