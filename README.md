# Django-Payment-Processes


This is an example of payment processing system using payment processing using the Django Framework, Celery and RabbitMQ server.

## Structure 
The structure is typical to the one of a common Django project the app being located in the 'payment' directory.

In alphabetical order, the files and their assigned responsibilities are:

1. celery.py -> configuration and initiation of celery
2. dispatcher.py -> contains class that implements the logic for dispatching the payments to their gateways
3. forms.py -> contains form class used in view
4. gateways.py -> implementation of the gateways
5. models.py -> implements the model of the payment
6. tests.py -> Implements the tests for the system
7. validators.py -> contains the validation fields for the payment
8. views.py -> contains the view class for the payment.

Special requirements: Make sure you have a RabbitMq server running on your host (Recommend using a Linux System)

Instalation:

```

pip install -r requirements.txt 
python manage.py makemigrations 
python manage,py migrate 
python manage.py runserver 

```


