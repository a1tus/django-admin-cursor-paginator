# django-admin-cursor-paginator
Drop-in replacement for django admin default pagination that works fast with huge tables.

## Test project

In `testproject` folder you can (surprisingly) find test project that uses this app
for one model so that you can see live example and check how it works if you want.

All you need is to install requirements from `requirements.txt` in some env,
run `./manage.py runserver`, login as admin:admin to django admin and open `Product` list.

Project includes sqlite3 file with some test data and preinstalled `debug_toolbar`
to observe db queries.

You will get something like that:

![](assets/testproject-example.png)

After that you can play with ordering field or data amount or may be test it in your target db.