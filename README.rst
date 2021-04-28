bmat-report-isrcs
==================

|Python-Versions| |pip-Version| |Django-Version| |DjangoRest-Version| |Environ-Version| |Bcrypt-Version| |Celery-Version| |DjangoRestJWT-Version|

``trade-core-social-network`` is a basic social network which consists of users and posts. Users can sign up/in, create posts, view/like/dislike other
Users' posts

--------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:

Project requirements ?
---------------------------
Below are the requirements of the project :

* On the sign up, the email must be verified through the email validation API `abstractapi <https://www.abstractapi.com/>`_ and only sign up valid emails
* Once signed up, enrich the User with geolocation data of the IP ; based on geolocation of the IP, check if the signup date coincides with a holiday in the User’s country, and save that info. This data enrichment must be performed asynchronously, and through the geolocation data and Holiday API of `abstractapi <https://www.abstractapi.com/>`_
* use JWT for authentification
* API endpoints must be covered with tests

Technologies used and Why ?
---------------------------

To resolve this problem, we have used ``python``, ``django``, ``djangorestframework`` , ``requests`` , ``django-environ`` , ``Bcrypt`` , ``Celery`` , ``djangorestframework_simplejwt`` ,

* ``python``: among the requirements.
* ``django``: among the requirements.
* ``djangorestframework``: we were asked to develop a simple RESTFul API. Thereby, *djangorestframework* best fits the problem
* ``requests``: to request the holiday, geolocation and email validation third-party API.
* ``django-environ``: to set environment variables in django, for sensible data(API_KEY, SECRET_KEY) storage and security.
* ``Bcrypt``: to hash password before storing in the database.
* ``Celery``: *Celery* is an asynchronous job queue. It helps to perform the user data enrichment after the signUP
* ``djangorestframework_simplejwt``: to perform the JSON Web Token authentification in djangorestframework.


Installation
------------

To run my solution, you must have ``python`` and ``pip`` installed in your system.

Download the project from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To clone my code, you run the command below in the CLI

.. code:: sh

    git clone "https://github.com/adrienTchounkeu/trade_core_social_network.git"

You can also download the project by clicking the link `trade_core_social_network <https://github.com/adrienTchounkeu/trade_core_social_network.git>`_


Install Dependencies
~~~~~~~~~~~~~~~~~~~~~

After downloading the code, Open the CLI in the root directory and execute the command :

.. code:: sh

   pip install -r requirements.txt


NB: *"requirements.txt is a file which contains all the project dependencies"*

All the project dependencies installed, run the command

.. code:: sh

   python manage.py runserver # on Windows

or

.. code:: sh

   python3 manage.py runserver # on Linux


NB: *The server is running on the default port 8000*

Analyzing & Solving ``trade_core_social_network`` API
------------------------------------------------------

After installing all the dependencies, we must dive into the ``models`` , ``views`` ,and ``urls``.

We need a *User* and a *Post* models to save and retrieve users and posts from the database through the ORM (Object Relational Mapper)
To save a view/like/dislike post actions, we used the ViewPost, LikePost, and UnLikePost intermediate models which were respectively linked
to the views, likes and unlikes attributes of the *Post* model.

For the views, we implement a shared_task with celery to perform the data enrichment. The endpoints developed are below :

* ``POST /user`` user signUp
* ``GET /user`` get user data
* ``POST /login`` user login
* ``POST /post`` create a post
* ``GET /post`` get post data
* ``POST /view`` view a post by a user
* ``POST /like`` like a post by a user
* ``POST /unlike`` unlike a post by a user


Assumptions & Decisions
~~~~~~~~~~~~~~~~~~~~~~~

To solve the problem, we did some hypothesis & decisions:

* we have put the .env file in the GITHUB repo, for you to see and test the code. NB: *We never display sensitive data*
* the user enters correct informations because no bad formatted data have been handled


Tests
~~~~~

*Tests* have been done to test the endpoints. To run the tests, run the command ``python manage.py test``


Real-life Adaptation
~~~~~~~~~~~~~~~~~~~~

* add a redis-server to perform and optimize caching



.. |Python-Versions| image:: https://img.shields.io/pypi/pyversions/pip?logo=python&logoColor=white   :alt: Python Version
.. |pip-Version| image:: https://img.shields.io/pypi/v/pip?label=pip&logoColor=white   :alt: pip  Version
.. |Django-Version| image:: https://img.shields.io/pypi/v/django?label=django&logo=django   :alt: django Version
.. |DjangoRest-Version| image:: https://img.shields.io/pypi/v/djangorestframework?label=djangorestframework&logo=django   :alt: DjangoRests Version
.. |Environ-Version| image:: https://img.shields.io/pypi/v/django-environ?label=django-environ&logo=django-environ   :alt: Environ Version
.. |Bcrypt-Version| image:: https://img.shields.io/pypi/v/bcrypt?label=bcrypt&logo=bcrypt   :alt: bcrypt Search
.. |Celery-Version| image:: https://img.shields.io/pypi/v/celery?color=green&label=celery&logo=celery&logoColor=green   :alt: celery Search
.. |DjangoRestJWT-Version| image:: https://img.shields.io/pypi/v/djangorestframework_simplejwt?label=djangorestframework_simplejwt&logo=djangorestframework_simplejwt   :alt: DjangoRestJWT Search
