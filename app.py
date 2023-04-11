from threading import Thread
from time import sleep

import pymysql
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from dotenv import load_dotenv
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from waitress import serve
from flask_cors import CORS

from DataFetch import Fetch
from HttpService import HttpService
from OrderProcessingService import OrderProcessing
from OrderTrackerNumber import findCurrentOrderIndex
from Reprocessing import Reprocesing
from Dbqueries import query

load_dotenv(override=False, dotenv_path='.env')

app = Flask(__name__)
CORS(app)

pos = OrderProcessing()
items = HttpService()
reprocess = Reprocesing()
dataFetch = Fetch()
query = query()

@app.route('/')
def server():
    return 'SERVER IS UP'

@app.route('/getposted',methods=['GET'])
def getPosted():
    return query.getPosted()

@app.route('/getfailed',methods=['GET'])
def getFailed():
    query.getFailed()

@app.route('/getlinefromorder',methods=['GET'])
def getExact():
    res= query.getExactLines()
    return res


@app.route('/paymentmethodspecific/<id>', methods=['GET'])
def getPayMethod(id):
    payment = dataFetch.getPaymentMethod(id)

    try:
        payment_method = payment[0]['payment_method_id'][1]
        return payment_method
    except:
        return "System Error, Contact Admin!"


@app.route('/order/<id>', methods=['GET'])
def getOrder(id):
    order = dataFetch.posHeader(id)
    return order


@app.route('/getlines/<id>', methods=['GET'])
def getLines(id):
    lines = dataFetch.getLines(int(id))
    return lines


@app.route('/postcorrects/<id>', methods=['POST'])
def PostCorrects(id):
    correctional_index = int(id)
    try:
        res = pos.processOrder(correctional_index, True)
        return res
    except:
        return "Internal Server Error", 500


def post():
    id = int(findCurrentOrderIndex())
    pos.processOrder(id, False)
    # reprocess.findUnprocessedOrders()
    # sleep(3)



executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 1
}
scheduler = BackgroundScheduler(job_defaults=job_defaults)
# Create the job
scheduler.add_job(func=post, trigger="interval", seconds=3)  # Start the scheduler
# scheduler.add_job(func=fetch, trigger='cron', minute='*/1')  # Start the scheduler
scheduler.start()

if __name__ == '__main__':
    # serve(app)
    serve(app, host='0.0.0.0', port=5000)
    # app.run()
