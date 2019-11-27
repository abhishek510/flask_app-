# flask_app

This a full implementation of a distributed web server
a. wsgi server (using Flask + Rest Plus)
b. 2 API endpoint handlers.
i. API 1: Receive POST request and add a job into celery queue backed
by Redis and save task in a db MySql
---- Job function is to do a factorial of a number received from the post request
ii. API 2: Receive GET request and respond the status of completion of
job in queue - Retrieved from DB
Added sphinx documentation

Bootstrap the entire project into a self building docker containers- used docker compose
Used a nginx instance which routes requests to appropriate containers