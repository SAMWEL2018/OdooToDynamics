from OrderTrackerNumber import SkippedOrderFile
from OrderProcessingService import OrderProcessing
from DataFetch import Fetch


class Reprocesing:

    def findUnprocessedOrders(self):
        with open(SkippedOrderFile, 'r+') as r:
            order = r.readlines()
            if len(order) > 0:
                for i in order:
                    print('order id is: ' + i)
                    # print("occupation: "+i[0])
                    OrderProcessing().processOrder(int(i))
            else:
                print('no unprocessed order')
