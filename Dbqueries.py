import json

import pymysql

from configs import Configs


#
class query:

    def sql_connector(self):
        cfg1 = Configs()
        # conn = pymysql.connect(user='root', password='', db='system', host='localhost')
        conn = pymysql.connect(user=cfg1.MYSQL_USER, password=cfg1.MYSQL_PASSWORD
                               , db=cfg1.MYSQL_DB, host=cfg1.MYSQL_HOST)
        c = conn.cursor()
        return conn, c

    #
    def PostAllOrders(self, id, doc_no, is_posted,date_posted,reason):
        conn, c = self.sql_connector()
        # c.execute("SELECT * FROM `orders` WHERE `order_id` = 31214")
        c.execute("INSERT INTO orders VALUES ('{}','{}','{}','{}','{}')".format(id, doc_no, is_posted,date_posted,reason))
        conn.commit()
        conn.close()
        c.close()
        return "created record", 201

    #
    def Postlines(self, id, doc_no, product_name, reference_no, qty, unit_price, item_id):
        conn, c = self.sql_connector()
        c.execute(
            "INSERT INTO orderlines VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(id, doc_no,
                                                                                        product_name,
                                                                                        reference_no,
                                                                                        qty, unit_price, item_id))
        conn.commit()
        conn.close()
        c.close()
        return "created record", 201

    def UpdateOrder(self, id):
        conn, c = self.sql_connector()
        c.execute("UPDATE `orders` SET `is_posted`=1 WHERE `order_id`= %s" % id)
        conn.commit()
        conn.close()
        return 'database updated'

    def getPosted(self):
        conn, c = self.sql_connector()
        res=c.execute("SELECT * from orders WHERE orders.is_posted = 1")
        print(res)
        conn.commit()
        conn.close()
        return "res", 200

    def getFailed(self):
        conn, c = self.sql_connector()
        c.execute("SELECT * FROM `orders` WHERE `is_posted`=0")
        conn.commit()
        conn.close()
        return 'data fetched successfully', 200

    def getExactLines(self):
        conn, c = self.sql_connector()
        data = c.execute("SELECT * FROM orderlines WHERE order_id=2700")
        conn.commit()
        conn.close()
        print(data)
        return json.dumps(data), 200

    def getLatestId(self):
        conn, c = self.sql_connector()
        c.execute("SELECT * FROM `orders` WHERE `is_posted`=0")
        conn.commit()
        conn.close()
        return 'data fetched successfully', 200



#
