import json
import sys
import xmlrpc.client

from Dbqueries import query
from composeEmail import ComposeEmail
from configs import Configs
from HttpService import HttpService
from OrderTrackerNumber import findCurrentOrderIndex, OrderTrackingUpdate, SkippedOrder
import logsConfigs as applog

cfg = Configs()

# url = cfg.url
# db = cfg.db  # database name here
# username = cfg.username
# password = cfg.password
# # common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)


url = "https://pos-oyake.odoo.com"
db = "vombaka-oyake-prod-5154444"
username = "sales@oyake.co.ke"
password = "Sm@rt2022"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

items = HttpService()


# from logsConfigs import log as appLog
# import logsConfigs as appLog

class Fetch:

    def __init__(self):
        self.emailSend = ComposeEmail()

    def posHeader(self, id):
        try:
            pos_order = 'pos.order'

            pos = models.execute_kw(db, uid, password, pos_order, 'search', [[['id', '=', id]]])
            order = models.execute_kw(db, uid, password, pos_order, 'read', [pos])

            if "REFUND" not in str(order[0]['name']):
                return order[0] if len(order) > 0 else None

            else:
                self.emailSend.SendErrorOnEmail("This is an order of id " + str(id) + " that is a refund: ",
                                                str(order[0]))
                # query.PostAllOrders(ordered['id'], pos_reference, 1, current_date, "")
                # appLog.log(3, "This is refund order : " + str(order[0]))
                OrderTrackingUpdate(str(id + 1))


        except Exception as e:
            print("System Error ", e)
            return

    def getLines(self, id):
        pos = models.execute_kw(db, uid, password, 'pos.order.line', 'search', [[['order_id', '=', id]]])
        lines = models.execute_kw(db, uid, password, 'pos.order.line', 'read', [pos])

        return lines

    def getPayment(self, id):
        pos = self.models.execute_kw(db, self.uid, password, 'pos.payment', 'search', [[['id', '=', id]]])
        payment = self.models.execute_kw(db, self.uid, password, 'pos.payment', 'read', [pos])
        return payment

    def getItemid(self, referenceNo):

        pr = items.getAllItems()['value']
        for i in pr:
            item_x = i['number']
            if item_x == referenceNo:
                return i['id']

    def getReferenceNo(self, name):
        pos = models.execute_kw(db, uid, password, 'product.template', 'search', [[['name', '=', name]]])
        product = models.execute_kw(db, uid, password, 'product.template', 'read', [pos])
        print("product name: ", name)
        if len(product) == 0:

            print('Empty List: ', product)
            print('Proceeding to variants')
            clean_name = name.find('(')
            print("find: ", clean_name)
            print("name : ", name[:clean_name - 1])
            ready_name = name[:clean_name - 1]
            if ready_name == "SUMO CANDLE":
                pos1 = models.execute_kw(db, uid, password, 'product.product', 'search',
                                         [[['name', '=', "SUMO CANDLE (12*8) COLORED"]]])
                product1 = models.execute_kw(db, uid, password, 'product.product', 'read', [pos1])
                if len(product1) == 0:
                    print('no product.. variants')
                else:
                    reference_no_variants = product1[0]['default_code']
                    print("product code : ", reference_no_variants)
                    if reference_no_variants == False:
                        print("No reference from variants")
                        return None
                    return reference_no_variants

            pos1 = models.execute_kw(db, uid, password, 'product.product', 'search', [[['name', '=', ready_name]]])
            product1 = models.execute_kw(db, uid, password, 'product.product', 'read', [pos1])
            # self.generateRefVariants(product1)

            if len(product1) == 0:
                print('no product.. variants')
            else:
                reference_no_variants = product1[0]['default_code']
                print("product code : ", reference_no_variants)
                if reference_no_variants == False:
                    print("No reference from variants")
                    return None
                return reference_no_variants
        else:
            reference = product[0]['default_code']
            applog.log(1, 'Reference: ' + str(reference))

            if reference == False:
                return None

            return reference

    def generateRefVariants(self, product):

        if len(product) == 0:
            print('no product.. variants')
        else:
            reference_no_variants = product[0]['default_code']
            print("product code : ", reference_no_variants)
            if reference_no_variants == False:
                print("No reference from variants")
                return None
            return reference_no_variants

    def getVariantReferenceNo(self, name):

        pos1 = models.execute_kw(db, uid, password, 'product.product', 'search', [[['name', '=', name]]])
        product1 = models.execute_kw(db, uid, password, 'product.product', 'read', [pos1])
        print("product code : ", product1[0]['default_code'])
        if len(product1) == 0:
            print('Empty List')
        else:
            reference = product1[0]['default_code']
            if reference == False:
                print("proceeding to variants")

                # ref = product1[0]['default_code']
                print('Variant  ref: ', product1)

            print("Reference: ", reference)

    def getPaymentMethod(self, id):
        try:
            pos = models.execute_kw(db, uid, password, 'pos.payment', 'search', [[['id', '=', id]]])
            necessary = models.execute_kw(db, uid, password, 'pos.payment', 'read', [pos])
            print("data: ", json.dumps(necessary))
            return necessary
        except:
            return 'Error Occurred, Contact developer!'
