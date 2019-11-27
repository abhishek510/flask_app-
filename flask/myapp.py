from flask import Flask
from configuration import *
from flask_restplus import Api, Resource, fields
from flask_celery import make_celery
import math
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import logging
import time

app = Flask(__name__)
api = Api(app)
# broker and backend connection strings in configuration file
app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_BACKEND'] = CELERY_BACKEND_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# logging.basicConfig(filename='app.log', level=logging.DEBUG)

celery = make_celery(app)
db = SQLAlchemy(app)

# engine creates an interface to interact with the mysql db
# needed to query db and get the task status
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

# post request requires a model so that it knows what kind  of data to expect
# this corresponds to post needing a number to calculate factorial
numbers = api.model('Number', {'number': fields.Integer})


@api.route('/get_task_status/<task_id>')
class Getstatus(Resource):
    def get(self, task_id):
        '''Returns status of a task from MYSQL db given the task_id

           .. :quickref: Get status of task from database

           --Example Request--

           ..sourcecode:: http

           GET/get_task_status/{task_id}
           host: localhost
           Accept: task_id(string)

           --Example Response--

           ..sourcecode:: http
            content-length: 10
            content-type: application/json
            date: Sun, 10 Nov 2019 01:27:23 GMT
            server: Werkzeug/0.16.0 Python/3.7.3

            ["SUCCESS"]'''
        query_1 = "SELECT status FROM celery_taskmeta where task_id = \""
        query = query_1 + task_id + "\""
        result = engine.execute(query)
        try:
            # .fetchall() retrieves all the rows from engine.result object
            # since we have only 1 row here get status from [0][0]
            status = result.fetchall()[0][0]
        except:
            # if not found it throws out of bound exception
            status = "Not Found"
        return status


@api.route('/calculate_factorial')
class Createtask(Resource):
    @api.expect(numbers)
    def post(self):
        '''Adds a new task to celery taskqueue to find factorial of number
           given in this post request

           Example curl Request:
           curl -X POST "http://127.0.0.1:5000/calculate_factorial" -H
           "accept: application/json" -H  "Content-Type: application/json" -d
            "{  \"number\": 10000}"

           host: localhost
           Accept: application/json

           Response:
            "task sent"

            Response headers:
            content-length: 12
            content-type: application/json
            date: Sun, 10 Nov 2019 01:27:58 GMT
            server: Werkzeug/0.16.0 Python/3.7.3
'''
        # api.payload gets the json sent with the post request
        num = api.payload.get('number')
        # .delay function just points to .apply_async function
        result = task.delay(num)
        return result.status

# celery.task is decorator to indicate this task is run by celery workers
@celery.task(name='myapp.task')
def task(number):
    result = math.factorial(number)
    return result
