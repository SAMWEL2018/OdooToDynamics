import json


class PostH:
    def __init__(self):
        self.externalDocumentNumber = "" #
        self.customerNumber = "90000"  # order header
        # self.billToCustomerNumber = "90000"  #
        # self.shipToName = "CASH HQ"  # order header
        # self.currencyCode: "KES"

        self.salesOrderLines = ""

    def getJson(self):
        return json.dumps(self.__dict__)
