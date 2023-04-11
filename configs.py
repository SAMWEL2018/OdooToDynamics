import os


class Configs:
    def __init__(self):
        self.url = os.getenv("URL")
        self.db=os.getenv("DB")
        self.username = os.getenv("UNAME")
        self.password = os.getenv("PASSW")
        self.logsDir = os.getenv("LOGDIR")
        self.live_items_url = os.getenv("LIVE_URL_ITEM")
        self.test_items_url = os.getenv("TEST_URL_ITEM")
        self.live_sale_order_url = os.getenv("LIVE_URL_SALES_ORDER")
        self.test_sale_order_url = os.getenv("TEST_URL_SALES_ORDER")
        self.MYSQL_USER= os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD= os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DB= os.getenv("MYSQL_DB")
        self.MYSQL_HOST= os.getenv("MYSQL_HOST")