import json


class PostInvoice:
    def __init__(self):
        self.amount = 0  # payment_amount
        self.name = ""  # order header
        self.amountIncludingVAT = ""  # payment_amount
        self.billToName = ""  # order header
        self.sellToCustomerName = ""  # order header
        self.documentDate = ""  # order header
        self.postingDate = ""  # order header
        self.pricesIncludingVAT = True
        self.customerPostingGroup = "DOMESTIC"
        # list of items
        self.productsLine = ""  # order line
        self.paymentMethod = ""  # payment
        self.amountInc = ""  # payment

    def getJson(self):
        return json.dumps(self.__dict__)
