from threading import Thread
from time import sleep

from dotenv import load_dotenv
from flask import Flask

# from HttpService import HttpService
# from InvoiceProcessingService import InvoiceProcessingService


load_dotenv(override=False,dotenv_path='.env')

app = Flask(__name__)
#
# pos = InvoiceProcessingService()
# items= HttpService()


@app.route('/')
def server():
    return 'SERVER IS UP'


# def fetch():
#     while True:
#         pos.processInvoice()
#         sleep(3)

#
# task = Thread(target=fetch(), daemon=False, name='background')
# task.start()

if __name__ == '__main__':
    app.run()
